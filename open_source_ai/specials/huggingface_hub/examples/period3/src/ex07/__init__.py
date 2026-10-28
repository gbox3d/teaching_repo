"""Hub 데이터셋을 스트리밍으로 앞부분만 본다. 카드의 license 도 함께. uv run ex07"""

from itertools import islice

from datasets import load_dataset
from huggingface_hub import DatasetCard
from huggingface_hub.errors import HfHubHTTPError

from shared import HUB_CONFIG, HUB_DATASET


def main() -> None:
    print(f"'데이터셋ID 구성' 을 입력하면 카드 license 와 앞 3행을 보여 줍니다. 빈 줄은 {HUB_DATASET} {HUB_CONFIG}. 종료: /bye")
    while True:
        text = input("데이터셋> ").strip()
        if text == "/bye":
            break
        repo_id, config = (text.split() + [None])[:2] if text else (HUB_DATASET, HUB_CONFIG)
        try:
            card = DatasetCard.load(repo_id)  # 카드(README.md)만 받는다
            print("카드 license:", card.data.license)
            # streaming=True: 전부 내려받지 않고 앞에서부터 한 행씩 흘려 받는다
            ds = load_dataset(repo_id, config, split="train", streaming=True)
            for row in islice(ds, 3):
                print(" ", row)
        except (HfHubHTTPError, ValueError, FileNotFoundError) as error:
            print("오류:", " ".join(str(error).splitlines()[:2]))  # 구성이 빠지면 둘째 줄에 고를 수 있는 이름이 있다
