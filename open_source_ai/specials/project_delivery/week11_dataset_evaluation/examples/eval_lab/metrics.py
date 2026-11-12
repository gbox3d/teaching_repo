"""metrics.py — 분류 지표(accuracy·precision·recall·F1)와 생성 지표(정확 일치·키워드 포함·유사도·형식 준수) 함수 모음.

evaluate.py가 import해서 쓴다. 단독 실행하면 자체 예시로 지표를 계산해 outputs/metrics_demo.json에 남긴다.
실행: uv run python metrics.py --demo
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import numpy as np

# 수업 도우미 답변 형식. 10주차 sample_sft.jsonl(LoRA 학습 데이터)과 같은 세 줄 형식이다.
# 첫 줄 "핵심:", 가운데 줄 "이유:", 마지막 줄 "다음 할 일:", 전체 400자 이하.
FORMAT_HEAD = "핵심:"
FORMAT_MID = "이유:"
FORMAT_TAIL = "다음 할 일:"
MAX_CHARS = 400


def normalize(text: str) -> str:
    """소문자화 + 공백 제거. 키워드 포함·정확 일치 판정에 쓴다."""
    return re.sub(r"\s+", "", (text or "").lower())


def char_bigrams(text: str) -> set[str]:
    t = normalize(text)
    return {t[i : i + 2] for i in range(len(t) - 1)}


def similarity(pred: str, ref: str) -> float:
    """문자 2-gram Jaccard 유사도(0~1). 외부 라이브러리 없이 계산하는 단순 유사도다."""
    a, b = char_bigrams(pred), char_bigrams(ref)
    return 1.0 if not a and not b else len(a & b) / len(a | b)


def exact_match(pred: str, ref: str) -> bool:
    return normalize(pred) == normalize(ref)


def keyword_hit(pred: str, keywords: list[str]) -> float:
    """정답 키워드 중 출력에 들어 있는 비율(0~1). 키워드가 없으면 1.0."""
    if not keywords:
        return 1.0
    p = normalize(pred)
    return sum(1 for k in keywords if normalize(k) in p) / len(keywords)


def format_ok(pred: str) -> bool:
    """세 줄 형식 판정. 줄 수·머리말·길이만 본다. 내용이 맞는지는 모른다(3교시 수동 채점의 몫)."""
    lines = [l.strip() for l in (pred or "").splitlines() if l.strip()]
    if len(lines) < 3 or len(pred) > MAX_CHARS:
        return False
    return (
        lines[0].startswith(FORMAT_HEAD)
        and any(l.startswith(FORMAT_MID) for l in lines[1:-1])
        and lines[-1].startswith(FORMAT_TAIL)
    )


def hangul_ratio(text: str) -> float:
    """글자(문자·숫자 제외 기호 무시) 중 한글 음절 비율. 언어 혼합의 신호로 쓴다."""
    letters = [c for c in text or "" if c.isalpha()]
    if not letters:
        return 0.0
    return sum(1 for c in letters if "가" <= c <= "힣") / len(letters)


def has_repetition(text: str) -> bool:
    """같은 문장(6자 이상)이 두 번 이상 나오거나 같은 10자 조각이 세 번 이상 나오면 반복으로 본다."""
    parts = [p.strip() for p in re.split(r"[.!?\n]+", text or "") if len(p.strip()) >= 6]
    if len(parts) != len(set(parts)):
        return True
    t = normalize(text)
    return any(t.count(t[i : i + 10]) >= 3 for i in range(0, max(0, len(t) - 10), 5))


def score_item(pred: str, ref: str, keywords: list[str]) -> dict:
    return {
        "exact": exact_match(pred, ref),
        "keyword_hit": round(keyword_hit(pred, keywords), 3),
        "format_ok": format_ok(pred),
        "similarity": round(similarity(pred, ref), 3),
        "hangul_ratio": round(hangul_ratio(pred), 3),
        "repetition": has_repetition(pred),
    }


def summarize(rows: list[dict]) -> dict:
    n = len(rows)
    if n == 0:
        return {"n": 0}
    return {
        "n": n,
        "keyword_hit_rate": round(float(np.mean([r["keyword_hit"] for r in rows])), 3),
        "format_rate": round(sum(r["format_ok"] for r in rows) / n, 3),
        "exact_rate": round(sum(r["exact"] for r in rows) / n, 3),
        "similarity_mean": round(float(np.mean([r["similarity"] for r in rows])), 3),
        "hangul_ratio_mean": round(float(np.mean([r["hangul_ratio"] for r in rows])), 3),
        "repetition_count": sum(r["repetition"] for r in rows),
        "missing_count": sum(1 for r in rows if r.get("missing")),
    }


def confusion(y_true: list[int], y_pred: list[int]) -> dict[str, int]:
    """이진 분류 혼동행렬. 1을 양성으로 본다."""
    t, p = np.asarray(y_true), np.asarray(y_pred)
    return {
        "tp": int(((t == 1) & (p == 1)).sum()),
        "fp": int(((t == 0) & (p == 1)).sum()),
        "fn": int(((t == 1) & (p == 0)).sum()),
        "tn": int(((t == 0) & (p == 0)).sum()),
    }


def prf(y_true: list[int], y_pred: list[int]) -> dict[str, float]:
    c = confusion(y_true, y_pred)
    total = sum(c.values())
    precision = c["tp"] / (c["tp"] + c["fp"]) if c["tp"] + c["fp"] else 0.0
    recall = c["tp"] / (c["tp"] + c["fn"]) if c["tp"] + c["fn"] else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {
        "accuracy": round((c["tp"] + c["tn"]) / total, 3) if total else 0.0,
        "precision": round(precision, 3),
        "recall": round(recall, 3),
        "f1": round(f1, 3),
        **c,
    }


def demo() -> dict:
    # 분류 예: 20개 출력에 대해 "형식 준수(1)/위반(0)"를 사람이 붙인 정답과 자동 판정 결과
    y_true = [1] * 14 + [0] * 6
    y_pred = [1] * 12 + [0, 0] + [1, 1] + [0] * 4
    ref = (
        "핵심: .venv는 커밋하지 않고 .gitignore에 넣는다.\n"
        "이유: 가상환경은 PC마다 경로와 바이너리가 달라 산출물이다.\n"
        "다음 할 일: `git status`에 .venv가 나타나지 않는지 확인한다."
    )
    cands = {
        "형식 준수·키워드 포함": "핵심: .venv 폴더는 .gitignore에 넣고 커밋하지 않는다.\n이유: 환경은 PC마다 다르다.\n다음 할 일: git status를 확인한다.",
        "내용은 맞고 형식 위반": ".venv는 커밋하지 않는 것이 좋습니다. .gitignore에 추가하세요.",
        "언어 혼합·반복": "The .venv folder should be ignored. The .venv folder should be ignored. 커밋 no.",
    }
    return {
        "classification": prf(y_true, y_pred),
        "generation": {name: score_item(text, ref, [".gitignore", "커밋"]) for name, text in cands.items()},
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="지표 함수 자체 예시")
    parser.add_argument("--demo", action="store_true", help="예시 데이터로 지표를 계산해 출력한다")
    parser.add_argument("--out", default="outputs/metrics_demo.json")
    args = parser.parse_args()
    if not args.demo:
        parser.print_help()
        return
    result = demo()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"저장: {args.out}")


if __name__ == "__main__":
    main()
