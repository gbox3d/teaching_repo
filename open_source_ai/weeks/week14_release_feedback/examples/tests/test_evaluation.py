"""Ollama 없이 채점 계약과 실제 자식 프로세스 수명 주기를 검증한다."""

import copy
import io
import json
import sys
import threading
import time
import unittest
from unittest.mock import patch

from shared import DATA_DIR, MAX_ITEMS, normalize, validate_response
from shared.evaluation import Worker, evaluate, score_response, validate_dataset


# 테스트 전용 모듈을 자식 안에서만 주입한다. 실제 shared.worker의 입출력을 실행한다.
STUB = r'''
import os, runpy, subprocess, sys, time, types
bot = types.ModuleType("student_bot")
calls = 0
mode = sys.argv[1] if len(sys.argv) > 1 else ""
def answer(question):
    global calls
    calls += 1
    assert type(question) is str
    if mode == "느린 준비" and calls == 1:
        time.sleep(.3)
    if mode == "준비 형식 오류" and calls == 1:
        return "준비 출력의 형식 오류"
    if question == "자식 생성":
        child = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(3)"])
        return {"answers": [str(child.pid)], "sources": ["doc"], "abstain": False}
    if question == "시간 초과":
        time.sleep(60)
    if question == "실행 오류":
        raise RuntimeError("의도한 테스트 오류")
    if question == "강제 종료":
        os._exit(7)
    if question == "잘못된 형식":
        return {"answers": [], "sources": [], "abstain": "false"}
    if question == "일반 문자열":
        return "JSON이 아닌 실제 응답"
    if question == "긴 출력":
        return {"answers": ["x" * 70000], "sources": [], "abstain": False}
    if question == "로그 분리":
        print("학생 진단 메시지: 표준 오류로 출력")
    if question.startswith("문자열만") or question in ("프로세스 확인", "로그 분리"):
        return {"answers": [question, str(os.getpid()), str(calls)], "sources": ["doc"], "abstain": False}
    return {"answers": [], "sources": [], "abstain": True}
bot.answer = answer
sys.modules["student_bot"] = bot
runpy.run_module("shared.worker", run_name="__main__")
'''
COMMAND = [sys.executable, "-u", "-c", STUB]


def gold(expected=None, sources=None, *, abstain=False, item_id="q1"):
    return {"id": item_id, "expected": expected if expected is not None else [["익산시", "익산"]],
            "sources": sources if sources is not None else ["doc"], "abstain": abstain}


def response(answers=None, sources=None, *, abstain=False):
    return {"answers": answers if answers is not None else ["익산시"],
            "sources": sources if sources is not None else ["doc"], "abstain": abstain}


