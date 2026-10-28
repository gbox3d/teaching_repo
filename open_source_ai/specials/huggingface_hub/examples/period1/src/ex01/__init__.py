"""Hub 저장소 정보 읽기: uv run ex01"""

from huggingface_hub import HfApi
from huggingface_hub.errors import HfHubHTTPError, HFValidationError

api = HfApi()


def main() -> None:
    print("모델 ID를 입력하면 Hub의 정보를 보여 줍니다. 예: Qwen/Qwen2.5-0.5B-Instruct  종료: /bye")
    while True:
        repo_id = input("모델> ").strip()
        if repo_id == "/bye":
            break
        if not repo_id:
            continue
        try:
            info = api.model_info(repo_id, files_metadata=True)  # 파일 목록과 크기까지 받는다
        except (HfHubHTTPError, HFValidationError) as error:  # 없는 이름·잘못된 형식
            print("Hub 오류:", str(error).splitlines()[0])  # 라이브러리 메시지의 첫 줄에 이유가 있다
            continue
        size = sum(f.size or 0 for f in info.siblings)
        print("라이선스 :", info.card_data.license if info.card_data else "카드에 없음")
        print("task     :", info.pipeline_tag)
        print("gated    :", info.gated)  # False 가 아니면 약관 동의가 필요하다
        print("commit   :", info.sha)  # 지금 main 이 가리키는 commit hash
        print(f"파일 {len(info.siblings)}개, 합계 {size / 1e9:.2f} GB")
