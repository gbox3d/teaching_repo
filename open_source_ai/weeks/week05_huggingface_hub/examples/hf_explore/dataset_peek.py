"""datasets 로 로컬 파일과 Hub 데이터셋을 같은 API 로 열어 필드 구조·건수·샘플·카드 라이선스를 기록한다 — 3교시.

    uv run python dataset_peek.py                                            # data/sample_qa.jsonl
    uv run python dataset_peek.py --streaming --n 3 --max-chars 40
    uv run python dataset_peek.py --file data\\없음.jsonl                      # 실패 경로: 파일 없음
    uv run python dataset_peek.py --hub-id klue/klue --config ynat --split train --streaming --n 5
    uv run python dataset_peek.py --hub-id klue/klue --split train --streaming   # 실패 경로: config 누락

종료 코드: 0 성공, 1 실패(파일 없음, config 누락, 저장소 없음, 오프라인). 실패해도 outputs/ 에 error 를 남긴다.
"""

from __future__ import annotations

import argparse
import sys
from itertools import islice
from pathlib import Path
from typing import Any

from hf_env import first_line, offline_mode, prepare_env, save_json

DEFAULT_FILE = "data/sample_qa.jsonl"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="로컬 jsonl 또는 Hub 데이터셋의 구조·샘플·카드 라이선스 기록")
    parser.add_argument("--file", default=DEFAULT_FILE, help="로컬 JSON Lines 파일. --hub-id 가 있으면 무시")
    parser.add_argument("--hub-id", default=None, help="Hub 데이터셋 ID(조직/이름). 네트워크 필요")
    parser.add_argument("--config", default=None, help="Hub 데이터셋의 구성(config) 이름")
    parser.add_argument("--split", default="train", help="split 이름(train, validation, test 등)")
    parser.add_argument("--streaming", action="store_true", help="전부 받지 않고 앞부분만 흘려 본다(IterableDataset)")
    parser.add_argument("--n", type=int, default=5, help="보여 줄 샘플 수")
    parser.add_argument("--max-chars", type=int, default=80, help="샘플 문자열을 자를 길이")
    parser.add_argument("--outputs", default="outputs", help="결과 JSON 을 둘 폴더")
    parser.add_argument("--tag", default=None, help="출력 파일 이름 뒤에 붙일 짧은 표식")
    return parser


def open_dataset(args: argparse.Namespace) -> tuple[Any, str]:
    from datasets import load_dataset

    if args.hub_id:
        ds = load_dataset(args.hub_id, args.config, split=args.split, streaming=args.streaming)
        return ds, f"hub:{args.hub_id}" + (f"/{args.config}" if args.config else "") + f"@{args.split}"
    path = Path(args.file)
    if not path.is_file():
        raise FileNotFoundError(f"파일이 없다: {path}")
    ds = load_dataset("json", data_files=str(path), split=args.split, streaming=args.streaming)
    return ds, f"file:{path}"


def describe_features(ds: Any, first_row: dict[str, Any]) -> dict[str, str]:
    features = getattr(ds, "features", None)
    if features:
        return {name: str(feature) for name, feature in features.items()}
    # 스트리밍에서는 파일 전체를 읽지 않아 features 가 비어 있을 수 있다 → 첫 행의 파이썬 자료형으로 추론
    return {name: f"(추론) {type(value).__name__}" for name, value in first_row.items()}


def truncate(value: Any, max_chars: int) -> Any:
    if isinstance(value, str):
        return value if len(value) <= max_chars else value[:max_chars] + "…"
    if isinstance(value, list):
        return [truncate(v, max_chars) for v in value[:5]] + (["…"] if len(value) > 5 else [])
    if isinstance(value, dict):
        return {k: truncate(v, max_chars) for k, v in value.items()}
    return value


def card_license(args: argparse.Namespace) -> tuple[str | None, str]:
    """카드(README.md) YAML 의 license. 로컬은 파일 옆 README.md, Hub 는 카드만 내려받는다."""
    from huggingface_hub import DatasetCard

    try:
        if args.hub_id:
            if offline_mode():
                return None, "오프라인 모드라 카드를 받지 않음"
            card = DatasetCard.load(args.hub_id)
            note = "Hub 카드 YAML 의 license"
        else:
            path = Path(args.file).with_name("README.md")
            if not path.is_file():
                return None, f"카드 없음: {path}"
            card = DatasetCard.load(path)
            note = f"{path} 의 YAML license"
        return getattr(card.data, "license", None), note
    except Exception as exc:
        return None, f"카드 읽기 실패: {first_line(exc)}"


def explain(exc: BaseException, args: argparse.Namespace) -> str:
    name = exc.__class__.__name__
    lines = [ln.strip() for ln in str(exc).strip().splitlines() if ln.strip()]
    text = " ".join(lines[:2])[:500] if lines else name
    if isinstance(exc, FileNotFoundError):
        return f"{text} — --file 경로와 현재 폴더(Get-Location)를 확인한다"
    if isinstance(exc, ValueError) and "config" in text.lower():
        return f"config 이름이 필요하다: {args.hub_id} — 아래 목록에서 하나를 --config 로 지정한다\n  {text}"
    if offline_mode():
        return f"오프라인 모드(HF_HUB_OFFLINE=1)라 캐시에 없는 Hub 데이터셋을 열 수 없다: {args.hub_id} ({name})"
    if args.hub_id:
        return f"Hub 데이터셋을 열지 못했다: {args.hub_id} — ID 철자, config·split 이름, 네트워크를 확인한다 ({name}: {text})"
    return f"로컬 파일을 열지 못했다: {args.file} — JSON Lines 형식(한 줄에 객체 하나, UTF-8)인지 확인한다 ({name}: {text})"


def main() -> int:
    prepare_env()
    args = build_parser().parse_args()
    record: dict[str, Any] = {"source": args.hub_id or args.file, "config": args.config, "split": args.split, "streaming": args.streaming, "n": args.n}
    try:
        ds, source = open_dataset(args)
        rows = list(islice(iter(ds), args.n))
        num_rows = getattr(ds, "num_rows", None)  # IterableDataset 에는 없다
        features = describe_features(ds, rows[0] if rows else {})
        info_license = getattr(getattr(ds, "info", None), "license", None) or None
    except Exception as exc:
        message = explain(exc, args)
        print(message, file=sys.stderr)
        record.update(error=message, error_type=exc.__class__.__name__)
        print(f"saved: {save_json(Path(args.outputs), 'dataset_peek', args.tag, record)}", file=sys.stderr)
        return 1

    license_value, license_note = card_license(args)
    samples = [truncate(row, args.max_chars) for row in rows]
    record.update(source=source, mode="streaming(IterableDataset)" if args.streaming else "load(Dataset)", num_rows=num_rows, features=features, info_license=info_license, card_license=license_value, card_note=license_note, samples=samples)

    print(f"출처: {source}   모드: {record['mode']}")
    print(f"건수: {num_rows if num_rows is not None else '(스트리밍: 알 수 없음)'}")
    print(f"info.license: {info_license or '(없음)'}   카드 license: {license_value or '(없음)'}  ← {license_note}")
    print("필드:")
    for name, feature in features.items():
        print(f"  {name:<12} {feature}")
    print(f"샘플 {len(samples)}개:")
    for i, row in enumerate(samples, 1):
        print(f"  [{i}] {row}")
    print(f"saved: {save_json(Path(args.outputs), 'dataset_peek', args.tag, record)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