class ScoringTests(unittest.TestCase):
    def test_perfect_zero_and_source_gate(self):
        self.assertEqual(score_response(response(), gold())["score"], 100)
        wrong = score_response(response(["전주시"]), gold())
        self.assertEqual(wrong["score"], 0)
        self.assertEqual(wrong["subscores"]["source_f1"], 1)
        self.assertEqual(wrong["subscores"]["source_points"], 0)
        self.assertEqual(score_response(response(sources=[]), gold())["score"], 80)

    def test_partial_and_spam_penalize_precision(self):
        expected = gold([["익산시"], ["봉황"]], ["doc", "symbols"])
        partial = score_response(response(), expected)
        self.assertAlmostEqual(partial["score"], 100 * 2 / 3)
        spam = score_response(response(["익산시", "전주시", "서울시"]), gold())
        self.assertEqual(spam["subscores"]["answer_f1"], .5)
        self.assertEqual(spam["score"], 60)
        self.assertEqual(score_response(response(sources=["doc", "noise", "extra"]), gold())["score"], 90)

    def test_normalized_duplicates_not_counted_twice(self):
        self.assertEqual(score_response(response(["익산시", " 익 산 시. ", "익산시．．"],
                                                ["doc", " ＤＯＣ. "]), gold())["score"], 100)
        # 서로 다른 별칭은 한 사실에 둘 다 매칭되지 않으며 precision 분모에는 남는다.
        self.assertAlmostEqual(score_response(response(["익산", "익산시"]), gold())["score"], 80 * 2 / 3 + 20)

    def test_normalization_preserves_negation_signs_and_punctuation(self):
        self.assertEqual(normalize(" ＡＢＣ . "), "abc")
        for text in ("익산시가 아니다", "익산시는", "익산시!", "익산시?", "익산시, 전주시"):
            with self.subTest(text=text):
                self.assertEqual(score_response(response([text]), gold())["score"], 0)
        for text in ("-5", "+5", "5%", "5/", "5,", "5。"):
            with self.subTest(text=text):
                self.assertEqual(score_response(response([text]), gold([["5"]]))["score"], 0)
        self.assertEqual(normalize("0.5"), "0.5")
        self.assertEqual(normalize("063-850-5114"), "063-850-5114")
        self.assertNotEqual(normalize("https://a/"), normalize("https://a"))

    def test_aliases_exact_and_maximum_bipartite_matching(self):
        self.assertEqual(score_response(response(["익산"]), gold())["score"], 100)
        overlapping = gold([["a", "b"], ["a"]])
        self.assertEqual(score_response(response(["a", "b"]), overlapping)["score"], 100)
        one = score_response(response(["a"]), overlapping)
        self.assertEqual(one["subscores"]["matched_facts"], 1)
        self.assertAlmostEqual(one["score"], 80 * 2 / 3 + 20)

    def test_unknown_requires_all_three_conditions(self):
        unknown = gold([], [], abstain=True)
        self.assertEqual(score_response(response([], [], abstain=True), unknown)["score"], 100)
        for result in (response([], []), response(["모릅니다"], [], abstain=True),
                       response([], ["doc"], abstain=True), response()):
            self.assertEqual(score_response(result, unknown)["score"], 0)
        self.assertEqual(score_response(response(abstain=True), gold())["score"], 0)

    def test_strict_schema_false_bool_missing_extra_and_limits(self):
        bad_responses = [None, [], {"answers": [], "sources": []},
                         dict(response(), explanation="추가 키")]
        for invalid_bool in ("false", "true", 0, 1, None):
            bad_responses.append(response(abstain=invalid_bool))
        for bad_list in ("익산시", ("익산시",), [1], [None], [""], ["  "], ["..."],
                         ["x" * 257], ["x"] * (MAX_ITEMS + 1)):
            bad_responses.append(response(answers=bad_list))
        for bad_list in ("doc", [False], [""], [" "], ["x" * 129], ["x"] * (MAX_ITEMS + 1)):
            bad_responses.append(response(sources=bad_list))
        for result in bad_responses:
            with self.subTest(result=str(result)[:100]):
                scored = score_response(result, gold())
                self.assertEqual(scored["score"], 0)
                self.assertEqual(scored["status"], "invalid_response")
        self.assertIs(validate_response(response())["abstain"], False)


