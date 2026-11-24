"""Ollama 없이 ex04의 실패 분류, 문항 내용 검사, 14주 evaluate 연결을 확인한다."""

import importlib
import io
import json
import os
import sys
import tempfile
import threading
import unittest
from contextlib import redirect_stdout
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from unittest.mock import patch

import ex04_my_eval
import lab_shared
import shared
from ex04_my_eval import KINDS, check_content, failure_table, lost_points, print_failures, print_result
from shared.evaluation import score_response, validate_dataset, zero_result

SRC = Path(lab_shared.__file__).resolve().parents[1]
CORPUS = json.loads((shared.DATA_DIR / "corpus.json").read_text(encoding="utf-8"))
PUBLIC_QUESTIONS = json.loads((shared.DATA_DIR / "public_questions.json").read_text(encoding="utf-8"))
DIGEST = "0123456789abcdef" * 4
EMBED_DIGEST = "fedcba9876543210" * 4

TWO_FACTS = {"id": "q", "expected": [["익산시", "익산"], ["봉황"]], "sources": ["wku-location", "wku-symbols"],
             "fact_sources": ["wku-location", "wku-symbols"], "abstain": False}
UNKNOWN = {"id": "q", "expected": [], "sources": [], "fact_sources": [], "abstain": True}


def reply(answers: list, sources: list, abstain: bool = False) -> dict:
    return {"answers": answers, "sources": sources, "abstain": abstain}


def row(item_id: str, gold: dict, response: object, scored: dict | None = None) -> dict:
    """evaluate가 on_result에 넘기는 행과 키가 같은 합성 행. 점수는 14주 score_response로 매긴다."""
    category = "unknown" if gold["abstain"] else "composite" if len(gold["expected"]) > 1 else "fact"
    scored = scored or score_response(response, gold)
    return dict(id=item_id, category=category, question="합성 질문", response=response,
                gold=dict(gold, id=item_id), **scored, latency=0.0)


ROWS = [
    row("timeout", TWO_FACTS, None, zero_result("TimeoutError: 문항 제한 시간 30초를 초과했습니다.", "timeout")),
    row("error", TWO_FACTS, None, zero_result("RuntimeError: 연결 거부", "error")),
    row("format", TWO_FACTS, "JSON이 아닌 응답"),
    row("answered-unknown", UNKNOWN, reply(["12석"], ["wku-services"])),
    row("refused", TWO_FACTS, reply([], [], abstain=True)),
    row("partial", TWO_FACTS, reply(["익산시"], ["wku-symbols"])),
    row("wrong-fact", TWO_FACTS, reply(["전주시"], ["wku-location"])),
    row("extra-source", TWO_FACTS, reply(["익산시", "봉황"], ["wku-location", "wku-symbols", "wku-history"])),
    row("perfect", TWO_FACTS, reply(["익산", "봉황"], ["wku-location", "wku-symbols"])),
    row("abstained-unknown", UNKNOWN, reply([], [], abstain=True)),
]


def pair(item_id: str, category: str, question: str, expected: list, fact_sources: list) -> tuple[dict, dict]:
    """질문과 v1.1 정답 한 쌍."""
    return ({"id": item_id, "category": category, "question": question},
            {"id": item_id, "expected": expected, "sources": list(dict.fromkeys(fact_sources)),
             "fact_sources": fact_sources, "abstain": category == "unknown"})


