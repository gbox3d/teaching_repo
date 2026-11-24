"""Ollama 없이 rag_bot, ex05 검색 관찰, ex06 학습 예시 만들기, 명령 이름 규칙을 확인한다."""

import contextlib
import importlib
import io
import json
import sys
import tempfile
import tomllib
import types
import unittest
from pathlib import Path
from unittest.mock import patch

import ex05_search
import ex06_make_sft
import lab_shared
import rag_bot
import shared

CORPUS = json.loads((shared.DATA_DIR / "corpus.json").read_text(encoding="utf-8"))
DOCS = {doc["id"]: doc for doc in CORPUS}
WORDS = ("교화", "익산", "1946", "홈페이지")


def fake_embed(texts):
    """낱말이 들어 있으면 1인 작은 벡터. 코사인 순위를 손으로 예상할 수 있다."""
    return [[1.0 if word in text else 0.0 for word in WORDS] + [0.01] for text in texts]


def write_set(folder, name, questions, answers):
    questions_file, answers_file = lab_shared.SETS[name]
    (folder / questions_file).write_text(json.dumps(questions, ensure_ascii=False), encoding="utf-8")
    (folder / answers_file).write_text(json.dumps(answers, ensure_ascii=False), encoding="utf-8")


def known(item_id, question, expected, fact_sources, category="fact"):
    q = {"id": item_id, "category": category, "question": question}
    a = {"id": item_id, "expected": expected, "fact_sources": fact_sources,
         "sources": list(dict.fromkeys(fact_sources)), "abstain": False}
    return q, a


def unknown(item_id, question):
    return ({"id": item_id, "category": "unknown", "question": question},
            {"id": item_id, "expected": [], "fact_sources": [], "sources": [], "abstain": True})


class RagBotTests(unittest.TestCase):
    def setUp(self):
        rag_bot.index = None
        self.addCleanup(setattr, rag_bot, "index", None)

    def test_import_does_not_embed_and_urls_are_local(self):
        with patch("urllib.request.OpenerDirector.open", side_effect=AssertionError("import 때 요청")):
            importlib.reload(rag_bot)
        self.assertIsNone(rag_bot.index)
        self.assertTrue(rag_bot.CHAT_URL.startswith("http://127.0.0.1:11434/"))
        self.assertTrue(rag_bot.EMBED_URL.startswith("http://127.0.0.1:11434/"))

    def test_rank_orders_by_cosine_and_builds_index_once(self):
        with patch.object(rag_bot, "embed", side_effect=fake_embed) as embed:
            first = rag_bot.rank("교화 이름")
            second = rag_bot.rank("익산")
        self.assertEqual(first[0][1]["id"], "wku-symbols")
        self.assertEqual(second[0][1]["id"], "wku-location")
        self.assertEqual(len(first), len(CORPUS))
        # 문서 색인 1번 + 질문 2번. 문서는 다시 임베딩하지 않는다.
        self.assertEqual(embed.call_count, 3)

    def test_retrieve_applies_top_k_and_min_score(self):
        ranked = [(0.9, DOCS["wku-symbols"]), (0.6, DOCS["wku-values"]), (0.3, DOCS["wku-location"])]
        with patch.object(rag_bot, "rank", return_value=ranked), patch.object(rag_bot, "TOP_K", 2):
            self.assertEqual([d["id"] for d in rag_bot.retrieve("q")], ["wku-symbols", "wku-values"])
            with patch.object(rag_bot, "MIN_SCORE", 0.7):
                self.assertEqual([d["id"] for d in rag_bot.retrieve("q")], ["wku-symbols"])

    def test_answer_request_body_and_responses(self):
        with patch.object(rag_bot, "retrieve", return_value=[]), patch.object(rag_bot, "post") as post:
            self.assertEqual(rag_bot.answer("q"), {"answers": [], "sources": [], "abstain": True})
            post.assert_not_called()
        doc = dict(DOCS["wku-symbols"], score=0.9)
        reply = {"message": {"content": '{"answers": ["백목련"], "sources": ["wku-symbols"], "abstain": false}'}}
        with patch.object(rag_bot, "retrieve", return_value=[doc]), \
                patch.object(rag_bot, "post", return_value=reply) as post:
            self.assertEqual(rag_bot.answer("교화"), json.loads(reply["message"]["content"]))
        url, body = post.call_args.args
        self.assertEqual(url, rag_bot.CHAT_URL)
        self.assertEqual((body["model"], body["stream"], body["think"]), (rag_bot.MODEL, False, False))
        self.assertEqual(body["options"], {"temperature": 0, "num_predict": 512})
        self.assertEqual(body["messages"][0], {"role": "system", "content": rag_bot.SYSTEM_PROMPT})
        user = json.loads(body["messages"][1]["content"])
        self.assertEqual(user["question"], "교화")
        self.assertEqual(set(user["documents"][0]), {"id", "title", "text"})
        with patch.object(rag_bot, "retrieve", return_value=[doc]), \
                patch.object(rag_bot, "post", return_value={"message": {"content": "형식 아님"}}):
            self.assertEqual(rag_bot.answer("교화"), "형식 아님")

    def test_post_skips_proxies(self):
        class Opener:
            def open(self, request, timeout):
                return io.BytesIO(b'{"embeddings": [[1.0]]}')

        with patch.object(rag_bot, "build_opener", return_value=Opener()) as build:
            self.assertEqual(rag_bot.embed(["x"]), [[1.0]])
        handler = build.call_args.args[0]
        self.assertEqual(handler.proxies, {})


