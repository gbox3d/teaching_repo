import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import Mock, patch

from bleuno_control import Board, load_cases, validate_calls
from bleuno_control.evaluation import evaluate, expected_leds
from bleuno_control.training import train, trained_path


def call(name, **args):
    return {"name": name, "arguments": args}


class MemoryBoard:
    def __init__(self):
        self.leds = [0, 0, 0, 0]

    def execute(self, calls):
        validate_calls(calls)
        self.leds = expected_leds(calls, self.leds)
        return [{"result": "ok", "value": "[24.5,40.0]"} for _ in calls]

    def state(self):
        return {"leds": self.leds[:], "temperature": 24.5, "humidity": 40.0}


class ControlTests(unittest.TestCase):
    def test_invalid_tail_prevents_partial_execution(self):
        board = Board.__new__(Board)
        board.command = Mock()
        with self.assertRaises(ValueError):
            board.execute([call("turn_on", index=0), call("set_brightness", index=1, value=256)])
        board.command.assert_not_called()

    def test_bounds_types_missing_and_unknown(self):
        for calls in [[call("turn_on", index=True)], [call("turn_off", index=-1)],
                      [call("turn_on", index=4)], [call("set_brightness", index=1, value=1.0)],
                      [call("turn_on")], [call("read_environment", value=30)],
                      [call("__import__", index=0)], [call([], index=0)],
                      [call("turn_on", index="0")], {}, [call("read_environment")] * 9]:
            with self.subTest(calls=calls), self.assertRaises(ValueError):
                validate_calls(calls)

    def test_boundary_values_accepted(self):
        self.assertEqual(expected_leds([call("set_brightness", index=3, value=255),
                                        call("set_brightness", index=0, value=0)]), [0, 64, 128, 255])

    def test_input_events_before_reply_are_ignored(self):
        board = Board.__new__(Board)
        board.file = Mock()
        board.file.readline.side_effect = ['{"event":"input"}\n', '{"result":"ok"}\n']
        self.assertEqual(board.command("on 0"), {"result": "ok"})
        board.file.write.assert_called_once_with("on 0\n")

    def test_disconnect_is_an_error(self):
        board = Board.__new__(Board)
        board.file = Mock()
        board.socket = Mock()
        board.file.readline.return_value = ""
        with self.assertRaises(ConnectionError):
            board.command("dht11")
        self.assertTrue(board.closed)

    def test_event_overflow_closes_connection_before_next_command(self):
        board = Board.__new__(Board)
        board.file, board.socket = Mock(), Mock()
        board.file.readline.side_effect = ['{"event":"input"}\n'] * 32 + ['{"result":"ok"}\n']
        with self.assertRaises(ConnectionError):
            board.command("on 0")
        with self.assertRaises(ConnectionError):
            board.command("off 0")
        board.file.write.assert_called_once_with("on 0\n")
        board.file.close.assert_called_once()
        board.socket.close.assert_called_once()

    def test_all_published_cases_100_including_sensor_and_no_call(self):
        cases = load_cases()
        answers = {c["query"]: c["calls"] for c in cases}
        with redirect_stdout(io.StringIO()):
            rows, summary = evaluate(lambda q: answers.get(q, []), MemoryBoard(), cases)
        self.assertEqual(len(rows), 16)
        self.assertEqual(summary["success_rate"], 1)
        self.assertEqual(summary["false_call_rate"], 0)
        self.assertEqual(summary["by_language"], {"en": 1, "ko": 1})

    def test_errors_and_wrong_calls_remain_in_denominator(self):
        cases = [dict(id="1", language="ko", query="q1", calls=[call("turn_on", index=0)]),
                 dict(id="2", language="en", query="q2", calls=[]),
                 dict(id="3", language="en", query="q3", calls=[])]
        def predict(q):
            if q == "q3":
                raise RuntimeError("model failed")
            return [call("turn_on", index=0)]
        with redirect_stdout(io.StringIO()):
            rows, summary = evaluate(predict, MemoryBoard(), cases)
        self.assertEqual(summary["count"], 3)
        self.assertAlmostEqual(summary["success_rate"], 1 / 3)
        self.assertEqual(summary["false_call_rate"], .5)
        self.assertEqual(summary["error_count"], 1)
        self.assertFalse(rows[-1]["success"])

    def test_ok_ack_with_wrong_state_is_not_success(self):
        board = MemoryBoard()
        original = board.execute
        def ignore_on(calls):
            return [{"result": "ok"}] if calls and calls[0]["name"] == "turn_on" else original(calls)
        board.execute = ignore_on
        cases = [dict(id="1", query="on", calls=[call("turn_on", index=0)])]
        with redirect_stdout(io.StringIO()):
            rows, summary = evaluate(lambda q: cases[0]["calls"], board, cases)
        self.assertTrue(rows[0]["exact"])
        self.assertEqual(summary["success_rate"], 0)

    def test_execution_error_preserves_model_only_time(self):
        board = MemoryBoard()
        original = board.execute
        def fail_on(calls):
            if calls and calls[0]["name"] == "turn_on":
                raise ConnectionError("device failed")
            return original(calls)
        board.execute = fail_on
        cases = [dict(id="1", query="on", calls=[call("turn_on", index=0)])]
        with redirect_stdout(io.StringIO()), patch("bleuno_control.evaluation.time.perf_counter", side_effect=[10, 10.125]):
            rows, summary = evaluate(lambda q: cases[0]["calls"], board, cases)
        self.assertEqual(rows[0]["latency"], .125)
        self.assertEqual(summary["error_count"], 1)

    def test_device_setup_failure_keeps_all_cases_without_fake_latency(self):
        board = Mock()
        board.execute.side_effect = ConnectionError("disconnected")
        with redirect_stdout(io.StringIO()):
            rows, summary = evaluate(lambda q: [], board, load_cases())
        self.assertEqual(len(rows), 16)
        self.assertEqual(summary["error_count"], 16)
        self.assertEqual(summary["success_rate"], 0)
        self.assertEqual(summary["latency_count"], 0)
        self.assertIsNone(summary["median_seconds"])

    def test_state_query_failure_keeps_remaining_cases(self):
        board = MemoryBoard()
        original = board.state
        board.state = Mock(side_effect=[original(), ConnectionError("HTTP failed"), original(), original()])
        cases = [dict(id=str(i), query="no action", calls=[]) for i in range(2)]
        with redirect_stdout(io.StringIO()):
            rows, summary = evaluate(lambda q: [], board, cases)
        self.assertEqual(len(rows), 2)
        self.assertEqual(summary["error_count"], 1)
        self.assertEqual(summary["count"], 2)

    def test_failed_warmup_does_not_remove_evaluation_cases(self):
        predict = Mock(side_effect=[RuntimeError("warmup failed"), [], []])
        cases = [dict(id=str(i), query="no action", calls=[]) for i in range(2)]
        with redirect_stdout(io.StringIO()):
            rows, summary = evaluate(predict, MemoryBoard(), cases)
        self.assertEqual(summary["count"], 2)
        self.assertEqual(summary["success_rate"], 1)

    def test_training_checks_eval_overlap_before_loading_dependencies(self):
        question = load_cases()[0]["query"]
        rows = [dict(query=f"train-{i}", answers=[]) for i in range(9)] + [dict(query=question, answers=[])]
        with patch("pathlib.Path.read_text", return_value="\n".join(json.dumps(r) for r in rows)), patch("bleuno_control.training.load_cases", return_value=[dict(query=question)]):
            with self.assertRaisesRegex(ValueError, "학습과 평가"):
                train("unused.jsonl", "unused-output")

    def test_interrupted_training_blocks_even_existing_model_pair(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name in ("baseline.cact", "tuned.cact"):
                (root / name).write_bytes(b"previous model")
            marker = root / ".training-in-progress"
            marker.touch()
            with self.assertRaisesRegex(RuntimeError, "완료되지"):
                trained_path(root)
            marker.unlink()
            self.assertEqual(trained_path(root), root / "tuned.cact")
            (root / "baseline.cact").unlink()
            with self.assertRaises(FileNotFoundError):
                trained_path(root)


if __name__ == "__main__":
    unittest.main()