class DatasetTests(unittest.TestCase):
    def setUp(self):
        self.questions = json.loads((DATA_DIR / "public_questions.json").read_text(encoding="utf-8"))
        self.answers = json.loads((DATA_DIR / "public_answers.json").read_text(encoding="utf-8"))

    def test_public_all_20_and_each_perfect_answer(self):
        by_id = validate_dataset(self.questions, self.answers)
        self.assertEqual(len(by_id), 20)
        self.assertEqual({category: sum(q["category"] == category for q in self.questions)
                          for category in ("fact", "composite", "unknown")},
                         {"fact": 12, "composite": 4, "unknown": 4})
        corpus_ids = {doc["id"] for doc in json.loads((DATA_DIR / "corpus.json").read_text(encoding="utf-8"))}
        for question in self.questions:
            expected = by_id[question["id"]]
            with self.subTest(item_id=question["id"]):
                prediction = response([group[0] for group in expected["expected"]],
                                      expected["sources"], abstain=expected["abstain"])
                self.assertEqual(score_response(prediction, expected)["score"], 100)
                self.assertTrue(set(expected["sources"]) <= corpus_ids)

    def test_wrong_ids_labels_missing_and_extra_columns_rejected(self):
        mutations = [
            lambda qs, gs: qs[0].update(id=qs[1]["id"]),
            lambda qs, gs: gs[0].update(id=gs[1]["id"]),
            lambda qs, gs: gs[0].update(id="wrong-id"),
            lambda qs, gs: gs.pop(),
            lambda qs, gs: gs.append(gold(item_id="extra")),
            lambda qs, gs: qs[0].update(category="facts"),
            lambda qs, gs: qs[0].update(category="unknown"),
            lambda qs, gs: qs[-1].update(category="fact"),
            lambda qs, gs: qs[0].update(extra="column"),
            lambda qs, gs: gs[0].update(extra="column"),
            lambda qs, gs: qs[0].pop("question"),
            lambda qs, gs: gs[0].pop("expected"),
            lambda qs, gs: gs[0].update(abstain="false"),
            lambda qs, gs: gs[0].update(expected=[[]]),
            lambda qs, gs: gs[0].update(expected=["익산시"]),
            lambda qs, gs: gs[0].update(sources=[]),
        ]
        for index, mutate in enumerate(mutations):
            qs, gs = copy.deepcopy(self.questions), copy.deepcopy(self.answers)
            mutate(qs, gs)
            with self.subTest(index=index), self.assertRaises(ValueError):
                validate_dataset(qs, gs)
        with self.assertRaises(ValueError):
            validate_dataset([], [])

    def test_full_20_coverage_macro_is_per_question_not_category(self):
        report = evaluate(self.questions, list(reversed(self.answers)), worker_command=COMMAND)
        self.assertEqual(report["total"], 20)
        self.assertEqual([r["id"] for r in report["results"]], [q["id"] for q in self.questions])
        self.assertEqual(report["mean_score"], 20)  # known 16개 0점 + unknown 4개 100점
        self.assertEqual(report["categories"]["unknown"], {"count": 4, "mean_score": 100})
        self.assertEqual(report["warmup"]["status"], "ok")


