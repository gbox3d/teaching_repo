"""Ollama 없이 lab_shared의 문항 세트 읽기, 워커 명령, 워커 통신을 확인한다."""

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import lab_shared
import shared
from lab_shared import load_set, worker_command
from shared.evaluation import Worker

SRC = Path(lab_shared.__file__).resolve().parents[1]

# 시험용 가짜 봇. import 때와 answer 안에서 print해 프로토콜과 섞이지 않는지 본다.
FAKE_BOT = '''
print("봇 import 때 출력")
calls = 0


def answer(question):
    global calls
    calls += 1
    print("봇 answer 안의 출력")
    if question == "오류":
        raise RuntimeError("의도한 시험 오류")
    if question == "NaN":
        return {"answers": [float("nan")], "sources": [], "abstain": False}
    return {"answers": [question, str(calls)], "sources": ["doc"], "abstain": False}
'''
# 14주 채점기의 Worker는 자식의 표준 오류를 그대로 물려주므로 print하지 않는 봇으로 시험한다.
QUIET_BOT = '''
def answer(question):
    if question == "오류":
        raise RuntimeError("의도한 시험 오류")
    return {"answers": [question], "sources": ["doc"], "abstain": False}
'''
# answer가 없거나 호출할 수 없는 봇. 워커는 끝나지 않고 질문마다 같은 안내를 ok:false로 보낸다.
NO_ANSWER_BOTS = {
    "lab_no_answer_bot": 'MODEL = "qwen3.5:2b"',
    "lab_not_callable_bot": 'answer = "함수가 아닌 값"',
}


