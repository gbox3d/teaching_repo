"""2교시 예제들이 함께 쓰는 설정. ex04·ex05 가 `from shared import ...` 로 가져다 쓴다."""

import torch

# 모델 ID 와 revision 을 한곳에 둔다. revision 을 commit hash 로 바꾸면 모든 예제가 그 버전을 쓴다.
CLS_MODEL = "lxyuan/distilbert-base-multilingual-cased-sentiments-student"
CLS_REVISION = "main"
TEXT_MODEL = "Qwen/Qwen2.5-0.5B-Instruct"
TEXT_REVISION = "main"


def pick_device() -> str:
    """쓸 수 있는 가장 빠른 장치. CPU 와 비교하려면 예제에서 DEVICE = "cpu" 로 바꾼다."""
    if torch.cuda.is_available():  # NVIDIA GPU
        return "cuda"
    if torch.backends.mps.is_available():  # Apple 실리콘 Mac
        return "mps"
    return "cpu"