class WorkerTests(unittest.TestCase):
    def assert_clean(self, process):
        self.assertIsNotNone(process.poll())
        self.assertTrue(process.stdin.closed)
        self.assertTrue(process.stdout.closed)
        self.assertFalse(any(t.name == "evaluation-worker-io" for t in threading.enumerate()))

    def test_persistent_process_utf8_stderr_and_close(self):
        with Worker(COMMAND) as worker:
            first = worker.request("프로세스 확인", 5)
            second = worker.request("로그 분리", 5)
            third = worker.request("문자열만 한글\n두 번째 줄", 5)
            self.assertEqual(first["answers"][1], second["answers"][1])
            self.assertEqual(second["answers"][2], "2")
            self.assertEqual(third["answers"][0], "문자열만 한글\n두 번째 줄")
            process = worker.process
        self.assert_clean(process)

    def test_timeout_kills_worker_and_next_request_restarts(self):
        with Worker(COMMAND) as worker:
            first = worker.request("프로세스 확인", 5)
            process = worker.process
            with self.assertRaises(TimeoutError):
                worker.request("시간 초과", .1)
            self.assert_clean(process)
            second = worker.request("프로세스 확인", 5)
            self.assertNotEqual(first["answers"][1], second["answers"][1])
            self.assertEqual(second["answers"][2], "1")
            restarted = worker.process
        self.assert_clean(restarted)

    def test_timeout_kills_descendant_holding_stdout_even_after_parent_exits(self):
        for question in ("시간 초과", "강제 종료"):
            with self.subTest(question=question), Worker(COMMAND) as worker:
                worker.request("자식 생성", 5)
                process = worker.process
                started = time.perf_counter()
                with self.assertRaises(TimeoutError):
                    worker.request(question, .05)
                elapsed = time.perf_counter() - started
                self.assertLess(elapsed, 1.5, "자식의 3초 sleep이 끝나기를 기다리면 안 됩니다.")
                self.assert_clean(process)

    def test_exception_exit_and_oversized_output_cleanup(self):
        for question in ("실행 오류", "강제 종료", "긴 출력"):
            with self.subTest(question=question), Worker(COMMAND) as worker:
                worker.request("프로세스 확인", 5)
                process = worker.process
                with self.assertRaises((RuntimeError, ValueError)):
                    worker.request(question, 5)
                self.assert_clean(process)

    def test_keyboard_interrupt_cleans_up(self):
        with Worker(COMMAND) as worker:
            worker.request("프로세스 확인", 5)
            process = worker.process
            with patch("shared.evaluation.queue.Queue.get", side_effect=KeyboardInterrupt):
                with self.assertRaises(KeyboardInterrupt):
                    worker.request("시간 초과", 5)
            self.assert_clean(process)

    def test_errors_remain_in_denominator_and_details(self):
        labels = ["시간 초과", "실행 오류", "잘못된 형식", "일반 문자열", "응답 불가"]
        questions = [{"id": f"q{i}", "category": "unknown", "question": label}
                     for i, label in enumerate(labels)]
        answers = [gold([], [], abstain=True, item_id=q["id"]) for q in questions]
        report = evaluate(questions, answers, timeout=.3, worker_command=COMMAND)
        self.assertEqual([row["status"] for row in report["results"]],
                         ["timeout", "error", "invalid_response", "invalid_response", "ok"])
        self.assertEqual(report["total"], 5)
        self.assertEqual(report["mean_score"], 20)
        self.assertEqual(report["results"][2]["response"], response([], [], abstain="false"))
        self.assertEqual(report["results"][3]["response"], "JSON이 아닌 실제 응답")
        self.assertEqual(report["categories"]["fact"], {"count": 0, "mean_score": None})
        for row in report["results"]:
            self.assertTrue({"id", "category", "response", "gold", "subscores", "error", "latency"} <= row.keys())

    def test_warmup_timeout_recorded_without_unprepared_scored_call(self):
        sent = []
        original = Worker.request

        def first_warmup_times_out(worker, question, timeout):
            sent.append(question)
            return original(worker, "시간 초과" if len(sent) == 1 else question, timeout)

        questions = [{"id": f"q{i}", "category": "unknown", "question": "응답 불가"} for i in range(2)]
        with patch.object(Worker, "request", first_warmup_times_out):
            report = evaluate(questions, [gold([], [], abstain=True, item_id=q["id"]) for q in questions],
                              warmup_timeout=.1, worker_command=COMMAND)
        self.assertEqual(report["warmup"]["status"], "timeout")
        self.assertEqual(len(report["warmups"]), 2)
        self.assertEqual(sent.count("응답 불가"), 1)
        self.assertEqual(report["mean_score"], 50)
        self.assertEqual(report["total"], 2)
        self.assertIn("모델 준비 실패", report["results"][0]["error"])

    def test_restarted_worker_is_warmed_again_and_warmup_time_excluded(self):
        questions = [{"id": "q1", "category": "unknown", "question": "실행 오류"},
                     {"id": "q2", "category": "unknown", "question": "응답 불가"}]
        answers = [gold([], [], abstain=True, item_id=q["id"]) for q in questions]
        report = evaluate(questions, answers, timeout=.15, warmup_timeout=2,
                          worker_command=COMMAND + ["느린 준비"])
        self.assertEqual([row["score"] for row in report["results"]], [0, 100])
        self.assertEqual(len(report["warmups"]), 2)
        for warmup in report["warmups"]:
            self.assertEqual(warmup["status"], "ok")
            self.assertGreaterEqual(warmup["latency"], .3)
        self.assertLess(report["results"][1]["latency"], .15)

    def test_schema_errors_in_warmup_and_question_keep_same_worker(self):
        questions = [{"id": "q1", "category": "unknown", "question": "잘못된 형식"},
                     {"id": "q2", "category": "fact", "question": "프로세스 확인"}]
        answers = [gold([], [], abstain=True), gold(item_id="q2")]
        report = evaluate(questions, answers, worker_command=COMMAND + ["준비 형식 오류"])
        self.assertEqual(report["warmup"]["status"], "invalid_response")
        self.assertEqual(report["warmup"]["response"], "준비 출력의 형식 오류")
        self.assertEqual(len(report["warmups"]), 1)
        self.assertEqual(report["results"][0]["status"], "invalid_response")
        self.assertEqual(report["results"][1]["response"]["answers"][2], "3")

    def test_parent_transmits_only_question_without_metadata(self):
        sent = []
        original = Worker.request

        def record(worker, question, timeout):
            sent.append(question)
            return original(worker, question, timeout)

        with patch.object(Worker, "request", record):
            evaluate([{"id": "secret-id", "category": "fact", "question": "문자열만 전달"}],
                     [gold([["secret-gold"]], item_id="secret-id")], worker_command=COMMAND)
        self.assertEqual(len(sent), 2)  # 준비 1개 + 채점 1개
        self.assertEqual(sent[-1], "문자열만 전달")
        self.assertNotIn("secret-id", str(sent))
        self.assertNotIn("secret-gold", str(sent))


