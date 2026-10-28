"""캐시 보고: 내려받은 모델이 어디에, 어떤 commit 으로, 얼마나 있는지. uv run ex03"""

from huggingface_hub import scan_cache_dir
from huggingface_hub.constants import HF_HUB_CACHE


def main() -> None:
    print("캐시 위치:", HF_HUB_CACHE)  # HF_HOME 을 정했으면 그 아래 hub/, 아니면 ~/.cache/huggingface/hub
    cache = scan_cache_dir()
    print(f"총 용량: {cache.size_on_disk / 1e9:.2f} GB, 저장소 {len(cache.repos)}개")
    for repo in sorted(cache.repos, key=lambda r: r.size_on_disk, reverse=True):
        print(f"- {repo.repo_id} [{repo.repo_type}] {repo.size_on_disk / 1e9:.2f} GB")
        for rev in repo.revisions:
            refs = ",".join(rev.refs) or "(ref 없음)"
            print(f"    commit {rev.commit_hash[:12]}  refs={refs}  파일 {rev.nb_files}개")
