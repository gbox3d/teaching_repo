"""10주차 공통 헬퍼.

환경변수 읽기, 장치·dtype 선택, JSONL 읽기, outputs/ 기록, 모델 로드 오류 안내를 모아 둔다.
다른 스크립트(lora_setup.py, train_lora.py, compare.py, merge.py)가 이 모듈을 가져다 쓴다.
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

import torch
from dotenv import load_dotenv

load_dotenv()

# 모델 ID는 하드코딩하지 않고 환경변수 + 기본값으로 읽는다.
# 기본값은 교재 검증용이며 실제 모델 ID·revision은 학기별 환경 기준표에서 확정한다.
DEFAULT_MODEL = "Qwen/Qwen2.5-0.5B-Instruct"
DEFAULT_TARGET_MODULES = "q_proj,k_proj,v_proj,o_proj"

# 학습과 비교에서 같은 system 프롬프트를 쓴다. 조건이 다르면 전후 비교가 공정하지 않다.
SYSTEM_PROMPT = "당신은 오픈소스 AI 응용 수업의 도우미입니다. 한국어로 짧고 정확하게 답합니다."

OUTPUTS_DIR = Path("outputs")


def model_id_from_env() -> str:
    """HF_TEXT_MODEL 환경변수를 읽고 없으면 기본값을 돌려준다."""
    return os.environ.get("HF_TEXT_MODEL", DEFAULT_MODEL)


def resolve_device(choice: str) -> torch.device:
    """'auto'면 CUDA가 있을 때 cuda, 없으면 cpu. 명시하면 그대로 쓴다."""
    if choice == "auto":
        return torch.device("cuda" if torch.cuda.is_available() else "cpu")
    if choice == "cuda" and not torch.cuda.is_available():
        print("[안내] --device cuda를 요청했지만 CUDA를 쓸 수 없다. cpu로 진행한다.")
        return torch.device("cpu")
    return torch.device(choice)


def resolve_dtype(choice: str, device: torch.device) -> torch.dtype:
    """'auto'면 GPU에서는 bf16(지원 시), CPU에서는 fp32를 고른다."""
    if choice == "auto":
        if device.type == "cuda" and torch.cuda.is_bf16_supported():
            return torch.bfloat16
        return torch.float32
    table = {"fp32": torch.float32, "bf16": torch.bfloat16, "fp16": torch.float16}
    return table[choice]


def dtype_bytes(dtype: torch.dtype) -> int:
    return 4 if dtype == torch.float32 else 2


def split_modules(text: str) -> list[str]:
    return [item.strip() for item in text.split(",") if item.strip()]


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    """한 줄에 JSON 객체 하나인 파일을 읽는다. 빈 줄은 건너뛴다."""
    if not path.exists():
        print(f"[오류] 데이터 파일이 없다: {path}")
        sys.exit(2)
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as exc:
                print(f"[오류] {path}:{line_no} JSON 형식 오류: {exc}")
                sys.exit(2)
    return rows


def timestamp() -> str:
    return datetime.now().strftime("%Y%m%d-%H%M%S")


def write_json(path: Path, payload: dict[str, Any]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def write_text(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip("\n") + "\n", encoding="utf-8")
    return path


def cuda_peak_mb() -> float | None:
    """CUDA가 있으면 지금까지의 최대 할당 메모리(MB), 없으면 None."""
    if not torch.cuda.is_available():
        return None
    return round(torch.cuda.max_memory_allocated() / (1024 * 1024), 1)


def gpu_name() -> str:
    if torch.cuda.is_available():
        return torch.cuda.get_device_name(0)
    return "cpu"


def explain_load_error(model_id: str, exc: Exception) -> None:
    """모델 로드 실패를 사람이 읽을 메시지로 바꾼다."""
    print(f"[오류] 모델을 불러오지 못했다: {model_id}")
    print(f"       원인: {type(exc).__name__}: {str(exc).splitlines()[0] if str(exc) else ''}")
    print("       확인할 것:")
    print("       1. 모델 ID 오타 여부 (.env 의 HF_TEXT_MODEL 또는 --model)")
    print("       2. 수업 전 캐시 여부 (HF_HOME 아래 hub/models--… 폴더)")
    print("       3. 네트워크가 막힌 실습실이면 HF_HUB_OFFLINE=1 로 캐시만 사용")
    print("       4. gated 모델이면 HF_TOKEN 이 .env 에 있는지 (토큰은 커밋 금지)")


def load_tokenizer(model_id: str) -> Any:
    """토크나이저만 읽는다. 템플릿·마스킹 확인(--inspect)처럼 모델 가중치가 필요 없을 때 쓴다."""
    from transformers import AutoTokenizer

    try:
        tokenizer = AutoTokenizer.from_pretrained(model_id)
    except (OSError, ValueError) as exc:
        explain_load_error(model_id, exc)
        sys.exit(2)
    if tokenizer.pad_token is None:
        # 패딩 토큰이 없는 토크나이저는 eos를 패딩으로 쓴다.
        tokenizer.pad_token = tokenizer.eos_token
    return tokenizer


def load_tokenizer_and_model(model_id: str, device: torch.device, dtype: torch.dtype) -> tuple[Any, Any]:
    """토크나이저와 CausalLM 모델을 읽어 지정 장치·dtype으로 옮긴다."""
    from transformers import AutoModelForCausalLM

    tokenizer = load_tokenizer(model_id)
    try:
        model = AutoModelForCausalLM.from_pretrained(model_id)
    except (OSError, ValueError) as exc:
        explain_load_error(model_id, exc)
        sys.exit(2)
    model = model.to(device=device, dtype=dtype)
    return tokenizer, model


def build_messages(instruction: str, output: str | None = None) -> list[dict[str, str]]:
    """chat template에 넣을 메시지 목록. output이 None이면 답을 생성할 차례다."""
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": instruction},
    ]
    if output is not None:
        messages.append({"role": "assistant", "content": output})
    return messages
