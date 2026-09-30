"""3교시: 2교시 CLI에 config만 추가한 참조 코드."""
import argparse
import json
import logging
import sys
from datetime import datetime
from pathlib import Path

from oss_tool import __version__
from oss_tool.sysinfo import collect, format_text
from oss_tool.config import load_settings, settings_to_dict

log = logging.getLogger("oss_tool")


# 실습 5–13분: 이름을 받아 인사한다.
def cmd_greet(args):
    print(f"안녕하세요, {args.name}. oss-tool {__version__} 입니다.")
    return 0


# 실습 13–21분: 결과는 stdout, 저장 안내는 stderr로 보낸다.
def cmd_sysinfo(args):
    info = collect()
    if args.json:
        print(json.dumps(info, ensure_ascii=True, indent=2))
    else:
        print(format_text(info))
    out = Path("outputs")
    out.mkdir(exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    path = out / f"sysinfo-{stamp}.json"
    path.write_text(json.dumps(info, ensure_ascii=False, indent=2), encoding="utf-8")
    log.info("저장: %s", path)
    return 0


# 3교시 실습 5–13분: 설정 로더의 값과 출처를 출력한다.
def cmd_config(args):
    settings = load_settings({"OLLAMA_HOST": args.host, "OLLAMA_MODEL": args.model})
    payload = settings_to_dict(settings)  # 비밀 값을 가린 뒤 출력한다.
    if args.json:
        print(json.dumps(payload, ensure_ascii=True, indent=2))
    else:
        for setting in settings.values():
            print(f"{setting.key} = {setting.display()} [{setting.source}]")
    return 0


def build_parser():
    parser = argparse.ArgumentParser(prog="oss-tool")
    sub = parser.add_subparsers(dest="command", required=True)
    greet = sub.add_parser("greet", help="인사말 출력")
    greet.add_argument("--name", default="student01")
    greet.set_defaults(func=cmd_greet)
    sysinfo = sub.add_parser("sysinfo", help="환경 정보 출력")
    sysinfo.add_argument("--json", action="store_true")
    sysinfo.set_defaults(func=cmd_sysinfo)
    config = sub.add_parser("config", help="설정값과 출처")
    config.add_argument("--host")
    config.add_argument("--model")
    config.add_argument("--json", action="store_true")
    config.set_defaults(func=cmd_config)
    return parser


def main():
    args = build_parser().parse_args()
    logging.basicConfig(level=logging.INFO, stream=sys.stderr,
                        format="%(levelname)s %(name)s: %(message)s")
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
