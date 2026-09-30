"""2교시 실습 5–13분: greet만 연결한다."""
import argparse
import sys

from oss_tool import __version__


def cmd_greet(args):
    print(f"안녕하세요, {args.name}. oss-tool {__version__} 입니다.")
    return 0


def build_parser():
    parser = argparse.ArgumentParser(prog="oss-tool")
    sub = parser.add_subparsers(dest="command", required=True)
    greet = sub.add_parser("greet", help="인사말 출력")
    greet.add_argument("--name", default="student01")
    greet.set_defaults(func=cmd_greet)
    return parser


def main():
    args = build_parser().parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