class FailureKindTests(unittest.TestCase):
    def test_lost_points_go_to_one_kind_or_split_into_fact_and_source(self):
        expected = {
            "timeout": {"시간 초과": 100}, "error": {"실행 오류": 100}, "format": {"형식 오류": 100},
            "answered-unknown": {"답변 불가인데 답함": 100}, "refused": {"답할 수 있는데 거절": 100},
            "partial": {"사실 누락·불필요한 답": 80 / 3, "출처 누락·불필요한 출처": 20},
            # 맞힌 사실이 없으면 출처를 맞게 적어도 출처 점수가 0이므로 100점 모두 사실 쪽이다.
            "wrong-fact": {"사실 누락·불필요한 답": 100},
            "extra-source": {"출처 누락·불필요한 출처": 4},
            "perfect": {}, "abstained-unknown": {},
        }
        for item in ROWS:
            with self.subTest(item=item["id"]):
                lost = lost_points(item)
                self.assertEqual(set(lost), set(expected[item["id"]]))
                for kind, points in expected[item["id"]].items():
                    self.assertAlmostEqual(lost[kind], points)
                self.assertAlmostEqual(sum(lost.values()), 100 - item["score"])

    def test_table_has_all_kinds_and_missing_points_plus_mean_is_100(self):
        table = failure_table(ROWS)
        self.assertEqual([kind for kind, _, _ in table], list(KINDS))
        self.assertEqual(len(KINDS), 7)
        by_kind = {kind: (ids, lost) for kind, ids, lost in table}
        self.assertEqual(by_kind["사실 누락·불필요한 답"][0], ["partial", "wrong-fact"])
        self.assertEqual(by_kind["출처 누락·불필요한 출처"][0], ["partial", "extra-source"])
        self.assertAlmostEqual(by_kind["출처 누락·불필요한 출처"][1], 24)
        mean = sum(item["score"] for item in ROWS) / len(ROWS)
        self.assertAlmostEqual(sum(lost for _, _, lost in table) / len(ROWS) + mean, 100)
        output = io.StringIO()
        with redirect_stdout(output):
            print_failures({"results": ROWS, "total": len(ROWS), "mean_score": mean})
        lines = output.getvalue().splitlines()
        self.assertIn("| 종류 | 문항 수 | 문항 id | 잃은 점수 합 | 전체 평균에서 빠진 점수 |", lines)
        self.assertIn("| 시간 초과 | 1 | timeout | 100.00 | 10.00 |", lines)
        self.assertIn("| 출처 누락·불필요한 출처 | 2 | partial, extra-source | 24.00 | 2.40 |", lines)
        self.assertTrue(lines[-1].startswith("빠진 점수 합 "))
        self.assertTrue(lines[-1].endswith(f"+ 전체 평균 {mean:.2f} = 100.00"))


class PrintResultTests(unittest.TestCase):
    def printed(self, item: dict) -> list[str]:
        output = io.StringIO()
        with redirect_stdout(output):
            print_result(item)
        return output.getvalue().splitlines()

    def test_failed_item_shows_question_then_response_and_error(self):
        rows = {item["id"]: item for item in ROWS}
        question = "원광대학교의\n소재   도시는? " + "가" * 200
        lines = self.printed(dict(rows["timeout"], question=question))
        shown = "원광대학교의 소재 도시는? " + "가" * 200  # 줄바꿈과 겹친 공백은 한 칸으로 보여 준다.
        self.assertEqual(lines[1:], [
            "    질문 " + shown[:ex04_my_eval.RESPONSE_WIDTH] + "...",
            "    응답 null",
            "    오류 TimeoutError: 문항 제한 시간 30초를 초과했습니다.",
        ])

    def test_passed_item_has_no_question_line(self):
        rows = {item["id"]: item for item in ROWS}
        for item_id in ("perfect", "abstained-unknown"):
            with self.subTest(item=item_id):
                lines = self.printed(rows[item_id])
                self.assertEqual(len(lines), 2)
                self.assertTrue(lines[0].endswith("실패: 없음"), lines[0])
                self.assertTrue(lines[1].startswith("    응답 "), lines[1])


