"""Transformers pipeline 첫 추론 — 2교시. 감성 분류(cls)와 텍스트 생성(gen)을
model=·revision=·device= 를 명시해 실행하고 로드·워밍업·추론 시간과 commit hash 를
outputs/pipeline-*.json 에 남긴다. 시간은 워밍업(첫 호출) 뒤 두 번째 호출을 잰다.

    uv run python pipeline_demo.py --task cls --device cpu            # GPU 는 --device cuda
    uv run python pipeline_demo.py --task gen --device cuda --max-new-tokens 120   # CPU 는 60 정도
    uv run python pipeline_demo.py --task gen --gen-revision <commit hash>       # revision 고정
    uv run python pipeline_demo.py --task gen --gen-revision 0000000             # 실패 경로 A
    uv run python pipeline_demo.py --task cls --cls-model 없는조직/없는모델       # 실패 경로 B(HF_HUB_OFFLINE=1)

종료 코드: 0 성공, 1 실패(장치 없음, 모델·revision 없음, 오프라인). 실패해도 outputs/ 에 error 를 남긴다.
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path
from typing import Any

from hf_env import cached_commit_hash, env, first_line, offline_mode, prepare_env, save_json

# 한국어 3 + 영어 2, 긍정·부정·중립 섞음. 실제 인물·기관 없음.
SAMPLE_SENTENCES = [
    "이 수업은 정말 재미있고 배울 것이 많다.",
    "설치가 자꾸 실패해서 시간을 다 날렸다.",
    "모델 카드에는 라이선스와 학습 데이터 항목이 있다.",
    "The lab instructions were clear and easy to follow.",
    "The download was slow and the error message was useless.",
]
DEFAULT_SYSTEM = "너는 오픈소스 AI 수업의 도우미다. 한국어로 세 문장 이내로 짧게 답한다."
DEFAULT_PROMPT = "공개 모델을 프로젝트에 쓰기 전에 확인할 것을 세 가지만 말해 줘."


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Transformers pipeline 분류·생성 실행과 시간 기록")
    parser.add_argument("--task", choices=["cls", "gen"], required=True, help="cls: 감성 분류 5문장, gen: 텍스트 생성 1건")
    parser.add_argument("--device", choices=["auto", "cpu", "cuda"], default="auto", help="auto 는 CUDA 가 있으면 cuda")
    parser.add_argument("--dtype", choices=["auto", "float32", "float16", "bfloat16"], default="auto", help="auto: gen+cuda 는 float16, 나머지는 float32")
    parser.add_argument("--cls-model", default=None, help="분류 모델 ID. 생략하면 HF_CLS_MODEL")
    parser.add_argument("--cls-revision", default=None, help="분류 모델 revision(commit hash 또는 브랜치)")
    parser.add_argument("--gen-model", default=None, help="생성 모델 ID. 생략하면 HF_TEXT_MODEL")
    parser.add_argument("--gen-revision", default=None, help="생성 모델 revision(commit hash 또는 브랜치)")
    parser.add_argument("--prompt", default=DEFAULT_PROMPT, help="생성 질문")
    parser.add_argument("--system", default=DEFAULT_SYSTEM, help="생성 시스템 메시지")
    parser.add_argument("--max-new-tokens", type=int, default=120, help="생성 최대 토큰 수")
    parser.add_argument("--outputs", default="outputs", help="결과 JSON 을 둘 폴더")
    parser.add_argument("--tag", default=None, help="출력 파일 이름 뒤에 붙일 짧은 표식")
    return parser


def pick_device(name: str, torch: Any) -> Any:
    if name == "auto":
        name = "cuda" if torch.cuda.is_available() else "cpu"
    if name == "cuda" and not torch.cuda.is_available():
        raise RuntimeError("CUDA 장치를 찾지 못했다 — torch.cuda.is_available() 가 False 다. --device cpu 로 진행하고, CUDA 태그·드라이버는 환경 기준표와 대조한다")
    return torch.device(name)


def sync(device: Any, torch: Any) -> None:
    if device.type == "cuda":  # GPU 는 비동기로 계산하므로 시간을 멈추기 전에 동기화한다
        torch.cuda.synchronize()


def load(task: str, model_id: str, revision: str | None, device: Any, dtype: Any, torch: Any) -> tuple[Any, float]:
    from transformers import AutoModelForCausalLM, AutoModelForSequenceClassification, AutoTokenizer, pipeline

    t0 = time.perf_counter()
    tokenizer = AutoTokenizer.from_pretrained(model_id, revision=revision)
    model_cls = AutoModelForSequenceClassification if task == "cls" else AutoModelForCausalLM
    model = model_cls.from_pretrained(model_id, revision=revision)
    model.to(device=device, dtype=dtype)  # dtype 인자 이름이 버전마다 달라 .to() 로 통일한다
    model.eval()
    pipe = pipeline("text-classification" if task == "cls" else "text-generation", model=model, tokenizer=tokenizer, device=device)
    sync(device, torch)
    return pipe, time.perf_counter() - t0


def run_cls(pipe: Any, device: Any, torch: Any) -> tuple[dict[str, Any], float, float]:
    t0 = time.perf_counter()
    pipe(SAMPLE_SENTENCES[0], truncation=True)  # 워밍업: 첫 호출은 커널 준비 시간이 섞인다
    sync(device, torch)
    warmup = time.perf_counter() - t0
    t1 = time.perf_counter()
    outputs = pipe(SAMPLE_SENTENCES, truncation=True)
    sync(device, torch)
    infer = time.perf_counter() - t1
    results = [{"text": s, "label": o["label"], "score": round(float(o["score"]), 4)} for s, o in zip(SAMPLE_SENTENCES, outputs)]
    return {"results": results, "id2label": dict(pipe.model.config.id2label)}, warmup, infer


def run_gen(pipe: Any, device: Any, torch: Any, system: str, prompt: str, max_new_tokens: int) -> tuple[dict[str, Any], float, float]:
    messages = [{"role": "system", "content": system}, {"role": "user", "content": prompt}]
    try:
        text = pipe.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    except (ValueError, AttributeError):  # chat template 이 없는 모델은 질문만 그대로 넣는다
        text = prompt
    kwargs = {"do_sample": False, "return_full_text": False}  # do_sample=False ≈ temperature 0
    t0 = time.perf_counter()
    pipe(text, max_new_tokens=2, **kwargs)
    sync(device, torch)
    warmup = time.perf_counter() - t0
    t1 = time.perf_counter()
    answer = pipe(text, max_new_tokens=max_new_tokens, **kwargs)[0]["generated_text"].strip()
    sync(device, torch)
    infer = time.perf_counter() - t1
    n_tokens = len(pipe.tokenizer(answer, add_special_tokens=False)["input_ids"])
    body = {
        "system": system,
        "prompt": prompt,
        "prompt_tokens": len(pipe.tokenizer(text, add_special_tokens=False)["input_ids"]),
        "answer": answer,
        "generated_tokens": n_tokens,
        "max_new_tokens": max_new_tokens,
        "tokens_per_second": round(n_tokens / infer, 2) if infer > 0 else None,
    }
    return body, warmup, infer


def explain(exc: BaseException, model_id: str, revision: str | None) -> str:
    name, text = exc.__class__.__name__, first_line(exc)
    if "CUDA 장치" in text:
        return text
    if "out of memory" in text.lower():
        return f"GPU 메모리 부족: {model_id} — --max-new-tokens 를 줄이거나 --dtype float16 을 쓴다 ({name})"
    if offline_mode():
        return f"오프라인 모드(HF_HUB_OFFLINE=1)에서 캐시에 없는 모델·revision 이다: {model_id}@{revision or 'main'} — precache.py 로 미리 받거나 .env 의 HF_HUB_OFFLINE 을 0 으로 되돌린다 ({name})"
    if revision:
        return f"모델 또는 revision 을 불러오지 못했다: {model_id}@{revision} — commit hash 철자를 Files and versions 탭·cache_report.py 출력과 대조한다 ({name}: {text})"
    return f"모델을 불러오지 못했다: {model_id} — 모델 ID 철자, 사전 캐시 여부, 네트워크를 확인한다 ({name}: {text})"


def main() -> int:
    prepare_env()
    args = build_parser().parse_args()
    import torch
    import transformers

    task = args.task
    model_id = (args.cls_model or env("HF_CLS_MODEL")) if task == "cls" else (args.gen_model or env("HF_TEXT_MODEL"))
    revision = args.cls_revision if task == "cls" else args.gen_revision
    record: dict[str, Any] = {"task": task, "model": model_id, "requested_revision": revision, "device": args.device, "dtype": args.dtype,
                              "offline": offline_mode(), "torch_version": torch.__version__, "transformers_version": transformers.__version__}
    try:
        device = pick_device(args.device, torch)
        dtype_name = args.dtype if args.dtype != "auto" else ("float16" if (device.type == "cuda" and task == "gen") else "float32")
        record.update(device=str(device), dtype=dtype_name)
        if device.type == "cuda":
            torch.cuda.reset_peak_memory_stats()
        pipe, load_s = load(task, model_id, revision, device, getattr(torch, dtype_name), torch)
        commit = getattr(pipe.model.config, "_commit_hash", None) or cached_commit_hash(model_id, revision)
        if task == "cls":
            body, warmup_s, infer_s = run_cls(pipe, device, torch)
        else:
            body, warmup_s, infer_s = run_gen(pipe, device, torch, args.system, args.prompt, args.max_new_tokens)
    except Exception as exc:
        message = explain(exc, model_id, revision)
        print(message, file=sys.stderr)
        record.update(error=message, error_type=exc.__class__.__name__)
        print(f"saved: {save_json(Path(args.outputs), 'pipeline', args.tag, record)}", file=sys.stderr)
        return 1

    vram = round(torch.cuda.max_memory_allocated() / 2**20, 1) if device.type == "cuda" else None
    record.update(commit_hash=commit, load_seconds=round(load_s, 3), warmup_seconds=round(warmup_s, 3), infer_seconds=round(infer_s, 3), max_vram_mb=vram, **body)
    print(f"task={task}  model={model_id}  commit={commit}  device={device}  dtype={dtype_name}")
    print(f"load {load_s:.2f}s  warmup {warmup_s:.2f}s  infer {infer_s:.2f}s  max_vram {vram} MB")
    if task == "cls":
        for r in body["results"]:
            print(f"  {r['label']:<10} {r['score']:.3f}  {r['text']}")
        print(f"  id2label = {body['id2label']}")
    else:
        print("---\n" + body["answer"] + "\n---")
        print(f"generated_tokens={body['generated_tokens']}  tokens/s={body['tokens_per_second']}")
    print(f"saved: {save_json(Path(args.outputs), 'pipeline', args.tag, record)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
