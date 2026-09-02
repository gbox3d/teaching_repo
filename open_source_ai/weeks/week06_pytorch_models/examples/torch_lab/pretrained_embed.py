"""사전학습 모델 직접 호출 — 3교시.

pipeline 없이 AutoTokenizer/AutoModel을 직접 불러
문장 → 토큰 ID → hidden state → pooling → 문장 임베딩 → 코사인 유사도 행렬 → softmax
순서로 계산한다. 실험 기록은 runlog.RunLog로 outputs/runs/에 남긴다.

    uv run python pretrained_embed.py
    uv run python pretrained_embed.py --sentences my_sentences.txt --pooling cls
    uv run python pretrained_embed.py --device cpu --show-tokens
"""

from __future__ import annotations

import argparse
import json
import os
import time
from datetime import datetime
from pathlib import Path
from typing import Any

import torch
import torch.nn.functional as F
from dotenv import load_dotenv

from runlog import RunLog, gpu_name, pick_device, set_seed, sync

DEFAULT_MODEL = "intfloat/multilingual-e5-small"

# 수업 내용을 다룬 문장 5개. 실제 인물·기관 정보 없음.
DEFAULT_SENTENCES = [
    "uv는 Python 가상환경과 의존성을 한 도구로 관리한다.",
    "가상환경과 lock 파일로 Python 프로젝트를 다른 PC에서 재현한다.",
    "Ollama는 내 PC에서 언어 모델을 실행하는 로컬 서버다.",
    "오늘 점심에는 김치찌개와 계란말이를 먹었다.",
    "MIT 라이선스는 저작권 표시를 유지하면 재배포를 허용한다.",
]


def load_sentences(path: str | None) -> list[str]:
    if path is None:
        return list(DEFAULT_SENTENCES)
    lines = [ln.strip() for ln in Path(path).read_text(encoding="utf-8").splitlines()]
    sentences = [ln for ln in lines if ln and not ln.startswith("#")]
    if len(sentences) < 2:
        raise SystemExit(f"문장이 2개 이상 필요하다: {path}")
    return sentences


def load_model(model_id: str, device: torch.device) -> tuple[Any, Any, float]:
    # transformers는 무거우므로 필요할 때만 가져온다(--help가 빨라진다).
    from transformers import AutoModel, AutoTokenizer

    t0 = time.perf_counter()
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_id)
        model = AutoModel.from_pretrained(model_id)
    except (OSError, ValueError) as exc:
        raise SystemExit(
            f"모델을 불러오지 못했다: {model_id}\n"
            "  - 수업 전에 사전 캐시되었는지, HF_HOME이 그 캐시를 가리키는지 확인한다.\n"
            "  - 네트워크가 없으면 HF_HUB_OFFLINE=1 상태에서 캐시만으로 열려야 한다.\n"
            f"  - 원인: {exc}"
        ) from exc
    model.to(device)
    model.eval()  # dropout 등 학습 전용 동작을 끈다
    return tokenizer, model, time.perf_counter() - t0


def mean_pool(hidden: torch.Tensor, mask: torch.Tensor) -> torch.Tensor:
    """패딩 토큰을 빼고 토큰 벡터의 평균을 낸다. hidden [B,T,H], mask [B,T] → [B,H]."""
    m = mask.unsqueeze(-1).to(hidden.dtype)
    return (hidden * m).sum(dim=1) / m.sum(dim=1).clamp(min=1e-9)


def cls_pool(hidden: torch.Tensor, mask: torch.Tensor) -> torch.Tensor:
    """첫 토큰([CLS] 또는 <s>) 벡터만 쓴다."""
    return hidden[:, 0]


def print_matrix(sim: torch.Tensor, labels: list[str]) -> None:
    n = sim.shape[0]
    print("      " + " ".join(f"{lab:>6}" for lab in labels))
    for i in range(n):
        row = " ".join(f"{sim[i, j].item():6.3f}" for j in range(n))
        print(f"{labels[i]:>6} {row}")


