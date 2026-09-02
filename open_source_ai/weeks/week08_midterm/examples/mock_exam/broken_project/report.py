"""모의 실기 A 복구 대상 프로젝트의 실행 스크립트.

이 파일 자체에는 오류가 없다. 프로젝트 설정(`pyproject.toml`, `.gitignore`, `.env` 취급)을 고치면
`uv run python report.py` 가 동작해야 한다.

- 설정은 환경변수(.env 포함) + 기본값으로 읽는다.
- Ollama `/api/tags` 로 모델 목록을 확인하고 `outputs/report.json` 에 기록한다.
- 서버가 꺼져 있어도 파일은 만들고, 사람이 읽을 메시지와 종료 코드 2 로 알린다.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Any

import httpx
from dotenv import load_dotenv

DEFAULT_HOST = "http://localhost:11434"
DEFAULT_MODEL = "qwen3:4b"  # 교재 검증용 기본값. 확정 값은 환경 기준표, CPU 대체는 qwen3:0.6b


def read_settings() -> dict[str, str]:
    """환경변수(.env 포함)에서 설정을 읽는다. 값이 없으면 기본값을 쓴다."""
    load_dotenv()
    host = os.environ.get("OLLAMA_HOST", DEFAULT_HOST).strip().rstrip("/")
    if not host.startswith("http://") and not host.startswith("https://"):
        host = "http://" + host
    model = os.environ.get("OLLAMA_MODEL", DEFAULT_MODEL).strip()
    return {"host": host, "model": model}


def fetch_model_names(host: str, timeout: float) -> list[str]:
    """Ollama /api/tags 로 설치된 모델 이름 목록을 가져온다."""
    response = httpx.get(f"{host}/api/tags", timeout=timeout)
    response.raise_for_status()
    models = response.json().get("models", [])
    return [str(item.get("name", "")) for item in models]


def model_is_available(model: str, names: list[str]) -> bool:
    """태그가 없는 이름은 ':latest' 를 붙여 비교한다."""
    wanted = model if ":" in model else f"{model}:latest"
    return wanted in names


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Ollama 연결·모델 상태를 outputs/report.json 에 기록한다."
    )
    parser.add_argument("--timeout", type=float, default=5.0, help="연결 대기 시간(초), 기본 5")
    parser.add_argument("--output", default="outputs/report.json", help="기록 파일 경로")
    return parser


def main() -> int:
    # Windows 에서 출력이 파이프·파일로 넘어가면 콘솔 인코딩(cp949)이 적용되어 일부 기호에서 예외가 난다.
    # 인코딩은 그대로 두고, 표현할 수 없는 문자만 '?' 로 바꿔 프로그램이 죽지 않게 한다.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(errors="replace")
    args = build_parser().parse_args()
    settings = read_settings()
    report: dict[str, Any] = {
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "host": settings["host"],
        "model": settings["model"],
        "ollama_reachable": False,
        "model_available": False,
        "models": [],
        # 비밀값은 기록하지 않는다. 존재 여부만 남겨 .env 가 읽혔는지 확인한다.
        "hf_token_present": bool(os.environ.get("HF_TOKEN")),
        "note": "",
    }

    try:
        names = fetch_model_names(settings["host"], args.timeout)
        report["ollama_reachable"] = True
        report["models"] = names
        report["model_available"] = model_is_available(settings["model"], names)
    except httpx.ConnectError:
        report["note"] = "Ollama 서버에 연결할 수 없다. `ollama serve` 실행 여부와 OLLAMA_HOST 를 확인한다."
    except httpx.TimeoutException:
        report["note"] = f"{args.timeout}초 안에 응답이 없다. 서버가 뜨는 중이면 잠시 뒤 다시 실행한다."
    except httpx.HTTPError as exc:
        report["note"] = f"HTTP 오류: {exc}"

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    status = "연결됨" if report["ollama_reachable"] else "연결 실패"
    print(f"[Ollama] {settings['host']} - {status}")
    if report["ollama_reachable"]:
        found = "있음" if report["model_available"] else "없음 (ollama list 로 확인)"
        print(f"[모델] {settings['model']} - {found}")
    else:
        print(f"[안내] {report['note']}", file=sys.stderr)
    print(f"[저장] {output}")
    return 0 if report["ollama_reachable"] else 2


if __name__ == "__main__":
    sys.exit(main())
