"""텐서·학습 실습에 필요한 난수·장치·시간 측정 도우미. 모델 다운로드와 기록 클래스는 없다."""
from __future__ import annotations
import random
import numpy as np
import torch

def set_seed(seed: int) -> None:
    """Python·NumPy·PyTorch 난수를 한 번에 고정한다. GPU 연산은 완전 결정론이 아닐 수 있다."""
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)

def pick_device(name: str = "auto") -> torch.device:
    """'auto'면 CUDA가 있을 때 cuda, 아니면 cpu. cuda를 요청했는데 없으면 사람이 읽을 메시지로 종료한다."""
    if name == "auto":
        return torch.device("cuda" if torch.cuda.is_available() else "cpu")
    if name.startswith("cuda") and not torch.cuda.is_available():
        raise SystemExit(
            "CUDA 장치를 요청했지만 torch.cuda.is_available()가 False다. "
            "드라이버·torch 휠(CUDA 인덱스)을 확인하거나 --device cpu로 다시 실행한다."
        )
    return torch.device(name)

def gpu_name(device: torch.device) -> str | None:
    if device.type != "cuda":
        return None
    return torch.cuda.get_device_name(device)

def sync(device: torch.device) -> None:
    """GPU 연산은 비동기이므로 시간을 재기 전에 반드시 동기화한다."""
    if device.type == "cuda":
        torch.cuda.synchronize(device)