def main() -> None:
    load_dotenv()
    parser = argparse.ArgumentParser(description="문장 임베딩을 직접 계산하고 유사도 행렬을 만든다.")
    parser.add_argument("--model", default=os.environ.get("HF_EMBED_MODEL", DEFAULT_MODEL), help="Hugging Face 모델 ID")
    parser.add_argument("--sentences", default=None, help="한 줄에 한 문장인 텍스트 파일(없으면 내장 5문장)")
    parser.add_argument("--prefix", default="query: ", help="문장 앞에 붙일 접두어. e5 계열은 'query: '를 권장. 다른 모델은 '' 사용")
    parser.add_argument("--pooling", choices=["mean", "cls"], default="mean")
    parser.add_argument("--max-length", type=int, default=128)
    parser.add_argument("--temperature", type=float, default=0.05, help="softmax 온도. 작을수록 확률이 한쪽으로 쏠린다")
    parser.add_argument("--device", default="auto", help="auto | cpu | cuda")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--show-tokens", action="store_true", help="첫 문장의 토큰 분할을 출력")
    parser.add_argument("--out-dir", default="outputs")
    args = parser.parse_args()

    set_seed(args.seed)
    device = pick_device(args.device)
    sentences = load_sentences(args.sentences)
    print(f"torch {torch.__version__} · device={device} · gpu={gpu_name(device) or '-'}")
    print(f"모델 {args.model} · pooling={args.pooling} · prefix={args.prefix!r} · 문장 {len(sentences)}개")

    run = RunLog(
        name="embed",
        config={
            "model": args.model,
            "pooling": args.pooling,
            "prefix": args.prefix,
            "max_length": args.max_length,
            "temperature": args.temperature,
            "seed": args.seed,
            "n_sentences": len(sentences),
            "sentences_file": args.sentences,
        },
        device=device,
    )

    tokenizer, model, load_s = load_model(args.model, device)
    revision = getattr(model.config, "_commit_hash", None)
    print(f"모델 로드 {load_s:.1f}s · revision={revision or '알 수 없음(로컬 경로)'}")

    # 1) 문장 → 토큰 ID
    batch = tokenizer(
        [args.prefix + s for s in sentences],
        padding=True,
        truncation=True,
        max_length=args.max_length,
        return_tensors="pt",
    ).to(device)
    ids, mask = batch["input_ids"], batch["attention_mask"]
    print(f"input_ids {list(ids.shape)} · attention_mask 합(문장별 실제 토큰 수)={mask.sum(dim=1).tolist()}")
    if args.show_tokens:
        print("첫 문장 토큰:", tokenizer.convert_ids_to_tokens(ids[0]))

    # 2) 토큰 ID → hidden state (추론이므로 no_grad)
    t0 = time.perf_counter()
    with torch.no_grad():
        out = model(**batch)
    hidden = out.last_hidden_state
    sync(device)
    infer_s = time.perf_counter() - t0
    print(f"last_hidden_state {list(hidden.shape)}  (문장 수, 토큰 수, 은닉 차원) · 추론 {infer_s * 1000:.1f} ms")

    # 3) pooling → 문장 임베딩 → 정규화
    pooled = mean_pool(hidden, mask) if args.pooling == "mean" else cls_pool(hidden, mask)
    emb = F.normalize(pooled, p=2, dim=1)
    print(f"문장 임베딩 {list(emb.shape)} · 첫 벡터 앞 4개 {[round(v, 4) for v in emb[0, :4].tolist()]}")

    # 4) 코사인 유사도 = 정규화 벡터의 내적 → 행렬곱 한 번
    sim = emb @ emb.T
    labels = [f"s{i + 1}" for i in range(len(sentences))]
    print("\n코사인 유사도 행렬")
    print_matrix(sim, labels)
    for i, s in enumerate(sentences):
        print(f"  {labels[i]}: {s}")

    off = sim.clone()
    off.fill_diagonal_(-1.0)
    best = torch.argmax(off).item()
    bi, bj = divmod(best, len(sentences))
    print(f"\n가장 비슷한 쌍: {labels[bi]} – {labels[bj]} ({off[bi, bj].item():.3f})")

    # 5) 점수(logits) → softmax 확률: 첫 문장에서 본 나머지 문장의 '가까움' 확률
    scores = sim[0, 1:]
    probs = torch.softmax(scores / args.temperature, dim=0)
    print(f"s1 기준 softmax(유사도/{args.temperature}): " + ", ".join(f"{labels[j + 1]}={p:.3f}" for j, p in enumerate(probs.tolist())))
    print("  온도를 바꾸면 순위는 같아도 확률의 쏠림이 달라진다 (--temperature).")

    # 6) 결과와 실험 기록 저장
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_path = Path(args.out_dir) / f"embed-{stamp}.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        json.dumps(
            {
                "model": args.model,
                "revision": revision,
                "pooling": args.pooling,
                "prefix": args.prefix,
                "sentences": sentences,
                "token_counts": mask.sum(dim=1).tolist(),
                "hidden_shape": list(hidden.shape),
                "embedding_dim": emb.shape[1],
                "similarity": [[round(v, 4) for v in row] for row in sim.tolist()],
                "most_similar_pair": [labels[bi], labels[bj]],
                "softmax_from_s1": {labels[j + 1]: round(p, 4) for j, p in enumerate(probs.tolist())},
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    run.note(f"결과 파일: {out_path}")
    log_path = run.finish(
        {
            "revision": revision,
            "load_s": round(load_s, 2),
            "infer_ms": round(infer_s * 1000, 1),
            "embedding_dim": emb.shape[1],
            "most_similar_pair": f"{labels[bi]}-{labels[bj]}",
            "most_similar_score": round(off[bi, bj].item(), 4),
        }
    )
    print(f"\n결과 저장: {out_path}\n실험 기록: {log_path}")


if __name__ == "__main__":
    main()
