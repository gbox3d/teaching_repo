"""소형 MLP 학습 루프 — 2교시.

외부 다운로드 없이 스크립트 안에서 2차원 분류 데이터(두 개의 반달 모양)를 만들고,
Dataset → DataLoader → forward → loss → backward → step 을 epoch 수만큼 반복한다.
epoch마다 train/val loss·accuracy를 기록해 outputs/train-<시각>.json에 남긴다.

    uv run python train_loop.py
    uv run python train_loop.py --epochs 400 --hidden 128 --tag overfit
    uv run python train_loop.py --device cpu --seed 7
"""

from __future__ import annotations

import argparse
import json
import math
import time
from datetime import datetime
from pathlib import Path
from typing import Any

import torch
from torch import nn
from torch.utils.data import DataLoader, Dataset

from runlog import gpu_name, pick_device, set_seed, sync


def make_moons(n: int, noise: float, label_noise: float, seed: int) -> tuple[torch.Tensor, torch.Tensor]:
    """반달 두 개가 맞물린 2차원 점 n개와 라벨(0/1)을 만든다. label_noise 비율만큼 라벨을 뒤집는다."""
    gen = torch.Generator().manual_seed(seed)
    n0 = n // 2
    n1 = n - n0
    t0 = torch.rand(n0, generator=gen) * math.pi
    t1 = torch.rand(n1, generator=gen) * math.pi
    x0 = torch.stack([torch.cos(t0), torch.sin(t0)], dim=1)
    x1 = torch.stack([1.0 - torch.cos(t1), 1.0 - torch.sin(t1) - 0.5], dim=1)
    x = torch.cat([x0, x1])
    y = torch.cat([torch.zeros(n0), torch.ones(n1)]).long()
    x = x + noise * torch.randn(x.shape, generator=gen)
    flip = torch.rand(n, generator=gen) < label_noise
    y[flip] = 1 - y[flip]
    perm = torch.randperm(n, generator=gen)
    return x[perm], y[perm]


class MoonDataset(Dataset):
    """Dataset은 두 가지만 답하면 된다: 길이(len)와 i번째 항목(getitem)."""

    def __init__(self, x: torch.Tensor, y: torch.Tensor) -> None:
        self.x = x
        self.y = y

    def __len__(self) -> int:
        return len(self.y)

    def __getitem__(self, i: int) -> tuple[torch.Tensor, torch.Tensor]:
        return self.x[i], self.y[i]


def build_model(hidden: int) -> nn.Module:
    return nn.Sequential(
        nn.Linear(2, hidden),
        nn.ReLU(),
        nn.Linear(hidden, hidden),
        nn.ReLU(),
        nn.Linear(hidden, 2),  # 출력은 클래스별 점수(logits). softmax는 손실 함수 안에서 처리한다.
    )


@torch.no_grad()
def evaluate(model: nn.Module, x: torch.Tensor, y: torch.Tensor, criterion: nn.Module) -> tuple[float, float]:
    model.eval()
    logits = model(x)
    loss = criterion(logits, y).item()
    acc = (logits.argmax(dim=1) == y).float().mean().item()
    return loss, acc


def train(args: argparse.Namespace, device: torch.device) -> dict[str, Any]:
    x, y = make_moons(args.n_samples, args.noise, args.label_noise, args.seed)
    n_val = int(len(y) * args.val_ratio)
    if n_val < 1 or n_val >= len(y):
        raise SystemExit(
            f"--val-ratio {args.val_ratio}로는 검증 데이터가 {n_val}개다. "
            "val이 없으면 과적합을 볼 수 없다. 0과 1 사이 값(예: 0.3)으로 다시 실행한다."
        )
    x_train, y_train = x[n_val:].to(device), y[n_val:].to(device)
    x_val, y_val = x[:n_val].to(device), y[:n_val].to(device)  # val은 학습에 절대 쓰지 않는다
    print(f"데이터: train {len(y_train)}개 · val {len(y_val)}개 · 입력 shape {list(x_train.shape[1:])}")

    loader = DataLoader(MoonDataset(x_train, y_train), batch_size=args.batch_size, shuffle=True)
    model = build_model(args.hidden).to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=args.lr)

    history: list[dict[str, float | int]] = []
    print(f"{'epoch':>5} {'train_loss':>10} {'val_loss':>9} {'train_acc':>9} {'val_acc':>8}")
    for epoch in range(1, args.epochs + 1):
        model.train()
        for xb, yb in loader:
            optimizer.zero_grad()  # 이전 배치의 grad가 누적되지 않게 비운다
            logits = model(xb)
            loss = criterion(logits, yb)
            loss.backward()  # 파라미터마다 grad 계산
            optimizer.step()  # grad 방향으로 파라미터 갱신
        train_loss, train_acc = evaluate(model, x_train, y_train, criterion)
        val_loss, val_acc = evaluate(model, x_val, y_val, criterion)
        history.append(
            {
                "epoch": epoch,
                "train_loss": round(train_loss, 4),
                "val_loss": round(val_loss, 4),
                "train_acc": round(train_acc, 4),
                "val_acc": round(val_acc, 4),
            }
        )
        if epoch == 1 or epoch % args.print_every == 0 or epoch == args.epochs:
            print(f"{epoch:>5} {train_loss:>10.4f} {val_loss:>9.4f} {train_acc:>9.3f} {val_acc:>8.3f}")

    return {"history": history, "n_train": len(y_train), "n_val": len(y_val)}