class ContentCheckTests(unittest.TestCase):
    def check(self, *pairs: tuple[dict, dict]) -> tuple[list, list]:
        questions, answers = [q for q, _ in pairs], [a for _, a in pairs]
        validate_dataset(questions, answers)  # 형식이 맞는 자료로 내용만 본다.
        return check_content(questions, answers, CORPUS, PUBLIC_QUESTIONS)

    def test_clean_items_have_no_message(self):
        self.assertEqual(self.check(
            pair("my-01", "fact", "원광대학교가 있는 도시 이름은?", [["익산시", "익산"]], ["wku-location"]),
            pair("my-02", "composite", "원광대학교의 교목과 교화를 알려 주세요.",
                 [["은행나무"], ["백목련"]], ["wku-symbols", "wku-symbols"]),
            pair("my-03", "fact", "원광대학교 주소의 도로명과 건물번호는?", [["익산대로460"]], ["wku-location"]),
            pair("my-04", "fact", "원광대학교 공식 홈페이지 주소는?",
                 [["https://www.wku.ac.kr/", "www.wku.ac.kr"]], ["wku-services"]),
            pair("my-05", "unknown", "원광대학교 기숙사 방은 모두 몇 개인가요?", [], []),
        ), ([], []))

    def test_errors_name_the_question_id(self):
        public = PUBLIC_QUESTIONS[4]
        spaced = " " + public["question"].replace(" ", "  ") + " "
        errors, _ = self.check(
            pair("my-01", "fact", "원광대학교 기숙사 이름은?", [["새빛관"]], ["wku-dorm"]),
            pair("my-02", "fact", spaced, [["황금색"]], ["wku-symbols"]),
            pair("my-03", "fact", "원광대학교의 교조는?", [["봉황"]], ["wku-symbols"]),
            pair("my-04", "fact", "원광대학교의 교조는 ?", [["봉황"]], ["wku-symbols"]),
        )
        self.assertEqual(errors, [
            "[my-01] corpus에 없는 근거 문서 ID: wku-dorm",
            f"[my-02] 공개 문항과 같은 질문: {public['id']}",
            "[my-04] 세트 안에서 같은 질문: my-03",
        ])

    def test_warnings_for_alias_missing_from_document_and_single_fact_composite(self):
        errors, warnings = self.check(
            pair("my-01", "fact", "원광대학교의 교목은?", [["소나무"]], ["wku-symbols"]),
            pair("my-02", "composite", "원광대학교의 교화는?", [["백목련"]], ["wku-symbols"]),
            # '상징물'은 wku-symbols의 제목에만 있다. 별칭은 본문에서만 찾으므로 경고가 나와야 한다.
            pair("my-03", "fact", "원광대학교의 교색·교조·교목·교화를 묶어 부르는 말은?", [["상징물"]], ["wku-symbols"]),
        )
        symbols = next(doc for doc in CORPUS if doc["id"] == "wku-symbols")
        self.assertIn("상징물", symbols["title"])
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [
            "[my-01] 사실 1의 별칭이 근거 문서 본문에 없음: 소나무 (wku-symbols)",
            "[my-02] composite인데 사실이 하나",
            "[my-03] 사실 1의 별칭이 근거 문서 본문에 없음: 상징물 (wku-symbols)",
        ])


# 질문 낱말로 답을 고르는 가짜 봇. 준비 질문("소재 도시")에도 형식에 맞게 답한다.
FAKE_BOT = '''
def answer(question):
    if "도시" in question and "새" in question:
        return {"answers": ["익산시"], "sources": ["wku-symbols"], "abstain": False}
    if "도시" in question:
        return {"answers": ["익산시"], "sources": ["wku-location"], "abstain": False}
    if "교목" in question:
        raise RuntimeError("의도한 시험 오류")
    return {"answers": [], "sources": [], "abstain": True}
'''
MY_SET = [
    pair("t-01", "fact", "원광대학교가 있는 도시 이름은?", [["익산시", "익산"]], ["wku-location"]),
    pair("t-02", "composite", "원광대학교가 있는 도시와 상징하는 새를 알려 주세요.",
         [["익산시", "익산"], ["봉황"]], ["wku-location", "wku-symbols"]),
    pair("t-03", "fact", "원광대학교의 교목은?", [["은행나무"]], ["wku-symbols"]),
    pair("t-04", "fact", "원광대학교의 교화는?", [["백목련"]], ["wku-symbols"]),
    pair("t-05", "unknown", "오늘 학생식당 저녁 메뉴는?", [], []),
]


class FakeOllama(BaseHTTPRequestHandler):
    """조회 API만 흉내 낸다. 생성·임베딩 요청이 오면 기록해 시험이 실패하게 한다."""

    def do_GET(self):
        bodies = {"/api/version": {"version": "0.0.0-test"},
                  "/api/ps": {"models": [{"name": "fake-model:1b", "model": "fake-model:1b", "digest": DIGEST},
                                         {"name": "fake-embed:latest", "model": "fake-embed:latest",
                                          "digest": EMBED_DIGEST}]}}
        if self.server.broken or self.path not in bodies:
            self.send_error(500)
            return
        data = json.dumps(bodies[self.path]).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_POST(self):
        self.server.posts.append(self.path)
        self.send_error(500)

    def log_message(self, *args):
        pass


