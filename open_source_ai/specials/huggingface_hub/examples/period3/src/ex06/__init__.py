"""로컬 파일도 datasets 로 연다: 구조·건수·라이선스를 보고 키워드로 찾는다. uv run ex06"""

from datasets import load_dataset
from huggingface_hub import DatasetCard

from shared import SAMPLE_CARD, SAMPLE_QA


def main() -> None:
    ds = load_dataset("json", data_files=str(SAMPLE_QA), split="train")  # Hub 데이터셋과 같은 API
    print(ds)  # 필드 이름과 건수(num_rows)
    print("필드 자료형:", ds.features)
    print("카드 license:", DatasetCard.load(SAMPLE_CARD).data.license)
    print("첫 행:", ds[0])

    print("낱말을 입력하면 question 에 그 낱말이 든 행을 찾습니다. 종료: /bye")
    while True:
        word = input("찾기> ").strip()
        if word == "/bye":
            break
        if not word:
            continue
        found = ds.filter(lambda row: word in row["question"])  # 조건에 맞는 행만 남긴 새 Dataset
        print(f"{found.num_rows}건")
        for row in found:
            print(f"  [{row['id']}] {row['question']}")
