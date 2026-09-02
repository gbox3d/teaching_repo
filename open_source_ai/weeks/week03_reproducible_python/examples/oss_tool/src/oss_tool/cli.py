"""oss-tool 명령행 진입점.

서브커맨드
  greet    인사말 출력 (엔트리포인트가 연결됐는지 확인하는 가장 작은 명령)
  sysinfo  OS·CPU·RAM·GPU 정보 출력, outputs/ 에 JSON 저장
  config   설정값과 그 출처(default / .env / env / arg) 출력

결과는 stdout, 진행 로그는 stderr 로 보낸다. 그래야 `| ConvertFrom-Json` 이 깨지지 않는다.
화면에 찍는 문장에는 콘솔 코드 페이지(cp949 등)에 없는 특수문자를 쓰지 않는다.
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from datetime import datetime
from pathlib import Path

import httpx

from oss_tool import __version__
from oss_tool.config import load_settings, settings_to_dict
from oss_tool.sysinfo import collect, format_text

log = logging.getLogger("oss_tool")


def configure_streams() -> None:
    """출력이 파이프·파일로 갈 때 콘솔 인코딩에 없는 글자가 있어도 죽지 않게 한다(글자는 ? 로 대체)."""
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is not None:
            reconfigure(errors="replace")


def save_json(out_dir: Path, prefix: str, payload: dict[str, object]) -> Path:
    """outputs/<prefix>-<시각>.json 으로 저장하고 경로를 돌려준다."""
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    path = out_dir / f"{prefix}-{stamp}.json"
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    log.info("저장: %s", path)
    return path


def cmd_greet(args: argparse.Namespace) -> int:
    message = f"안녕하세요, {args.name}. oss-tool {__version__} 입니다."
    if args.shout:
        message = message.upper()
    for _ in range(args.repeat):
        print(message)
    return 0


def cmd_sysinfo(args: argparse.Namespace) -> int:
    info = collect()
    if args.json:
        # 파이프로 넘길 때 콘솔 인코딩에 영향받지 않도록 stdout 은 ASCII 이스케이프로 출력한다.
        print(json.dumps(info, ensure_ascii=True, indent=2))
    else:
        print(format_text(info))
    if not args.no_save:
        save_json(args.out, "sysinfo", info)
    return 0


def ping_ollama(host: str) -> int:
    """GET /api/tags 로 Ollama 서버 연결만 확인한다. 본격적인 호출은 4주차에서 한다."""
    url = f"{host.rstrip('/')}/api/tags"
    try:
        response = httpx.get(url, timeout=3.0)
        response.raise_for_status()
    except httpx.ConnectError:
        print(f"연결 실패: {url} (Ollama 서버가 꺼져 있거나 OLLAMA_HOST 가 틀렸다)")
        return 2
    except httpx.HTTPError as exc:
        print(f"HTTP 오류: {url} ({exc})")
        return 2
    names = [m.get("name", "?") for m in response.json().get("models", [])]
    print(f"연결 성공: {url} / 모델 {len(names)}개: {', '.join(names) or '(없음)'}")
    return 0


def cmd_config(args: argparse.Namespace) -> int:
    overrides = {"OLLAMA_HOST": args.host, "OLLAMA_MODEL": args.model}
    settings = load_settings(overrides, env_file=args.env_file)
    payload = settings_to_dict(settings)
    if args.json:
        print(json.dumps(payload, ensure_ascii=True, indent=2))
    else:
        print("설정 (우선순위: default < .env < env < arg)")
        for setting in settings.values():
            print(f"  {setting.key:<13} = {setting.display():<28} [{setting.source}]")
    if not args.no_save:
        save_json(args.out, "config", payload)
    if args.ping:
        return ping_ollama(settings["OLLAMA_HOST"].value or "")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="oss-tool", description="오픈소스 AI 응용: 로컬 AI 도우미 CLI 골격"
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument("-v", "--verbose", action="store_true", help="DEBUG 로그를 stderr 로 출력")
    sub = parser.add_subparsers(dest="command", required=True)

    greet = sub.add_parser("greet", help="인사말 출력")
    greet.add_argument("--name", default="student01", help="부를 이름 (기본 student01)")
    greet.add_argument("--shout", action="store_true", help="대문자로 출력")
    greet.add_argument("--repeat", type=int, default=1, help="반복 횟수 (기본 1)")
    greet.set_defaults(func=cmd_greet)

    sysinfo = sub.add_parser("sysinfo", help="OS·CPU·RAM·GPU 정보")
    sysinfo.add_argument("--json", action="store_true", help="JSON 으로 출력")
    sysinfo.add_argument("--out", type=Path, default=Path("outputs"), help="저장 폴더 (기본 outputs)")
    sysinfo.add_argument("--no-save", action="store_true", help="파일로 저장하지 않음")
    sysinfo.set_defaults(func=cmd_sysinfo)

    config = sub.add_parser("config", help="설정값과 출처")
    config.add_argument("--host", help="OLLAMA_HOST 를 이번 실행에서만 덮어씀")
    config.add_argument("--model", help="OLLAMA_MODEL 을 이번 실행에서만 덮어씀")
    config.add_argument("--env-file", default=".env", help=".env 파일 경로 (기본 .env)")
    config.add_argument("--json", action="store_true", help="JSON 으로 출력")
    config.add_argument("--out", type=Path, default=Path("outputs"), help="저장 폴더 (기본 outputs)")
    config.add_argument("--no-save", action="store_true", help="파일로 저장하지 않음")
    config.add_argument("--ping", action="store_true", help="OLLAMA_HOST 의 /api/tags 로 연결 확인")
    config.set_defaults(func=cmd_config)
    return parser


def main(argv: list[str] | None = None) -> int:
    """[project.scripts] 가 가리키는 함수. 반환값이 곧 종료 코드다."""
    configure_streams()
    args = build_parser().parse_args(argv)
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        stream=sys.stderr,
        format="%(levelname)s %(name)s: %(message)s",
    )
    log.debug("인자: %s", vars(args))
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
