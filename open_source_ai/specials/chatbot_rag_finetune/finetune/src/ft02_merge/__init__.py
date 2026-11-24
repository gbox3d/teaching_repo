"""어댑터를 기본 모델과 합쳐 GGUF 변환에 쓸 모델 폴더를 만든다. 7주차 ex05와 같다."""

from peft import PeftModel

from shared import ADAPTER_DIR, MERGED_DIR, load_model


def main():
    if not (ADAPTER_DIR / "adapter_config.json").exists():
        raise SystemExit("저장한 어댑터가 없습니다. 먼저 uv run ft01로 학습하세요.")
    if MERGED_DIR.exists():
        raise SystemExit("병합 폴더가 이미 있습니다. shared의 MERGED_DIR을 새 이름으로 바꾸세요.")
    # 병합은 float32로 한다. 학습을 bf16으로 했어도 어댑터 가중치는 기본 모델에 그대로 더해진다.
    tokenizer, base = load_model()
    merged = PeftModel.from_pretrained(base, ADAPTER_DIR).merge_and_unload()
    merged.save_pretrained(MERGED_DIR, safe_serialization=True)
    tokenizer.save_pretrained(MERGED_DIR)
    print(f"병합 완료: {MERGED_DIR}. walkthrough의 GGUF 변환과 Ollama 등록을 이어서 하세요.")