class ChatTests(unittest.TestCase):
    def test_invalid_model_output_is_preserved_for_parent_feedback(self):
        import student_bot
        for content, expected in (("JSON이 아닌 실제 응답", "JSON이 아닌 실제 응답"),
                                  ('{"answer": "익산시"}', {"answer": "익산시"}),
                                  ('{"answers": [], "sources": [], "abstain": "false"}',
                                   response([], [], abstain="false"))):
            payload = json.dumps({"message": {"content": content}}).encode()
            with self.subTest(content=content), patch("student_bot.build_opener") as opener:
                opener.return_value.open.return_value = io.BytesIO(payload)
                actual = student_bot.answer("원광대학교 주소")
            self.assertEqual(actual, expected)
            self.assertEqual(score_response(actual, gold())["status"], "invalid_response")

    def test_both_chat_commands_use_same_answer_and_repeat_until_exit(self):
        from ex01_chat import main as first_chat
        from ex03_improve import main as improved_chat
        for command in (first_chat, improved_chat):
            with self.subTest(command=command.__module__), patch("builtins.input", side_effect=["", "첫 질문", "둘째 질문", "/bye"]), \
                 patch("student_bot.answer", return_value=response()) as answer, \
                 patch("sys.stdout", new_callable=io.StringIO) as output:
                command()
                self.assertEqual([call.args for call in answer.call_args_list], [("첫 질문",), ("둘째 질문",)])
                self.assertEqual(output.getvalue().count("AI>"), 2)

    def test_student_bot_reads_corpus_and_requests_plain_json_without_format(self):
        import student_bot
        payload = json.dumps({"message": {"content": json.dumps(response())}}).encode()
        with patch("student_bot.build_opener") as build_opener:
            request = build_opener.return_value.open
            request.return_value = io.BytesIO(payload)
            self.assertEqual(student_bot.answer("원광대학교 주소"), response())
        self.assertEqual(build_opener.call_args.args[0].proxies, {})
        self.assertEqual(request.call_args.args[0].full_url, "http://127.0.0.1:11434/api/chat")
        sent = json.loads(request.call_args.args[0].data)
        self.assertEqual(sent["model"], "qwen3.5:2b")
        self.assertIs(sent["stream"], False)
        self.assertNotIn("format", sent)
        self.assertIn('{"answers": [], "sources": [], "abstain": true}', sent["messages"][0]["content"])
        user = json.loads(sent["messages"][1]["content"])
        self.assertEqual(set(user), {"question", "documents"})
        self.assertEqual(len(user["documents"]), 3)
        self.assertIn("wku-location", {doc["id"] for doc in user["documents"]})


if __name__ == "__main__":
    unittest.main()
