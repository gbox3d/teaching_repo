"""저장한 어댑터를 다시 불러와 같은 모델에서 끄기·켜기를 비교한다."""

from peft import PeftModel

from shared import ADAPTER_DIR, answer, load_model, questions


def main():
    if not (ADAPTER_DIR / "adapter_config.json").exists():
        raise SystemExit("저장한 어댑터가 없습니다. 먼저 uv run ex03으로 학습하세요.")
    tokenizer, base = load_model()
    model = PeftModel.from_pretrained(base, ADAPTER_DIR).eval()
    for question in questions():
        with model.disable_adapter():
            print("학습 전>", answer(model, tokenizer, question))
        print("학습 후>", answer(model, tokenizer, question))
