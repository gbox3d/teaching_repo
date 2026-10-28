"""감성 분류: model·revision·device 를 적어 pipeline 을 만든다. uv run ex04"""

import time

from transformers import pipeline

from shared import CLS_MODEL, CLS_REVISION, pick_device

DEVICE = pick_device()  # CPU 와 비교할 때는 "cpu" 로 바꾼다


def main() -> None:
    start = time.perf_counter()
    classify = pipeline("text-classification", model=CLS_MODEL, revision=CLS_REVISION, device=DEVICE)
    print(f"로드 {time.perf_counter() - start:.1f}초  device={DEVICE}")
    print("문장을 입력하면 긍정·중립·부정과 점수를 보여 줍니다. 종료: /bye")
    while True:
        text = input("문장> ").strip()
        if text == "/bye":
            break
        if not text:
            continue
        start = time.perf_counter()
        result = classify(text)[0]  # [{'label': 'positive', 'score': 0.97}]
        print(f"{result['label']}  {result['score']:.3f}  ({time.perf_counter() - start:.2f}초)")
