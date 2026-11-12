"""저장한 병합 모델을 Python에서 직접 불러와 대화한다."""

from shared import MERGED_DIR, answer, load_model, questions


def main():
    if not (MERGED_DIR / "config.json").is_file():
        raise SystemExit("병합 모델이 없습니다. 먼저 uv run ex05로 저장하세요.")
    tokenizer, model = load_model(MERGED_DIR)
    for question in questions():
        print("AI>", answer(model, tokenizer, question))
