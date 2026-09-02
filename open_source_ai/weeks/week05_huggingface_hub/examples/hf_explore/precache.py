"""수업 전 사전 캐시 — 강의자·조교용. 실습 시간에는 실행하지 않는다.

모델 저장소의 스냅샷(가중치·토크나이저·config·README.md)을 캐시에 받는다. 카드 원문(README.md)이
함께 내려오므로 네트워크가 없는 실습실에서도 snapshots/<commit hash>/README.md 로 카드를 읽을 수 있다.
데이터셋은 기본으로 카드(README.md)만 받는다. --dataset-full 을 주면 파일까지 받는다.

    uv run python precache.py                                     # .env 의 HF_CLS_MODEL·HF_TEXT_MODEL·HF_EMBED_MODEL
    uv run python precache.py --models Qwen/Qwen2.5-0.5B-Instruct
    uv run python precache.py --dataset klue/klue                 # 카드만
    uv run python precache.py --dataset klue/klue --dataset-full

safetensors 가 있는 저장소는 *.bin 을 받지 않는다(중복 용량, pickle 위험 — 13주차). safetensors 가 없을 때만 *.bin 을 받는다.
종료 코드: 0 전부 성공, 1 하나라도 실패
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

from hf_env import env, explain_hub_error, format_bytes, prepare_env, resolve_cache_dir, save_json

# 같은 가중치의 다른 형식(TF·Flax·ONNX·CoreML 등)은 받지 않는다. 학생 실습에는 PyTorch 형식만 필요하다.
IGNORE_ALWAYS = ["*.h5", "*.msgpack", "*.onnx", "onnx/*", "*.tflite", "*.ckpt", "*.gguf", "*.mlmodel", "coreml/*", "*.ot"]
IGNORE_BIN = IGNORE_ALWAYS + ["*.bin", "*.pth", "*.pt"]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="수업 전 모델·데이터셋 카드 사전 캐시")
    parser.add_argument("--models", nargs="*", default=None, help="모델 ID 목록. 생략하면 .env 의 HF_CLS_MODEL·HF_TEXT_MODEL·HF_EMBED_MODEL")
    parser.add_argument("--dataset", default=None, help="데이터셋 ID(조직/이름). 기본은 README.md 만 받는다")
    parser.add_argument("--dataset-full", action="store_true", help="데이터셋 파일 전체를 받는다(용량 주의)")
    parser.add_argument("--cache-dir", default=None, help="캐시 폴더. 생략하면 HF_HOME/hub 또는 기본 위치")
    parser.add_argument("--outputs", default="outputs", help="결과 JSON 을 둘 폴더")
    parser.add_argument("--tag", default=None, help="출력 파일 이름 뒤에 붙일 짧은 표식")
    return parser


def snapshot_size(path: Path) -> int:
    return sum(p.stat().st_size for p in path.rglob("*") if p.is_file())


def fetch_model(repo_id: str, cache_dir: Path) -> dict[str, Any]:
    from huggingface_hub import snapshot_download

    path = Path(snapshot_download(repo_id, cache_dir=str(cache_dir), ignore_patterns=IGNORE_BIN))
    weight_format = "safetensors"
    if not any(path.rglob("*.safetensors")):
        # safetensors 가 없는 오래된 저장소. 이번에는 *.bin 을 허용해 다시 받는다(이미 받은 파일은 건너뛴다).
        path = Path(snapshot_download(repo_id, cache_dir=str(cache_dir), ignore_patterns=IGNORE_ALWAYS))
        weight_format = "bin" if any(path.rglob("*.bin")) else "none"
    return {
        "repo_id": repo_id,
        "repo_type": "model",
        "commit_hash": path.name,
        "snapshot_path": str(path),
        "size_on_disk": snapshot_size(path),
        "weight_format": weight_format,
        "has_card": (path / "README.md").is_file(),
    }


def fetch_dataset(repo_id: str, cache_dir: Path, full: bool) -> dict[str, Any]:
    from huggingface_hub import snapshot_download

    allow = None if full else ["README.md"]
    path = Path(snapshot_download(repo_id, repo_type="dataset", cache_dir=str(cache_dir), allow_patterns=allow))
    return {
        "repo_id": repo_id,
        "repo_type": "dataset",
        "commit_hash": path.name,
        "snapshot_path": str(path),
        "size_on_disk": snapshot_size(path),
        "card_only": not full,
        "has_card": (path / "README.md").is_file(),
    }


def main() -> int:
    prepare_env()
    args = build_parser().parse_args()
    cache_dir = resolve_cache_dir(args.cache_dir)
    models = args.models if args.models else [m for m in (env("HF_CLS_MODEL"), env("HF_TEXT_MODEL"), env("HF_EMBED_MODEL")) if m]
    print(f"캐시 위치: {cache_dir}")

    done: list[dict[str, Any]] = []
    failed: list[dict[str, str]] = []
    for repo_id in models:
        print(f"\n[model] {repo_id} 받는 중…")
        try:
            item = fetch_model(repo_id, cache_dir)
        except Exception as exc:  # 저장소 없음·gated·네트워크를 한 문장으로
            message = explain_hub_error(exc, repo_id)
            print("  실패: " + message, file=sys.stderr)
            failed.append({"repo_id": repo_id, "error": message})
            continue
        done.append(item)
        print(f"  commit {item['commit_hash'][:12]}  {format_bytes(item['size_on_disk'])}  가중치 {item['weight_format']}  카드 {'있음' if item['has_card'] else '없음'}")

    if args.dataset:
        print(f"\n[dataset] {args.dataset} {'전체' if args.dataset_full else '카드만'} 받는 중…")
        try:
            item = fetch_dataset(args.dataset, cache_dir, args.dataset_full)
            done.append(item)
            print(f"  commit {item['commit_hash'][:12]}  {format_bytes(item['size_on_disk'])}  카드 {'있음' if item['has_card'] else '없음'}")
        except Exception as exc:
            message = explain_hub_error(exc, args.dataset)
            print("  실패: " + message, file=sys.stderr)
            failed.append({"repo_id": args.dataset, "error": message})

    total = sum(int(item["size_on_disk"]) for item in done)
    print(f"\n완료 {len(done)}개, 실패 {len(failed)}개, 받은 스냅샷 합계 {format_bytes(total)}")
    path = save_json(Path(args.outputs), "precache", args.tag, {"cache_dir": str(cache_dir), "done": done, "failed": failed})
    print(f"saved: {path}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
