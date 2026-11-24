"""lab_shared/data의 내 평가·학습 문항 예시를 검사한다. Ollama가 필요 없다."""

import difflib
import json
import unicodedata
import unittest
from pathlib import Path

from shared import DATA_DIR, normalize
from shared.evaluation import score_response, validate_dataset

# lab_shared 패키지를 import하지 않고 이 파일 위치에서 자료 폴더를 찾는다.
MY_DATA_DIR = Path(__file__).resolve().parents[1] / "src" / "lab_shared" / "data"
SETS = ("my", "train")  # 파일 이름 앞부분(my_questions.json, my_answers.json 등)
# 문항 수를 바꾸면 아래 값도 고친다.
MY_COUNTS = {"fact": 12, "composite": 4, "unknown": 4}
TRAIN_TOTAL = 40
TRAIN_UNKNOWN_MIN, TRAIN_UNKNOWN_MAX = 10, 12
# 공개 문항과 문장 유사도(normalize 뒤 difflib 비율)가 이 값 이상이면 공개 문장을 조금만 바꾼 질문으로 본다.
SIMILARITY_LIMIT = 0.85


def read_json(path: Path) -> list:
    """JSON 파일을 읽는다. 읽지 못하면 어느 파일인지 메시지에 넣는다."""
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except ValueError as exc:  # JSON 문법 오류, BOM, UTF-8이 아닌 인코딩이 모두 ValueError다.
        raise ValueError(f"{path.name} 파일을 JSON으로 읽지 못했습니다. 쉼표·따옴표와 "
                         f"저장 인코딩(BOM 없는 UTF-8)을 확인하세요. {exc}") from exc


def squash(text: str) -> str:
    """NFKC·casefold 뒤 공백을 모두 지운다. 별칭이 문서 본문에 있는지 볼 때 쓴다."""
    return "".join(unicodedata.normalize("NFKC", text).casefold().split())


def unpaired_ids(questions: list, answers: list) -> str:
    """질문과 정답 가운데 짝이 없는 id를 적는다. 짝이 모두 맞으면 빈 문자열이다."""
    question_ids = {str(item.get("id")) for item in questions}
    answer_ids = {str(item.get("id")) for item in answers}
    notes = [f"{label} id: {', '.join(sorted(ids))}."
             for label, ids in (("정답이 없는 질문", question_ids - answer_ids),
                                ("질문이 없는 정답", answer_ids - question_ids)) if ids]
    return " ".join(notes)


class MyDataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.questions = {name: read_json(MY_DATA_DIR / f"{name}_questions.json") for name in SETS}
        cls.answers = {name: read_json(MY_DATA_DIR / f"{name}_answers.json") for name in SETS}
        cls.corpus = {doc["id"]: squash(doc["text"]) for doc in read_json(DATA_DIR / "corpus.json")}
        cls.public = {normalize(question["question"]): question["id"]
                      for question in read_json(DATA_DIR / "public_questions.json")}

    def known_items(self):
        for name in SETS:
            yield from (item for item in self.answers[name] if not item["abstain"])

    def test_validate_dataset(self):
        """14주 채점기의 형식 검사를 통과한다. 문항마다 먼저 돌려 오류가 난 문항 id를 보인다."""
        for name in SETS:
            questions, answers = self.questions[name], self.answers[name]
            checks = [(question.get("id"), [question],
                       [item for item in answers if item.get("id") == question.get("id")])
                      for question in questions]
            checks.append((f"{name} 전체", questions, answers))  # id 중복·누락은 전체에서 본다.
            for label, part_questions, part_answers in checks:
                with self.subTest(item_id=label):
                    try:
                        validate_dataset(part_questions, part_answers)
                    except ValueError as exc:
                        self.fail(f"{label}: {exc} {unpaired_ids(part_questions, part_answers)}".rstrip())

    def test_known_items_cite_corpus_documents(self):
        """답이 있는 문항은 사실마다 근거 문서 ID가 있고, 그 문서가 참고 자료에 있다."""
        for item in self.known_items():
            with self.subTest(item_id=item["id"]):
                self.assertIn("fact_sources", item, f"{item['id']}: fact_sources가 없습니다.")
                self.assertEqual(len(item["fact_sources"]), len(item["expected"]),
                                 f"{item['id']}: fact_sources에는 사실마다 문서 ID가 하나씩 필요합니다.")
                for doc_id in item["fact_sources"]:
                    self.assertIn(doc_id, self.corpus, f"{item['id']}: 참고 자료에 없는 문서 ID {doc_id}")

    def test_aliases_come_from_source_text(self):
        """별칭 하나 이상이 근거 문서 본문에 있다. ex06이 학습 답으로 쓰는 첫 별칭도 본문에 있어야 한다."""
        for item in self.known_items():
            for number, (group, doc_id) in enumerate(zip(item["expected"], item.get("fact_sources", [])), 1):
                text = self.corpus.get(doc_id, "")
                found = [alias for alias in group if squash(alias) in text]
                with self.subTest(item_id=item["id"], fact=number):
                    self.assertTrue(found, f"{item['id']} 사실 {number}: 별칭이 하나도 {doc_id} 본문에 없습니다. "
                                           "근거 문서와 표기를 확인하세요.")
                    self.assertTrue(squash(group[0]) in text,
                                    f"{item['id']} 사실 {number}: 첫 별칭이 본문 표기가 아닙니다"
                                    f"(첫 별칭 {group[0]!r}, 본문에 있는 별칭 {found[0]!r}).")

    def test_no_public_question(self):
        """공개 20문항과 같은 질문(14주 normalize 기준)이 없다."""
        for name in SETS:
            for question in self.questions[name]:
                public_id = self.public.get(normalize(question["question"]))
                with self.subTest(item_id=question["id"]):
                    self.assertIsNone(public_id, f"{question['id']}: 공개 문항 {public_id}의 질문과 같습니다.")

    def test_no_question_close_to_public(self):
        """공개 20문항과 문장 유사도(14주 normalize 뒤 difflib 비율)가 SIMILARITY_LIMIT보다 낮다."""
        for name in SETS:
            for question in self.questions[name]:
                text = normalize(question["question"])
                ratio, public_id = max((difflib.SequenceMatcher(None, text, public).ratio(), public_id)
                                       for public, public_id in self.public.items())
                with self.subTest(item_id=question["id"]):
                    self.assertLess(ratio, SIMILARITY_LIMIT,
                                    f"{question['id']}: 공개 문항({public_id})과 문장 유사도가 {ratio:.2f}입니다. "
                                    "조사·어순·낱말 몇 개만 바꾸지 말고 문장을 새로 쓰세요.")

    def test_no_question_shared_between_my_and_train(self):
        """내 평가와 학습 사이, 그리고 한 파일 안에 같은 질문(14주 normalize 기준)이 없다."""
        seen = {}
        for name in SETS:
            for question in self.questions[name]:
                key = normalize(question["question"])
                with self.subTest(item_id=question["id"]):
                    self.assertIsNone(seen.get(key), f"{question['id']}: {seen.get(key)}의 질문과 같습니다.")
                seen.setdefault(key, question["id"])

    def test_counts_and_categories(self):
        """내 평가는 범주별 문항 수, 학습은 전체 문항 수와 unknown 문항 수가 정한 값과 같다."""
        by_category = {}
        for question in self.questions["my"]:
            by_category.setdefault(question["category"], []).append(question["id"])
        counts = {category: len(ids) for category, ids in by_category.items()}
        self.assertEqual(counts, MY_COUNTS, f"내 평가 범주별 문항: {by_category}. "
                                            "문항 수를 바꿨다면 이 파일 맨 위의 MY_COUNTS를 고치세요.")
        train = self.questions["train"]
        unknown = [question["id"] for question in train if question["category"] == "unknown"]
        self.assertEqual(len(train), TRAIN_TOTAL, f"학습 문항 수가 {len(train)}개입니다. "
                                                  "문항 수를 바꿨다면 TRAIN_TOTAL을 고치세요.")
        self.assertTrue(TRAIN_UNKNOWN_MIN <= len(unknown) <= TRAIN_UNKNOWN_MAX,
                        f"학습 unknown 문항이 {len(unknown)}개입니다: {unknown}. "
                        "문항 수를 바꿨다면 TRAIN_UNKNOWN_MIN, TRAIN_UNKNOWN_MAX를 고치세요.")

    def test_unknown_answers_are_empty(self):
        """unknown 문항의 정답은 abstain이 true이고 세 배열이 모두 비어 있다."""
        for name in SETS:
            gold = {item["id"]: item for item in self.answers[name]}
            for question in self.questions[name]:
                if question["category"] != "unknown":
                    continue
                item = gold.get(question["id"], {})
                with self.subTest(item_id=question["id"]):
                    self.assertIs(item.get("abstain"), True, f"{question['id']}: abstain이 true가 아닙니다.")
                    for key in ("expected", "sources", "fact_sources"):
                        self.assertEqual(item.get(key, []), [], f"{question['id']}: {key}가 비어 있지 않습니다.")

    def test_first_alias_answer_scores_100(self):
        """ex06처럼 첫 별칭과 fact_sources로 만든 답이 14주 채점기에서 100점이다."""
        for name in SETS:
            for item in self.answers[name]:
                target = {"answers": [group[0] for group in item["expected"]],
                          "sources": list(dict.fromkeys(item.get("fact_sources", []))),
                          "abstain": item["abstain"]}
                with self.subTest(item_id=item["id"]):
                    score = score_response(target, item)["score"]
                    self.assertEqual(score, 100, f"{item['id']}: 첫 별칭과 fact_sources로 만든 답이 "
                                                 f"{score:.2f}점입니다. 사실끼리 겹치는 별칭과 fact_sources를 확인하세요.")


if __name__ == "__main__":
    unittest.main()