def summarize(history: list[dict[str, float | int]]) -> dict[str, Any]:
    best = min(history, key=lambda h: h["val_loss"])
    last = history[-1]
    rise = round(float(last["val_loss"]) - float(best["val_loss"]), 4)
    train_gap = round(float(last["val_loss"]) - float(last["train_loss"]), 4)
    # val loss 최저점 이후 5% 넘게 다시 올랐고 train loss는 계속 낮다면 과적합 신호로 본다
    overfit = rise > 0.05 * float(best["val_loss"]) and float(last["train_loss"]) < float(best["train_loss"])
    return {
        "val_loss_min": best["val_loss"],
        "val_loss_min_epoch": best["epoch"],
        "val_loss_final": last["val_loss"],
        "val_loss_rise_after_min": rise,
        "train_loss_final": last["train_loss"],
        "val_minus_train_final": train_gap,
        "val_acc_final": last["val_acc"],
        "overfit_suspected": overfit,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="합성 2차원 데이터로 소형 MLP를 학습하고 곡선을 기록한다.")
    parser.add_argument("--epochs", type=int, default=60)
    parser.add_argument("--hidden", type=int, default=32)
    parser.add_argument("--lr", type=float, default=0.003)
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--n-samples", type=int, default=300)
    parser.add_argument("--noise", type=float, default=0.25, help="좌표에 더하는 가우시안 잡음")
    parser.add_argument("--label-noise", type=float, default=0.1, help="라벨을 뒤집는 비율")
    parser.add_argument("--val-ratio", type=float, default=0.3)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--device", default="auto", help="auto | cpu | cuda")
    parser.add_argument("--print-every", type=int, default=10)
    parser.add_argument("--tag", default="", help="출력 파일 이름에 붙일 표식(예: overfit)")
    parser.add_argument("--out-dir", default="outputs")
    args = parser.parse_args()

    set_seed(args.seed)
    device = pick_device(args.device)
    print(f"torch {torch.__version__} · device={device} · gpu={gpu_name(device) or '-'} · seed={args.seed}")

    started = datetime.now()
    t0 = time.perf_counter()
    result = train(args, device)
    sync(device)
    elapsed = round(time.perf_counter() - t0, 2)
    summary = summarize(result["history"])

    print("\n요약")
    print(f"  val loss 최저 {summary['val_loss_min']} (epoch {summary['val_loss_min_epoch']}) → 마지막 {summary['val_loss_final']}")
    print(f"  마지막 train loss {summary['train_loss_final']} · val-train 차이 {summary['val_minus_train_final']}")
    print(f"  과적합 의심: {summary['overfit_suspected']} · 경과 {elapsed}s")

    stamp = started.strftime("%Y%m%d-%H%M%S")
    name = f"train-{stamp}" + (f"-{args.tag}" if args.tag else "") + ".json"
    out = Path(args.out_dir) / name
    out.parent.mkdir(parents=True, exist_ok=True)
    record = {
        "started_at": started.isoformat(timespec="seconds"),
        "elapsed_s": elapsed,
        "device": str(device),
        "gpu_name": gpu_name(device),
        "torch_version": torch.__version__,
        "config": vars(args),
        "n_train": result["n_train"],
        "n_val": result["n_val"],
        "summary": summary,
        "history": result["history"],
    }
    out.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"기록 저장: {out}")


if __name__ == "__main__":
    main()
