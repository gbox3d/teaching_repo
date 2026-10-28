"""모델 카드 읽기: uv run ex02"""

from huggingface_hub import ModelCard
from huggingface_hub.errors import HfHubHTTPError, HFValidationError


def main() -> None:
    print("모델 ID를 입력하면 카드의 YAML과 본문 절 제목을 보여 줍니다. 종료: /bye")
    while True:
        repo_id = input("모델> ").strip()
        if repo_id == "/bye":
            break
        if not repo_id:
            continue
        try:
            card = ModelCard.load(repo_id)  # 저장소의 README.md 가 모델 카드다
        except (HfHubHTTPError, HFValidationError) as error:  # 없는 이름·잘못된 형식
            print("Hub 오류:", str(error).splitlines()[0])
            continue
        print("[YAML 메타데이터]")
        for key, value in card.data.to_dict().items():
            text = " ".join(str(value).split())  # 약관처럼 긴 값은 한 줄로 줄여 앞부분만
            print(f"  {key}: {text[:80]}{'…' if len(text) > 80 else ''}")
        print("[본문 절 제목]")
        for line in card.text.splitlines():
            if line.startswith("#"):
                print(" ", line)