def worker_env(folder: str) -> dict:
    """가짜 봇 폴더와 src를 PYTHONPATH에 넣는다. 자식 프로세스도 .pyc를 남기지 않는다."""
    paths = [folder, str(SRC), os.environ.get("PYTHONPATH", "")]
    return dict(os.environ, PYTHONPATH=os.pathsep.join(path for path in paths if path),
                PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1")


class LoadSetTests(unittest.TestCase):
    def test_public_reads_week14_public_files(self):
        questions, answers = load_set("public")
        self.assertEqual(questions, json.loads(
            (shared.DATA_DIR / "public_questions.json").read_text(encoding="utf-8")))
        self.assertEqual(answers, json.loads(
            (shared.DATA_DIR / "public_answers.json").read_text(encoding="utf-8")))
        self.assertEqual(len(questions), 20)

    def test_mine_and_train_read_data_dir_at_call_time(self):
        files = {
            "my_questions.json": [{"id": "my-01", "category": "fact", "question": "내 질문"}],
            "my_answers.json": [{"id": "my-01", "expected": [["답"]]}],
            "train_questions.json": [{"id": "train-01", "category": "fact", "question": "학습 질문"}],
            "train_answers.json": [{"id": "train-01", "expected": [["학습 답"]]}],
        }
        with tempfile.TemporaryDirectory() as folder:
            for name, data in files.items():
                (Path(folder) / name).write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
            with patch("lab_shared.DATA_DIR", Path(folder)):
                self.assertEqual(load_set("mine"), (files["my_questions.json"], files["my_answers.json"]))
                self.assertEqual(load_set("train"),
                                 (files["train_questions.json"], files["train_answers.json"]))
                # public은 DATA_DIR과 관계없이 14주차 공개 문항을 읽는다.
                self.assertEqual(len(load_set("public")[0]), 20)
        with tempfile.TemporaryDirectory() as empty, patch("lab_shared.DATA_DIR", Path(empty)):
            with self.assertRaises(OSError):  # ex04는 파일이 없으면 평가 시작 오류로 멈춘다.
                load_set("mine")

    def test_unknown_set_name_lists_choices(self):
        for name in ("my", "Mine", "", "private"):
            with self.subTest(name=name):
                with self.assertRaises(ValueError) as caught:
                    load_set(name)
                for choice in ("public", "mine", "train"):
                    self.assertIn(choice, str(caught.exception))


class WorkerCommandTests(unittest.TestCase):
    def test_student_bot_keeps_week14_worker(self):
        self.assertIsNone(worker_command("student_bot"))

    def test_other_bot_runs_lab_worker_with_its_name(self):
        self.assertEqual(worker_command("rag_bot"),
                         [sys.executable, "-u", "-m", "lab_shared.worker", "rag_bot"])

    def test_invalid_or_missing_bot_rejected(self):
        for name in ("", "rag-bot", "rag_bot.py", "../rag_bot", "rag bot", "1bot", "no_such_bot_for_test"):
            with self.subTest(name=name), self.assertRaises(ValueError):
                worker_command(name)


class WorkerProtocolTests(unittest.TestCase):
    def setUp(self):
        self.folder = self.enterContext(tempfile.TemporaryDirectory())
        (Path(self.folder) / "lab_test_bot.py").write_text(FAKE_BOT, encoding="utf-8")
        (Path(self.folder) / "lab_quiet_bot.py").write_text(QUIET_BOT, encoding="utf-8")
        for name, source in NO_ANSWER_BOTS.items():
            (Path(self.folder) / f"{name}.py").write_text(source, encoding="utf-8")
        self.command = [sys.executable, "-u", "-m", "lab_shared.worker", "lab_test_bot"]

    def run_worker(self, lines: list[str], command: list[str] | None = None) -> subprocess.CompletedProcess:
        return subprocess.run(command or self.command, input="".join(line + "\n" for line in lines),
                              capture_output=True, text=True, encoding="utf-8",
                              env=worker_env(self.folder), timeout=60)

    def test_envelopes_on_stdout_and_bot_prints_on_stderr(self):
        lines = [json.dumps("첫 질문", ensure_ascii=False), json.dumps("오류", ensure_ascii=False),
                 json.dumps("x" * (shared.MAX_QUESTION_LENGTH + 1)), "123", "JSON 아님",
                 json.dumps("NaN"), json.dumps("둘째 질문", ensure_ascii=False)]
        result = self.run_worker(lines)
        self.assertEqual(result.returncode, 0, result.stderr)
        replies = [json.loads(line) for line in result.stdout.splitlines()]
        self.assertEqual(len(replies), len(lines))
        self.assertEqual(replies[0], {"ok": True, "response": {
            "answers": ["첫 질문", "1"], "sources": ["doc"], "abstain": False}})
        self.assertEqual(replies[1], {"ok": False, "error": "RuntimeError: 의도한 시험 오류"})
        for reply in replies[2:6]:  # 길이 초과, 문자열이 아닌 질문, 깨진 JSON, JSON으로 못 보내는 NaN
            self.assertEqual(set(reply), {"ok", "error"})
            self.assertIs(reply["ok"], False)
        # 오류 뒤에도 같은 프로세스가 답한다. answer 호출 횟수가 이어진다.
        self.assertEqual(replies[6]["response"]["answers"], ["둘째 질문", "4"])
        self.assertIn("봇 import 때 출력", result.stderr)
        self.assertIn("봇 answer 안의 출력", result.stderr)

    def test_week14_parent_worker_reads_lab_worker(self):
        command = [sys.executable, "-u", "-m", "lab_shared.worker", "lab_quiet_bot"]
        with patch.dict(os.environ, worker_env(self.folder)), Worker(command) as worker:
            self.assertEqual(worker.request("문자열만 전달", 10),
                             {"answers": ["문자열만 전달"], "sources": ["doc"], "abstain": False})
            with self.assertRaisesRegex(RuntimeError, "의도한 시험 오류"):
                worker.request("오류", 10)

    def test_bot_without_callable_answer_replies_error_for_each_question(self):
        lines = [json.dumps("첫 질문", ensure_ascii=False), json.dumps("둘째 질문", ensure_ascii=False)]
        for name in NO_ANSWER_BOTS:
            command = [sys.executable, "-u", "-m", "lab_shared.worker", name]
            message = f"{name}에 answer(question) 함수가 없습니다."
            with self.subTest(bot=name):
                result = self.run_worker(lines, command)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual([json.loads(line) for line in result.stdout.splitlines()],
                                 [{"ok": False, "error": message}] * len(lines))
                self.assertNotIn("Traceback", result.stderr)
                # 14주 채점기의 Worker는 이 답을 실행 오류(RuntimeError)로 받는다.
                with patch.dict(os.environ, worker_env(self.folder)), Worker(command) as worker:
                    with self.assertRaises(RuntimeError) as caught:
                        worker.request("질문", 10)
                self.assertEqual(str(caught.exception), message)

    def test_bad_module_argument_stops_before_protocol(self):
        for arguments in ([], ["bad-name"], ["lab_test_bot", "extra"]):
            with self.subTest(arguments=arguments):
                result = self.run_worker([], [sys.executable, "-u", "-m", "lab_shared.worker", *arguments])
                self.assertEqual(result.returncode, 1)
                self.assertEqual(result.stdout, "")
                self.assertIn("사용법", result.stderr)
        # 없는 모듈은 import에서 멈춘다. 부모 채점기는 빈 응답을 실행 오류로 기록한다.
        result = self.run_worker([], [sys.executable, "-u", "-m", "lab_shared.worker", "no_such_bot_for_test"])
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")
        self.assertIn("ModuleNotFoundError", result.stderr)


if __name__ == "__main__":
    unittest.main()
