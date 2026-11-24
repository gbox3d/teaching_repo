"""3교시 준비: 학습 문항마다 rag_bot이 실제로 보낼 대화를 만들고 정답 JSON을 붙여 학습 파일로 저장한다.
학습과 추론의 입력이 같아야 하므로 검색과 메시지는 rag_bot의 retrieve·messages를 그대로 쓴다."""

import json
from pathlib import Path

import rag_bot
from lab_shared import load_set
from shared import configure_utf8, normalize
from shared.evaluation import validate_dataset

# 특강 폴더의 outputs/sft/. finetune/ 프로젝트의 학습 명령이 이 위치를 읽는다.
OUTPUT_DIR = Path(__file__).resolve().parents[3] / "outputs" / "sft"


def target(item: dict) -> str:
    """사실마다 첫 번째 허용 표현을 답으로 쓰고, 근거 문서는 나온 순서대로 한 번씩 적는다."""
    return json.dumps({
        "answers": [group[0] for group in item["expected"]],
        "sources": list(dict.fromkeys(item.get("fact_sources", []))),
        "abstain": item["abstain"],
    }, ensure_ascii=False)


def main() -> None:
    configure_utf8()
    try:
        questions, answers = load_set("train")
        evaluation_sets = {name: load_set(name)[0] for name in ("public", "mine")}
    except FileNotFoundError as exc:
        raise SystemExit(f"문항 파일이 없습니다: {exc.filename}. lab_shared/data의 파일 이름과 위치를 확인하세요.") from exc
    gold = validate_dataset(questions, answers)
    missing_sources = [q["id"] for q in questions if not gold[q["id"]]["abstain"] and "fact_sources" not in gold[q["id"]]]
    if missing_sources:
        raise SystemExit(f"fact_sources가 없는 학습 문항: {', '.join(missing_sources)}. 사실마다 근거 문서 ID를 적으세요.")
    # 평가 문항을 학습에 넣으면 점수가 부풀어 개선 여부를 판단할 수 없다. 걸린 문항을 모두 보여 주고 멈춘다.
    evaluation = {}
    for set_name, set_questions in evaluation_sets.items():
        for question in set_questions:
            evaluation[normalize(question["question"])] = f"{set_name}:{question['id']}"
    overlaps = [f"{q['id']} = {evaluation[normalize(q['question'])]}" for q in questions
                if normalize(q["question"]) in evaluation]
    if overlaps:
        print("평가 문항과 같은 학습 문항이 있습니다. 학습 문항을 바꾼 뒤 다시 실행하세요.")
        for line in overlaps:
            print("  " + line)
        raise SystemExit(1)
    rows, skipped = [], []
    print(f"rag_bot 검색 설정: EMBED_MODEL={rag_bot.EMBED_MODEL} TOP_K={rag_bot.TOP_K} MIN_SCORE={rag_bot.MIN_SCORE}")
    for question in questions:
        item = gold[question["id"]]
        documents = rag_bot.retrieve(question["question"])
        if not documents:
            # 보낼 문서가 없으면 rag_bot은 모델을 부르지 않고 보류하므로 학습할 대화가 없다.
            skipped.append(f"{question['id']}: MIN_SCORE를 넘는 문서 없음")
            continue
        missing = [doc_id for doc_id in item.get("fact_sources", []) if doc_id not in {d["id"] for d in documents}]
        if missing:
            # 근거 문서가 빠진 대화로 정답을 가르치면 문서에 없는 답을 지어내도록 학습된다.
            skipped.append(f"{question['id']}: 검색 결과에 {', '.join(dict.fromkeys(missing))} 없음")
            continue
        messages = rag_bot.messages(question["question"], documents)
        rows.append({"messages": messages + [{"role": "assistant", "content": target(item)}]})
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "train.jsonl").write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows), encoding="utf-8")
    # 학습 데이터를 만든 때의 검색 설정. rag_bot 상수를 바꾸면 이 명령과 학습을 다시 실행한다.
    (OUTPUT_DIR / "settings.json").write_text(json.dumps({
        "EMBED_MODEL": rag_bot.EMBED_MODEL, "TOP_K": rag_bot.TOP_K, "MIN_SCORE": rag_bot.MIN_SCORE,
        "examples": len(rows), "skipped": len(skipped),
    }, ensure_ascii=False, indent=1), encoding="utf-8")
    for line in skipped:
        print("제외", line)
    print(f"학습 예시 {len(rows)}건 저장, 제외 {len(skipped)}건: {OUTPUT_DIR / 'train.jsonl'}")
