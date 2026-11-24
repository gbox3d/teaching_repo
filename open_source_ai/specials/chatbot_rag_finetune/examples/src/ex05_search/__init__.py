"""2교시: 정답의 근거 문서가 검색 결과에 들었는지 문항 세트 전체에서 본다. 답변은 만들지 않는다.
생성 모델은 필요 없고, rag_bot의 임베딩 검색에는 Ollama의 bge-m3가 필요하다."""

import importlib

from lab_shared import load_set
from shared import configure_utf8
from shared.evaluation import validate_dataset

BOTS = ("student_bot", "rag_bot")  # retrieve(question)가 있는 봇 모듈 이름
SETS = ("mine", "public")  # 내 평가 문항, 14주차 공개 20문항


def settings(bot) -> str:
    names = ("EMBED_MODEL", "TOP_K", "MIN_SCORE")
    return " ".join(f"{name}={getattr(bot, name)}" for name in names if hasattr(bot, name))


def main() -> None:
    configure_utf8()
    bots = {name: importlib.import_module(name) for name in BOTS}
    for name, bot in bots.items():
        print(f"{name}: {settings(bot)}")
    for set_name in SETS:
        try:
            questions, answers = load_set(set_name)
        except FileNotFoundError as exc:
            raise SystemExit(f"문항 파일이 없습니다: {exc.filename}. "
                             f"lab_shared/data에 파일을 두거나 SETS에서 {set_name!r}를 빼세요.") from exc
        gold = validate_dataset(questions, answers)
        found = {name: 0 for name in bots}
        unknown_docs = {name: 0 for name in bots}
        known = sum(1 for question in questions if not gold[question["id"]]["abstain"])
        print(f"\n== {set_name}: {len(questions)}문항(정답 있는 문항 {known}개)")
        for question in questions:
            item = gold[question["id"]]
            # 문서 하나가 여러 사실의 근거이면 한 번만 센다.
            needed = list(dict.fromkeys(item.get("fact_sources") or item["sources"]))
            parts = []
            for name, bot in bots.items():
                ids = [doc["id"] for doc in bot.retrieve(question["question"])]
                missing = [doc_id for doc_id in needed if doc_id not in ids]
                # 임베딩 봇은 가장 가까운 문서의 코사인 유사도를 함께 보여 MIN_SCORE를 정하는 데 쓴다.
                top = f"(최고 유사도 {bot.rank(question['question'])[0][0]:.3f})" if hasattr(bot, "rank") else ""
                if item["abstain"]:
                    unknown_docs[name] += len(ids)
                    parts.append(f"{name} 보낸 문서 {len(ids)}개{top}")
                elif missing:
                    parts.append(f"{name} 놓침 {', '.join(missing)}{top}")
                else:
                    found[name] += 1
                    parts.append(f"{name} 포함{top}")
            label = ", ".join(needed) if needed else "없음(답변 불가)"
            print(f"[{question['id']}] {question['category']} 근거 {label}")
            print("    " + " | ".join(parts))
        unknown = len(questions) - known
        for name in bots:
            line = f"{name}: 근거 문서를 모두 찾은 문항 {found[name]}/{known}"
            if unknown:
                line += f", 답변 불가 문항에 보낸 문서 평균 {unknown_docs[name] / unknown:.1f}개"
            print(line)
