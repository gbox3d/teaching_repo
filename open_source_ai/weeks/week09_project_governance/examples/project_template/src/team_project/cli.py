"""팀 프로젝트 골격 CLI.

서브커맨드:
  doctor   Ollama 서버 연결과 캐시된 모델 목록을 확인하고 outputs/ 에 기록한다.
  version  패키지 버전을 출력한다.

설정 우선순위: 기본값 < .env·환경변수 < 명령행 인자.
모델 ID·주소는 코드에 고정하지 않는다. 정확한 값은 학기별 환경 기준표에서 확정한다.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

import httpx
from dotenv import load_dotenv

from team_project import __version__

DEFAULT_HOST = "http://localhost:11434"
DEFAULT_MODEL = "qwen3:8b"  # CPU 대체는 qwen3:0.6b


def load_settings(args: argparse.Namespace) -> dict[str, str]:
    """기본값 < .env·환경변수 < 인자 순서로 설정을 결정한다."""
    load_dotenv()
    host = args.host or os.environ.get("OLLAMA_HOST", DEFAULT_HOST)
    model = args.model or os.environ.get("OLLAMA_MODEL", DEFAULT_MODEL)
    return {"host": host.rstrip("/"), "model": model}


def check_tags(client: httpx.Client, host: str) -> dict[str, Any]:
    """GET /api/tags 로 서버 생존과 캐시된 모델 목록을 확인한다."""
    response = client.get(f"{host}/api/tags")
    response.raise_for_status()
    models = [item.get("name", "") for item in response.json().get("models", [])]
    return {"ok": True, "models": models}


def chat_test(client: httpx.Client, host: str, model: str) -> dict[str, Any]:
    """POST /api/chat 로 짧은 비스트리밍 응답 한 번을 받아 본다."""
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": "한 단어로 인사해."}],
        "stream": False,
        # Qwen3 계열은 thinking 출력이 답에 섞이므로 끈다.
        "think": False,
        "options": {"temperature": 0, "num_predict": 32},
    }
    response = client.post(f"{host}/api/chat", json=payload)
    if response.status_code == 404:
        return {"ok": False, "reason": f"모델이 없다: {model} (ollama list 로 확인)"}
    response.raise_for_status()
    data = response.json()
    return {
        "ok": True,
        "reply": data.get("message", {}).get("content", "").strip(),
        "eval_count": data.get("eval_count"),
    }


def write_report(out_dir: Path, report: dict[str, Any]) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    path = out_dir / f"doctor-{stamp}.json"
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def run_doctor(args: argparse.Namespace) -> int:
    settings = load_settings(args)
    report: dict[str, Any] = {
        "time": datetime.now().isoformat(timespec="seconds"),
        "version": __version__,
        "host": settings["host"],
        "model": settings["model"],
        "tags": None,
        "chat": None,
    }
    try:
        with httpx.Client(timeout=args.timeout) as client:
            report["tags"] = check_tags(client, settings["host"])
            if args.chat_test:
                report["chat"] = chat_test(client, settings["host"], settings["model"])
    except httpx.ConnectError:
        report["tags"] = {
            "ok": False,
            "reason": f"Ollama 서버에 연결할 수 없다: {settings['host']} (ollama serve 실행 여부, OLLAMA_HOST 값 확인)",
        }
    except httpx.TimeoutException:
        report["tags"] = {"ok": False, "reason": f"응답 시간 초과({args.timeout}초). 모델 로딩 중이면 다시 시도한다."}
    except httpx.HTTPStatusError as exc:
        report["tags"] = {"ok": False, "reason": f"HTTP {exc.response.status_code}: {exc.response.text[:200]}"}

    path = write_report(Path(args.out_dir), report)
    tags = report["tags"] or {}
    if tags.get("ok"):
        print(f"[OK] Ollama 연결: {settings['host']}")
        print(f"     캐시된 모델 {len(tags['models'])}개: {', '.join(tags['models']) or '(없음)'}")
        if settings["model"] not in tags["models"]:
            print(f"[주의] 기본 모델 {settings['model']} 이 캐시에 없다. 환경 기준표의 모델을 수업 전에 받아 둔다.")
    else:
        print(f"[실패] {tags.get('reason', '알 수 없는 오류')}")
    chat = report["chat"]
    if chat is not None:
        print(f"[chat] {'OK' if chat.get('ok') else '실패'}: {chat.get('reply') or chat.get('reason')}")
    print(f"기록: {path}")
    return 0 if tags.get("ok") else 1


def run_version(_: argparse.Namespace) -> int:
    print(f"team-project {__version__}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="팀 프로젝트 골격 CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    doctor = sub.add_parser("doctor", help="Ollama 연결·모델 목록 확인")
    doctor.add_argument("--host", help="Ollama 주소 (기본: OLLAMA_HOST 또는 http://localhost:11434)")
    doctor.add_argument("--model", help="확인할 모델 (기본: OLLAMA_MODEL 또는 qwen3:8b)")
    doctor.add_argument("--chat-test", action="store_true", help="/api/chat 로 짧은 응답 1회 확인")
    doctor.add_argument("--timeout", type=float, default=30.0, help="초 단위 시간 제한")
    doctor.add_argument("--out-dir", default="outputs", help="결과 JSON 폴더")
    doctor.set_defaults(func=run_doctor)

    version = sub.add_parser("version", help="버전 출력")
    version.set_defaults(func=run_version)
    return parser


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")  # Windows 콘솔(cp949)에서 인코딩 오류로 멈추지 않게 한다
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
