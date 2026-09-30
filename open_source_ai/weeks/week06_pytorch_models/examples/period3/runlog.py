"""실험 기록 헬퍼 — 6주차 공통.

무엇을 돌렸는지(모델·설정·seed·device), 얼마나 걸렸는지, GPU 메모리를 얼마나 썼는지를
한 JSON 파일에 남긴다. 다른 스크립트에서는 다음처럼 가져다 쓴다.

    from runlog import RunLog, pick_device, set_seed

단독으로 실행하면 outputs/runs/ 아래에 쌓인 기록을 표로 보여 준다.

    uv run python runlog.py
    uv run python runlog.py --last 3
"""

from __future__ import annotations

import argparse
import json
import platform
import random
import time
from datetime import datetime
from pathlib import Path
from typing import Any

import numpy as np
import torch

DEFAULT_RUN_DIR = Path("outputs") / "runs"


def set_seed(seed: int) -> None:
    """Python·NumPy·PyTorch 난수를 한 번에 고정한다. GPU 연산은 완전 결정론이 아닐 수 있다."""
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def pick_device(name: str = "auto") -> torch.device:
    """'auto'면 CUDA가 있을 때 cuda, 아니면 cpu. cuda를 요청했는데 없으면 사람이 읽을 메시지로 종료한다."""
    if name == "auto":
        return torch.device("cuda" if torch.cuda.is_available() else "cpu")
    if name.startswith("cuda") and not torch.cuda.is_available():
        raise SystemExit(
            "CUDA 장치를 요청했지만 torch.cuda.is_available()가 False다. "
            "드라이버·torch 휠(CUDA 인덱스)을 확인하거나 --device cpu로 다시 실행한다."
        )
    return torch.device(name)


def gpu_name(device: torch.device) -> str | None:
    if device.type != "cuda":
        return None
    return torch.cuda.get_device_name(device)


def sync(device: torch.device) -> None:
    """GPU 연산은 비동기이므로 시간을 재기 전에 반드시 동기화한다."""
    if device.type == "cuda":
        torch.cuda.synchronize(device)


class RunLog:
    """실험 1회 = RunLog 1개. 생성 시 시작 시각을 찍고 finish()에서 파일을 쓴다."""

    def __init__(
        self,
        name: str,
        config: dict[str, Any],
        device: torch.device,
        out_dir: Path | str = DEFAULT_RUN_DIR,
    ) -> None:
        self.name = name
        self.config = config
        self.device = device
        self.out_dir = Path(out_dir)
        self.started_at = datetime.now()
        self._t0 = time.perf_counter()
        self.notes: list[str] = []
        if device.type == "cuda":
            torch.cuda.reset_peak_memory_stats(device)

    def note(self, text: str) -> None:
        """실행 중 관찰한 것을 한 줄씩 남긴다(예: 경고 메시지, 예상과 다른 점)."""
        self.notes.append(text)

    def finish(self, metrics: dict[str, Any]) -> Path:
        sync(self.device)
        elapsed = time.perf_counter() - self._t0
        peak_mb: float | None = None
        if self.device.type == "cuda":
            peak_mb = round(torch.cuda.max_memory_allocated(self.device) / (1024**2), 1)

        record: dict[str, Any] = {
            "name": self.name,
            "started_at": self.started_at.isoformat(timespec="seconds"),
            "elapsed_s": round(elapsed, 3),
            "device": str(self.device),
            "gpu_name": gpu_name(self.device),
            "max_memory_allocated_mb": peak_mb,
            "torch_version": torch.__version__,
            "python_version": platform.python_version(),
            "config": self.config,
            "metrics": metrics,
            "notes": self.notes,
        }
        self.out_dir.mkdir(parents=True, exist_ok=True)
        stamp = self.started_at.strftime("%Y%m%d-%H%M%S")
        path = self.out_dir / f"{stamp}-{self.name}.json"
        path.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return path


def load_runs(run_dir: Path) -> list[dict[str, Any]]:
    if not run_dir.exists():
        return []
    runs: list[dict[str, Any]] = []
    for path in sorted(run_dir.glob("*.json")):
        try:
            runs.append(json.loads(path.read_text(encoding="utf-8")))
        except json.JSONDecodeError:
            print(f"건너뜀(JSON 아님): {path}")
    return runs


def summarize_metrics(metrics: dict[str, Any]) -> str:
    parts: list[str] = []
    for key, value in metrics.items():
        if isinstance(value, (int, float, str, bool)):
            parts.append(f"{key}={value}")
    return ", ".join(parts)[:60]


def main() -> None:
    parser = argparse.ArgumentParser(description="outputs/runs/ 아래 실험 기록을 표로 보여 준다.")
    parser.add_argument("--run-dir", default=str(DEFAULT_RUN_DIR), help="기록 폴더")
    parser.add_argument("--last", type=int, default=10, help="최근 N건만 표시")
    args = parser.parse_args()

    runs = load_runs(Path(args.run_dir))
    if not runs:
        print(f"기록이 없다: {args.run_dir}")
        print("pretrained_embed.py를 먼저 실행하면 기록이 생긴다.")
        return

    print(f"{'시작 시각':<20} {'이름':<16} {'device':<7} {'경과(s)':>8} {'최대MB':>8}  metrics")
    for run in runs[-args.last :]:
        peak = run.get("max_memory_allocated_mb")
        peak_text = "-" if peak is None else f"{peak:.0f}"
        print(
            f"{run.get('started_at', '?'):<20} {run.get('name', '?'):<16} {run.get('device', '?'):<7} "
            f"{run.get('elapsed_s', 0):>8.2f} {peak_text:>8}  {summarize_metrics(run.get('metrics', {}))}"
        )
    print(f"총 {len(runs)}건 중 최근 {min(args.last, len(runs))}건")


if __name__ == "__main__":
    main()
