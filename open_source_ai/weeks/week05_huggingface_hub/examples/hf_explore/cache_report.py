"""캐시 보고 — 1교시. scan_cache_dir() 로 캐시 위치·용량·commit hash 를 표로 만들고,
파라미터 수로 용량을 암산하고, Hub 저장소의 파일 합계와 sha 를 조회해 캐시와 비교한다.

    uv run python cache_report.py
    uv run python cache_report.py --params 0.5 --bytes-per-param 2
    uv run python cache_report.py --estimate Qwen/Qwen2.5-0.5B-Instruct
    uv run python cache_report.py --estimate Qwen/Qwen2.5-0.5B-Instruct --revision <commit hash>
    uv run python cache_report.py --cache-dir C:\\없는폴더                # 실패 경로
    uv run python cache_report.py --estimate 없는조직/없는모델               # 실패 경로

종료 코드: 0 성공, 1 실패(캐시 폴더 없음, 저장소·revision 없음, 네트워크·오프라인)
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

from hf_env import explain_hub_error, first_line, format_bytes, prepare_env, resolve_cache_dir, save_json


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Hugging Face 캐시 보고와 용량 추정")
    parser.add_argument("--cache-dir", default=None, help="캐시 폴더. 생략하면 HF_HOME/hub 또는 기본 위치")
    parser.add_argument("--params", type=float, default=None, help="파라미터 수(십억 단위). 0.5 = 5억 개")
    parser.add_argument("--bytes-per-param", type=int, default=2, help="파라미터당 바이트. fp16=2, fp32=4, int8=1")
    parser.add_argument("--estimate", default=None, help="Hub 저장소 ID. 파일 합계와 sha 를 조회한다(네트워크 필요)")
    parser.add_argument("--revision", default=None, help="--estimate 에 쓸 브랜치 또는 commit hash. 생략하면 main")
    parser.add_argument("--repo-type", choices=["model", "dataset"], default="model", help="--estimate 대상의 종류")
    parser.add_argument("--top", type=int, default=5, help="--estimate 에서 보여 줄 큰 파일 수")
    parser.add_argument("--outputs", default="outputs", help="결과 JSON 을 둘 폴더")
    parser.add_argument("--tag", default=None, help="출력 파일 이름 뒤에 붙일 짧은 표식")
    return parser


def scan_cache(cache_dir: Path) -> dict[str, Any]:
    from huggingface_hub import scan_cache_dir

    info = scan_cache_dir(cache_dir)
    repos = []
    for repo in sorted(info.repos, key=lambda r: r.size_on_disk, reverse=True):
        revisions = [
            {
                "commit_hash": rev.commit_hash,
                "refs": sorted(rev.refs),
                "size_on_disk": rev.size_on_disk,
                "nb_files": rev.nb_files,
                "snapshot_path": str(rev.snapshot_path),
            }
            for rev in sorted(repo.revisions, key=lambda r: r.last_modified, reverse=True)
        ]
        repos.append({"repo_id": repo.repo_id, "repo_type": repo.repo_type, "size_on_disk": repo.size_on_disk, "nb_files": repo.nb_files, "revisions": revisions})
    return {"cache_dir": str(cache_dir), "size_on_disk": info.size_on_disk, "repo_count": len(repos), "warnings": [str(w) for w in info.warnings], "repos": repos}


def print_cache(cache: dict[str, Any]) -> None:
    print(f"캐시 위치: {cache['cache_dir']}")
    print(f"총 용량: {format_bytes(cache['size_on_disk'])} (저장소 {cache['repo_count']}개)")
    if not cache["repos"]:
        print("  캐시가 비어 있다. precache.py 로 모델을 먼저 받는다.")
    for repo in cache["repos"]:
        print(f"- {repo['repo_id']} [{repo['repo_type']}]  {format_bytes(repo['size_on_disk'])}  파일 {repo['nb_files']}개")
        for rev in repo["revisions"]:
            refs = ",".join(rev["refs"]) or "(ref 없음)"
            print(f"    commit {rev['commit_hash'][:12]}  refs={refs}  {format_bytes(rev['size_on_disk'])}  {rev['snapshot_path']}")
    for warning in cache["warnings"]:
        print(f"  경고: {warning}")


def estimate_hub(repo_id: str, revision: str | None, repo_type: str, top: int) -> dict[str, Any]:
    from huggingface_hub import HfApi

    api = HfApi()
    if repo_type == "dataset":
        info = api.dataset_info(repo_id, revision=revision, files_metadata=True)
    else:
        info = api.model_info(repo_id, revision=revision, files_metadata=True)
    files = [{"path": s.rfilename, "size": s.size or 0} for s in (info.siblings or [])]
    card = getattr(info, "card_data", None)
    return {
        "repo_id": repo_id,
        "repo_type": repo_type,
        "requested_revision": revision,
        "sha": info.sha,
        "gated": getattr(info, "gated", None),
        "card_license": getattr(card, "license", None),
        "file_count": len(files),
        "total_size": sum(f["size"] for f in files),
        "largest_files": sorted(files, key=lambda f: f["size"], reverse=True)[:top],
    }


def compare_with_cache(hub: dict[str, Any], cache: dict[str, Any]) -> str:
    for repo in cache["repos"]:
        if repo["repo_id"] == hub["repo_id"]:
            hashes = [rev["commit_hash"] for rev in repo["revisions"]]
            if hub["sha"] in hashes:
                return "캐시의 commit hash 와 같다"
            return "캐시에 있지만 commit 이 다르다(캐시: " + ", ".join(h[:12] for h in hashes) + ")"
    return "캐시에 없는 저장소다"


def main() -> int:
    prepare_env()
    args = build_parser().parse_args()
    cache_dir = resolve_cache_dir(args.cache_dir)
    if not cache_dir.is_dir():
        print(
            f"캐시 폴더가 없다: {cache_dir}\n"
            "  - .env 의 HF_HOME / HF_HUB_CACHE 경로 철자를 확인한다.\n"
            "  - 아직 아무 모델도 받지 않은 PC 라면 이 메시지가 정상이다. precache.py 를 먼저 실행한다.",
            file=sys.stderr,
        )
        return 1
    try:
        cache = scan_cache(cache_dir)
    except Exception as exc:
        print(f"캐시 스캔 실패: {cache_dir} — {first_line(exc)}", file=sys.stderr)
        return 1
    print_cache(cache)
    report: dict[str, Any] = {"cache": cache, "estimate_params": None, "hub": None}

    if args.params is not None:
        estimated = args.params * 1e9 * args.bytes_per_param
        report["estimate_params"] = {"params_billion": args.params, "bytes_per_param": args.bytes_per_param, "bytes": estimated}
        print(f"\n암산: {args.params}B 파라미터 × {args.bytes_per_param}바이트 ≈ {format_bytes(estimated)} (가중치만, 토크나이저·설정 파일 제외)")

    exit_code = 0
    if args.estimate:
        try:
            hub = estimate_hub(args.estimate, args.revision, args.repo_type, args.top)
            hub["cache_match"] = compare_with_cache(hub, cache)
            report["hub"] = hub
            print(f"\nHub 조회: {hub['repo_id']}  sha={hub['sha']}  gated={hub['gated']}  license={hub['card_license']}")
            print(f"  파일 {hub['file_count']}개 합계 {format_bytes(hub['total_size'])}  → {hub['cache_match']}")
            for f in hub["largest_files"]:
                print(f"    {format_bytes(f['size']):>10}  {f['path']}")
        except Exception as exc:
            message = explain_hub_error(exc, args.estimate)
            print(message, file=sys.stderr)
            report["hub"] = {"repo_id": args.estimate, "error": message}
            exit_code = 1

    path = save_json(Path(args.outputs), "cache_report", args.tag, report)
    print(f"saved: {path}")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