class Ex06Tests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.folder = Path(temp.name)
        self.output = self.folder / "out"
        for target, value in ((lab_shared, self.folder), (ex06_make_sft, self.output)):
            patcher = patch.object(target, "DATA_DIR" if target is lab_shared else "OUTPUT_DIR", value)
            patcher.start()
            self.addCleanup(patcher.stop)
        write_set(self.folder, "mine", *zip(known("mine-01", "원광대학교 교화는?", [["백목련"]], ["wku-symbols"])))

    def run_main(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            ex06_make_sft.main()
        return stdout.getvalue()

    def test_writes_rag_messages_targets_and_settings(self):
        items = [
            known("train-01", "원광대학교 교육목표 세 가지는?", [["학술탐구"], ["덕성함양"], ["사회봉사", "봉사"]],
                  ["wku-values"] * 3),
            known("train-02", "원광대학 설립 연도와 홈페이지 주소는?", [["1953", "1953년"], ["https://www.wku.ac.kr/"]],
                  ["wku-history", "wku-services"], "composite"),
            known("train-03", "석사과정 설치 연도는?", [["1967"]], ["wku-history"]),
            unknown("train-04", "원광대학교 총장 이름은?"),
            unknown("train-05", "원광대학교 등록금은?"),
        ]
        write_set(self.folder, "train", *zip(*items))
        found = {"train-01": ["wku-values"], "train-02": ["wku-history", "wku-services"],
                 "train-03": ["wku-location"], "train-04": ["wku-services"], "train-05": []}
        questions = {q["question"]: q["id"] for q, _ in items}
        with patch.object(rag_bot, "retrieve", side_effect=lambda q: [DOCS[i] for i in found[questions[q]]]):
            output = self.run_main()
        rows = [json.loads(line) for line in (self.output / "train.jsonl").read_text(encoding="utf-8").splitlines()]
        self.assertEqual(len(rows), 3)
        # 근거 문서를 놓친 문항과 보낼 문서가 없는 문항은 이유와 함께 제외한다.
        self.assertIn("train-03: 검색 결과에 wku-history 없음", output)
        self.assertIn("train-05: MIN_SCORE를 넘는 문서 없음", output)
        first = rows[0]["messages"]
        self.assertEqual(first[:2], rag_bot.messages("원광대학교 교육목표 세 가지는?", [DOCS["wku-values"]]))
        self.assertEqual(json.loads(first[2]["content"]),
                         {"answers": ["학술탐구", "덕성함양", "사회봉사"], "sources": ["wku-values"], "abstain": False})
        self.assertEqual(json.loads(rows[1]["messages"][2]["content"])["sources"], ["wku-history", "wku-services"])
        self.assertEqual(rows[2]["messages"][2]["content"], '{"answers": [], "sources": [], "abstain": true}')
        settings = json.loads((self.output / "settings.json").read_text(encoding="utf-8"))
        self.assertEqual((settings["TOP_K"], settings["examples"], settings["skipped"]), (rag_bot.TOP_K, 3, 2))

    def test_stops_with_every_question_that_repeats_an_evaluation_question(self):
        public_question = json.loads((shared.DATA_DIR / "public_questions.json").read_text(encoding="utf-8"))[6]
        items = [known("train-01", " " + public_question["question"].replace(" ", "  "), [["은행나무"]], ["wku-symbols"]),
                 known("train-02", "원광대학교 교화는?", [["백목련"]], ["wku-symbols"]),
                 known("train-03", "원광초급대학 설립 연도는?", [["1951"]], ["wku-history"])]
        write_set(self.folder, "train", *zip(*items))
        with patch.object(rag_bot, "retrieve", side_effect=AssertionError("검사 전에 검색함")), \
                self.assertRaises(SystemExit):
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                ex06_make_sft.main()
        self.assertIn(f"train-01 = public:{public_question['id']}", output.getvalue())
        self.assertIn("train-02 = mine:mine-01", output.getvalue())
        self.assertFalse((self.output / "train.jsonl").exists())


class MissingFileTests(unittest.TestCase):
    """학생이 문항 파일을 지우거나 옮겼을 때 OSError 대신 파일 이름을 알려 주고 멈춘다."""

    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        patcher = patch.object(lab_shared, "DATA_DIR", Path(temp.name))
        patcher.start()
        self.addCleanup(patcher.stop)

    def test_ex05_names_the_missing_file(self):
        with patch.object(ex05_search, "BOTS", ()), patch.object(ex05_search, "SETS", ("mine",)), \
                self.assertRaises(SystemExit) as stop:
            ex05_search.main()
        self.assertIn("my_questions.json", str(stop.exception.code))

    def test_ex06_names_the_missing_file(self):
        with self.assertRaises(SystemExit) as stop:
            ex06_make_sft.main()
        self.assertIn("train_questions.json", str(stop.exception.code))


class Ex05Tests(unittest.TestCase):
    def test_counts_questions_whose_evidence_was_retrieved(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        items = [known("mine-01", "교화", [["백목련"]], ["wku-symbols"]),
                 known("mine-02", "도시와 교화", [["익산시"], ["백목련"]], ["wku-location", "wku-symbols"], "composite"),
                 unknown("mine-03", "총장")]
        write_set(Path(temp.name), "mine", *zip(*items))
        bot = types.ModuleType("fake_search_bot")
        bot.TOP_K = 1
        bot.retrieve = lambda question: [DOCS["wku-symbols"]]
        stdout = io.StringIO()
        with patch.dict(sys.modules, {"fake_search_bot": bot}), patch.object(lab_shared, "DATA_DIR", Path(temp.name)), \
                patch.object(ex05_search, "BOTS", ("fake_search_bot",)), patch.object(ex05_search, "SETS", ("mine",)), \
                contextlib.redirect_stdout(stdout):
            ex05_search.main()
        output = stdout.getvalue()
        self.assertIn("fake_search_bot: TOP_K=1", output)
        self.assertIn("fake_search_bot 놓침 wku-location", output)
        self.assertIn("근거 문서를 모두 찾은 문항 1/2", output)
        self.assertIn("답변 불가 문항에 보낸 문서 평균 1.0개", output)


class ProjectTests(unittest.TestCase):
    def test_command_names_do_not_shadow_week14_and_packages_exist(self):
        special_root = Path(rag_bot.__file__).resolve().parents[2]
        week14_root = Path(shared.__file__).resolve().parents[2]
        special = tomllib.loads((special_root / "pyproject.toml").read_text(encoding="utf-8"))
        week14 = tomllib.loads((week14_root / "pyproject.toml").read_text(encoding="utf-8"))
        special_scripts = set(special["project"].get("scripts", {}))
        # 같은 가상 환경에 두 프로젝트의 명령이 함께 설치된다. 이름이 겹치면 한쪽 명령이 가려진다.
        self.assertFalse(special_scripts & set(week14["project"]["scripts"]))
        for module in special["tool"]["uv"]["build-backend"]["module-name"]:
            self.assertTrue((special_root / "src" / module / "__init__.py").exists(), module)


if __name__ == "__main__":
    unittest.main()
