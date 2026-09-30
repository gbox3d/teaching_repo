"""실기 시작 전 환경 점검 — Ollama 연결과 기본 모델 존재를 확인하고 outputs/env-check.json 에 남긴다.

실행: uv run python check_env.py [--host URL] [--model NAME] [--timeout SEC]
종료 코드: 0 = 연결되고 모델 있음, 1 = 그 밖의 경우
"""

from __future__ import annotations

import argparse
import json
import platform
import sys
import time
from pathlib import Path
from typing import Any

import httpx

from config import load_settings

OUTPUT_PATH = Path("outputs") / "env-check.json"


def fetch_model_names(host: str, timeout: float) -> list[str]:
    """Ollama /api/tags 로 설치된 모델 이름 목록을 가져온다."""
    response = httpx.get(f"{host}/api/tags", timeout=timeout)
    response.raise_for_status()
    return [str(item.get("name", "")) for item in response.json().get("models", [])]


def model_is_available(model: str, names: list[str]) -> bool:
    """태그가 없는 이름은 ':latest' 를 붙여 비교한다."""
    wanted = model if ":" in model else f"{model}:latest"
    return wanted in names


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Ollama 연결·모델 존재를 점검하고 outputs/env-check.json 에 기록한다.")
    parser.add_argument("--host", help="Ollama 주소 (기본: OLLAMA_HOST 환경변수)")
    parser.add_argument("--model", help="확인할 모델 (기본: OLLAMA_MODEL 환경변수)")
    parser.add_argument("--timeout", type=float, default=5.0, help="연결 대기 시간(초), 기본 5")
    return parser


def main() -> int:
    # Windows 에서 출력이 파이프·파일로 넘어가면 콘솔 인코딩(cp949)이 적용되어 일부 기호에서 예외가 난다.
    # 인코딩은 그대로 두고, 표현할 수 없는 문자만 '?' 로 바꿔 프로그램이 죽지 않게 한다.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(errors="replace")
    args = build_parser().parse_args()
    settings = load_settings(host=args.host, model=args.model, timeout=args.timeout)
    result: dict[str, Any] = {
        "checked_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "python": platform.python_version(),
        "os": platform.platform(),
        "host": settings.host,
        "model": settings.model,
        "ollama_reachable": False,
        "model_available": False,
        "models": [],
        "note": "",
    }

    try:
        names = fetch_model_names(settings.host, settings.timeout)
        result["ollama_reachable"] = True
        result["models"] = names
        result["model_available"] = model_is_available(settings.model, names)
        if not result["model_available"]:
            result["note"] = "기본 모델이 목록에 없다. 이름·태그를 확인하거나 사전 캐시된 모델로 OLLAMA_MODEL 을 바꾼다."
    except httpx.ConnectError:
        result["note"] = "Ollama 서버에 연결할 수 없다. `ollama serve` 실행 여부와 OLLAMA_HOST 를 확인한다."
    except httpx.TimeoutException:
        result["note"] = f"{settings.timeout}초 안에 응답이 없다. 서버가 뜨는 중이면 잠시 뒤 다시 실행한다."
    except httpx.HTTPError as exc:
        result["note"] = f"HTTP 오류: {exc}"

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    reach = "[OK]" if result["ollama_reachable"] else "[실패]"
    avail = "[OK]" if result["model_available"] else "[실패]"
    print(f"{reach} Ollama 연결: {settings.host}")
    print(f"{avail} 기본 모델: {settings.model}")
    if result["note"]:
        print(f"[안내] {result['note']}")
    print(f"[저장] {OUTPUT_PATH}")
    return 0 if (result["ollama_reachable"] and result["model_available"]) else 1


if __name__ == "__main__":
    sys.exit(main())
