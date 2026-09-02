"""모델 후보의 추론 VRAM을 추정해 12 GB 기준으로 판정한다.

추정식(대략치이며 실측을 대체하지 않는다):
  가중치   = 파라미터 수 × 비트 ÷ 8
  KV 캐시  = 2 × 층 수 × 컨텍스트 길이 × KV 헤드 수 × 헤드 차원 × KV 비트 ÷ 8
  실행 여유 = (가중치 + KV 캐시) × overhead   (런타임 버퍼·활성화 등)

후보 형식: "이름,파라미터,비트" 또는 "이름,파라미터,비트,층수,KV헤드,헤드차원"
  예) "qwen3:4b,4B,4"   "my-model,0.5B,16,24,2,64"
층 수·KV 헤드·헤드 차원은 모델 카드의 config.json(num_hidden_layers,
num_key_value_heads, hidden_size ÷ num_attention_heads)에서 읽는다.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

GIB = 1024**3


@dataclass
class Candidate:
    name: str
    params: float
    bits: int
    layers: int = 0
    kv_heads: int = 0
    head_dim: int = 0


def parse_params(text: str) -> float:
    """'4B', '0.6B', '500M', '4e9' 같은 표기를 파라미터 수(float)로 바꾼다."""
    match = re.fullmatch(r"\s*(\d+(?:\.\d+)?)\s*([bBmM]?)\s*", text)
    if match:
        value, unit = float(match.group(1)), match.group(2).lower()
        return value * {"b": 1e9, "m": 1e6, "": 1.0}[unit]
    try:
        return float(text)
    except ValueError as exc:
        raise ValueError(f"파라미터 표기를 읽을 수 없다: {text!r} (예: 4B, 0.6B, 500M, 4e9)") from exc


def parse_candidate(text: str) -> Candidate:
    parts = [part.strip() for part in text.split(",")]
    if len(parts) not in (3, 6):
        raise ValueError(
            f"후보 형식 오류: {text!r} - '이름,파라미터,비트' 또는 '이름,파라미터,비트,층수,KV헤드,헤드차원'"
        )
    name, params, bits = parts[0], parse_params(parts[1]), int(parts[2])
    if bits not in (2, 3, 4, 5, 6, 8, 16, 32):
        raise ValueError(f"비트 수가 이상하다: {bits} (양자화 4·8, 반정밀 16, 단정밀 32)")
    extra = [int(part) for part in parts[3:]] if len(parts) == 6 else [0, 0, 0]
    return Candidate(name, params, bits, *extra)


def params_from_tag(tag: str) -> float | None:
    """'qwen3:4b' 같은 Ollama 태그 끝의 크기 표기에서 파라미터 수를 읽는다."""
    match = re.search(r"(\d+(?:\.\d+)?)b$", tag.lower())
    return float(match.group(1)) * 1e9 if match else None


def default_candidates() -> list[Candidate]:
    """환경변수의 기본 모델 태그로 후보 두 개를 만든다(교재 검증용 기본값)."""
    result: list[Candidate] = []
    for key, fallback in (("OLLAMA_MODEL", "qwen3:4b"), ("OLLAMA_MODEL_SMALL", "qwen3:0.6b")):
        tag = os.environ.get(key, fallback)
        params = params_from_tag(tag)
        if params is None:
            raise ValueError(f"{key}={tag} 에서 파라미터 수를 읽을 수 없다. --candidate 로 직접 준다.")
        result.append(Candidate(tag, params, 4))
    return result


def estimate(cand: Candidate, ctx: int, kv_bits: int, overhead: float, vram_gb: float) -> dict[str, Any]:
    weights = cand.params * cand.bits / 8
    has_kv = cand.layers > 0 and cand.kv_heads > 0 and cand.head_dim > 0
    kv_cache = 2 * cand.layers * ctx * cand.kv_heads * cand.head_dim * kv_bits / 8 if has_kv else 0.0
    extra = (weights + kv_cache) * overhead
    total = weights + kv_cache + extra
    verdict = "여유" if total <= vram_gb * GIB * 0.8 else ("빠듯" if total <= vram_gb * GIB else "초과")
    return {
        **asdict(cand),
        "ctx": ctx,
        "weights_gib": round(weights / GIB, 2),
        "kv_cache_gib": round(kv_cache / GIB, 2),
        "overhead_gib": round(extra / GIB, 2),
        "total_gib": round(total / GIB, 2),
        "kv_known": has_kv,
        "verdict": verdict,
    }


def render_markdown(rows: list[dict[str, Any]], vram_gb: float) -> str:
    lines = [
        f"# VRAM 추정 ({datetime.now().isoformat(timespec='seconds')}, 기준 {vram_gb:g} GB)",
        "",
        "| 후보 | 파라미터 | 비트 | ctx | 가중치 GiB | KV GiB | 여유 GiB | 합계 GiB | 판정 |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in rows:
        kv = f"{row['kv_cache_gib']}" if row["kv_known"] else "미계산"
        lines.append(
            f"| {row['name']} | {row['params'] / 1e9:.2f}B | {row['bits']} | {row['ctx']} | "
            f"{row['weights_gib']} | {kv} | {row['overhead_gib']} | {row['total_gib']} | {row['verdict']} |"
        )
    lines += ["", "- 판정: 여유(기준의 80% 이하) · 빠듯(80~100%) · 초과(100% 초과)",
              "- KV 미계산 후보는 층 수·KV 헤드·헤드 차원을 주면 다시 계산된다.",
              "- 추정치는 4주차 `ollama ps` 실측값과 나란히 적는다."]
    return "\n".join(lines) + "\n"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="모델 후보 VRAM 추정")
    parser.add_argument("--candidate", action="append", default=[], help='"이름,파라미터,비트[,층수,KV헤드,헤드차원]" (반복 가능)')
    parser.add_argument("--ctx", type=int, default=8192, help="컨텍스트 길이(토큰)")
    parser.add_argument("--kv-bits", type=int, default=16, help="KV 캐시 비트 수")
    parser.add_argument("--overhead", type=float, default=0.15, help="실행 여유 비율")
    parser.add_argument("--vram-gb", type=float, default=float(os.environ.get("GPU_VRAM_GB", "12")), help="판정 기준 VRAM(GB)")
    parser.add_argument("--layers", type=int, default=0, help="층 수를 주지 않은 후보에 적용")
    parser.add_argument("--kv-heads", type=int, default=0, help="KV 헤드 수를 주지 않은 후보에 적용")
    parser.add_argument("--head-dim", type=int, default=0, help="헤드 차원을 주지 않은 후보에 적용")
    parser.add_argument("--out-dir", default="outputs", help="결과 폴더")
    return parser


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")  # Windows 콘솔(cp949)에서 인코딩 오류로 멈추지 않게 한다
    load_dotenv()
    args = build_parser().parse_args(argv)
    try:
        candidates = [parse_candidate(text) for text in args.candidate] or default_candidates()
    except ValueError as exc:
        print(f"[오류] {exc}", file=sys.stderr)
        return 2
    for cand in candidates:
        if cand.layers == 0 and args.layers:
            cand.layers, cand.kv_heads, cand.head_dim = args.layers, args.kv_heads, args.head_dim
    rows = [estimate(cand, args.ctx, args.kv_bits, args.overhead, args.vram_gb) for cand in candidates]
    markdown = render_markdown(rows, args.vram_gb)
    print(markdown)

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    (out_dir / f"vram-{stamp}.md").write_text(markdown, encoding="utf-8")
    (out_dir / f"vram-{stamp}.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"기록: {out_dir / f'vram-{stamp}.md'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