class MainTests(unittest.TestCase):
    def setUp(self):
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), FakeOllama)
        self.server.broken, self.server.posts = False, []
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.addCleanup(self.server.server_close)
        self.addCleanup(self.server.shutdown)
        self.folder = Path(self.enterContext(tempfile.TemporaryDirectory()))
        (self.folder / "ex04_test_bot.py").write_text(FAKE_BOT, encoding="utf-8")
        (self.folder / "data").mkdir()
        # 부모는 봇 위치를 sys.path에서 찾고, 워커 프로세스는 PYTHONPATH로 봇을 import한다.
        paths = [str(self.folder), str(SRC), os.environ.get("PYTHONPATH", "")]
        self.enterContext(patch.dict(os.environ, PYTHONPATH=os.pathsep.join(p for p in paths if p),
                                     PYTHONDONTWRITEBYTECODE="1"))
        self.enterContext(patch.object(sys, "path", [str(self.folder), *sys.path]))
        importlib.invalidate_caches()
        self.enterContext(patch("lab_shared.DATA_DIR", self.folder / "data"))
        self.enterContext(patch.object(ex04_my_eval, "BOT", "ex04_test_bot"))
        self.enterContext(patch.object(ex04_my_eval, "QUESTION_SET", "mine"))
        self.enterContext(patch.object(ex04_my_eval, "OLLAMA_HOST", f"http://127.0.0.1:{self.server.server_port}"))

    def write_mine(self, pairs: list) -> None:
        data = self.folder / "data"
        (data / "my_questions.json").write_text(json.dumps([q for q, _ in pairs], ensure_ascii=False),
                                                encoding="utf-8")
        (data / "my_answers.json").write_text(json.dumps([a for _, a in pairs], ensure_ascii=False),
                                              encoding="utf-8")

    def run_main(self) -> tuple[object, list[str]]:
        output = io.StringIO()
        code = None
        with redirect_stdout(output):
            try:
                ex04_my_eval.main()
            except SystemExit as exc:
                code = exc.code
        return code, output.getvalue().splitlines()

    def test_fake_bot_through_lab_worker_and_week14_evaluate(self):
        self.write_mine(MY_SET)
        code, lines = self.run_main()
        self.assertIsNone(code)
        for line in (
            "평가 대상: BOT=ex04_test_bot, 문항 세트=mine (5문항)",
            "내용 검사: 오류 0건, 경고 0건",
            "[t-01] fact  점수 100.00  status=ok  실패: 없음",
            "[t-02] composite  점수 53.33  status=ok  실패: 사실 누락·불필요한 답 -26.67, 출처 누락·불필요한 출처 -20.00",
            "    질문 원광대학교가 있는 도시와 상징하는 새를 알려 주세요.",
            '    응답 {"answers": ["익산시"], "sources": ["wku-symbols"], "abstain": false}',
            "[t-03] fact  점수 0.00  status=error  실패: 실행 오류 -100.00",
            "    응답 null",
            "    오류 RuntimeError: RuntimeError: 의도한 시험 오류",
            "[t-04] fact  점수 0.00  status=ok  실패: 답할 수 있는데 거절 -100.00",
            "    질문 원광대학교의 교화는?",
            "[t-05] unknown  점수 100.00  status=ok  실패: 없음",
            "모델 준비 2회: ok, ok",
            "fact: 3문항, 평균 33.33",
            "composite: 1문항, 평균 53.33",
            "unknown: 1문항, 평균 100.00",
            "전체 5문항 평균: 50.67/100",
            "| 시간 초과 | 0 | - | 0.00 | 0.00 |",
            "| 실행 오류 | 1 | t-03 | 100.00 | 20.00 |",
            "| 답할 수 있는데 거절 | 1 | t-04 | 100.00 | 20.00 |",
            "| 사실 누락·불필요한 답 | 1 | t-02 | 26.67 | 5.33 |",
            "| 출처 누락·불필요한 출처 | 1 | t-02 | 20.00 | 4.00 |",
            "빠진 점수 합 49.33 + 전체 평균 50.67 = 100.00",
            "- 문항 세트: mine (5문항)",
            "- BOT: ex04_test_bot",
            "- 전체 평균: 50.67",
            "- 범주 평균: fact 33.33, composite 53.33, unknown 100.00",
            # 올라간 모델마다 한 줄이다. 학생은 BOT이 쓰는 모델의 줄만 기록표에 옮긴다.
            f"- 평가 뒤 올라가 있는 모델: fake-model:1b digest {DIGEST[:12]}",
            f"- 평가 뒤 올라가 있는 모델: fake-embed:latest digest {EMBED_DIGEST[:12]}",
            "- Ollama 버전: 0.0.0-test",
        ):
            with self.subTest(line=line):
                self.assertIn(line, lines)
        # 실패한 세 문항만 질문 줄이 있고, 머리 줄 다음에 질문, 응답, 오류 순서로 나온다.
        self.assertEqual(sum(line.startswith("    질문 ") for line in lines), 3)
        start = lines.index("[t-03] fact  점수 0.00  status=error  실패: 실행 오류 -100.00")
        self.assertEqual(lines[start + 1:start + 4], [
            "    질문 원광대학교의 교목은?",
            "    응답 null",
            "    오류 RuntimeError: RuntimeError: 의도한 시험 오류",
        ])
        self.assertEqual(self.server.posts, [])

    def test_bot_without_answer_fails_each_question_with_one_message(self):
        (self.folder / "ex04_no_answer_bot.py").write_text('MODEL = "qwen3.5:2b"', encoding="utf-8")
        importlib.invalidate_caches()
        self.write_mine(MY_SET[:2])
        with patch.object(ex04_my_eval, "BOT", "ex04_no_answer_bot"):
            code, lines = self.run_main()
        self.assertIsNone(code)
        # 워커가 끝나지 않고 답하므로 문항마다 같은 안내 한 줄이 오류 원인으로 남는다.
        error = ("    오류 모델 준비 실패로 문항을 실행하지 못했습니다. "
                 "RuntimeError: ex04_no_answer_bot에 answer(question) 함수가 없습니다.")
        self.assertEqual(lines.count(error), 2)
        self.assertIn("모델 준비 2회: error, error", lines)
        self.assertIn("| 실행 오류 | 2 | t-01, t-02 | 200.00 | 100.00 |", lines)
        self.assertEqual(self.server.posts, [])

    def test_lookup_failure_prints_unknown_and_keeps_scores(self):
        self.write_mine(MY_SET[:1])
        self.server.broken = True
        code, lines = self.run_main()
        self.assertIsNone(code)
        self.assertIn("전체 1문항 평균: 100.00/100", lines)
        self.assertIn("- 평가 뒤 올라가 있는 모델: 확인 못 함 (HTTPError)", lines)
        self.assertIn("- Ollama 버전: 확인 못 함 (HTTPError)", lines)

    def test_content_error_stops_before_evaluation(self):
        self.write_mine([pair("t-01", "fact", "원광대학교 기숙사 이름은?", [["새빛관"]], ["wku-dorm"])])
        with patch.object(ex04_my_eval, "evaluate") as evaluate:
            code, lines = self.run_main()
        self.assertEqual(code, 1)
        self.assertIn("  오류 [t-01] corpus에 없는 근거 문서 ID: wku-dorm", lines)
        self.assertEqual(lines[-1], "오류를 고친 뒤 다시 실행하세요. 평가는 시작하지 않았습니다.")
        evaluate.assert_not_called()

    def test_start_errors_like_week14_ex02(self):
        self.write_mine(MY_SET)
        for name, value in (("QUESTION_SET", "my"), ("BOT", "no_such_bot_for_test"), ("BOT", "rag-bot")):
            with self.subTest(**{name: value}), patch.object(ex04_my_eval, name, value):
                code, lines = self.run_main()
                self.assertEqual(code, 1)
                self.assertTrue(lines[-1].startswith("평가 시작 오류:"), lines[-1])
        (self.folder / "data" / "my_answers.json").unlink()
        code, lines = self.run_main()
        self.assertEqual(code, 1)
        self.assertTrue(lines[-1].startswith("평가 시작 오류:"), lines[-1])

    def test_public_set_skips_content_check_and_interrupt_prints_notice(self):
        calls = []

        def interrupted(questions, answers, *, worker_command, on_result):
            calls.append((len(questions), worker_command))
            raise KeyboardInterrupt

        with patch.object(ex04_my_eval, "QUESTION_SET", "public"), \
                patch.object(ex04_my_eval, "BOT", "student_bot"), \
                patch.object(ex04_my_eval, "evaluate", side_effect=interrupted):
            code, lines = self.run_main()
        self.assertIsNone(code)
        self.assertEqual(calls, [(20, None)])  # student_bot은 14주 공식 워커를 쓴다.
        self.assertFalse(any(line.startswith("내용 검사") for line in lines))
        self.assertEqual(lines[-1], "평가 중단: 워커 종료 완료. 전체 평가 점수는 산출하지 않습니다.")
        self.assertNotIn("기록할 값", lines)


if __name__ == "__main__":
    unittest.main()
