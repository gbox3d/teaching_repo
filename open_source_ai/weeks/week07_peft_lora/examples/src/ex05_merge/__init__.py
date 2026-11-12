"""어댑터를 기본 모델과 합쳐 Python과 Ollama에서 사용할 모델 폴더를 만든다."""

from peft import PeftModel

from shared import ADAPTER_DIR, MERGED_DIR, load_model


def main():
    if not (ADAPTER_DIR / "adapter_config.json").exists():
        raise SystemExit("저장한 어댑터가 없습니다. 먼저 uv run ex03으로 학습하세요.")
    if MERGED_DIR.exists():
        raise SystemExit("병합 폴더가 이미 있습니다. shared의 MERGED_DIR을 새 이름으로 바꾸세요.")
    tokenizer, base = load_model()
    model = PeftModel.from_pretrained(base, ADAPTER_DIR)
    merged = model.merge_and_unload()
    merged.save_pretrained(MERGED_DIR, safe_serialization=True)
    tokenizer.save_pretrained(MERGED_DIR)
    print(f"병합 완료: {MERGED_DIR}. uv run ex06으로 병합 모델과 대화하세요.")
