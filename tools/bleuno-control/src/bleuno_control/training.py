"""cactus-compute 4.2.0의 로컬 학습 API를 호출하는 제공 코드."""

import json
from pathlib import Path
from types import SimpleNamespace

from . import load_cases, validate_calls
from .models import TOOLS


def read_training(path):
    rows = [json.loads(line) for line in Path(path).read_text(encoding="utf-8").splitlines() if line.strip()]
    queries = set()
    for row in rows:
        if not isinstance(row.get("query"), str) or not row["query"].strip():
            raise ValueError("학습 문장의 query가 비어 있습니다.")
        if row["query"] in queries:
            raise ValueError("같은 학습 질문이 중복되었습니다.")
        queries.add(row["query"])
        validate_calls(row["answers"])
    if len(rows) < 10:
        raise ValueError("검증 분리를 위해 학습 예제를 10개 이상 준비하세요.")
    return rows


def train(source, output, epochs=4, batch_size=4, max_len=1024, learning_rate=1e-4):
    rows = read_training(source)
    overlap = {row["query"] for row in rows} & {case["query"] for case in load_cases()}
    if overlap:
        raise ValueError("학습과 평가에 같은 문장이 있습니다: " + str(sorted(overlap)))
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    # 중단된 학습의 파일이 이전 결과와 섞여 사용되지 않도록 표시한다.
    marker = output / ".training-in-progress"
    marker.write_text("학습·내보내기 진행 중\n", encoding="utf-8")

    import numpy as np
    from cactus.model.finetune import finetune_local, render_example
    from cactus.model.run import load_checkpoint
    from cactus.model.tokenizer import get_tokenizer
    from cactus.model.checkpoints import read_adapter, write_adapter
    from cactus.model.build import build_main

    checkpoint = output / "checkpoints" / "needle3.safetensors"
    _, config = load_checkpoint(str(checkpoint))
    tokenizer = get_tokenizer(config.vocab_size)
    rows = [dict(row, tools=TOOLS) for row in rows]
    longest = max(sum(len(tokenizer.encode(text)) for text in render_example(row)) + 2 for row in rows)
    print(f"학습 데이터 {len(rows)}개, 가장 긴 문장 {longest}토큰, 제한 {max_len}토큰")
    if longest > max_len:
        raise ValueError("학습 예제가 잘릴 수 있습니다. MAX_LEN을 늘리거나 문장을 줄이세요.")
    dataset = output / "training_input.jsonl"
    dataset.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n", encoding="utf-8")
    adapter_path = output / "adapter.safetensors"
    args = SimpleNamespace(checkpoint=str(checkpoint), jsonl_path=str(dataset),
                           epochs=epochs, batch_size=batch_size, max_len=max_len,
                           lr=learning_rate, lora_rank=16, lora_alpha=32,
                           val_split=0.125, seed=0, checkpoint_dir=str(output / "checkpoints"),
                           out=str(adapter_path), generate=0, score=False)
    finetune_local(args)
    # B=0인 어댑터는 가중치를 바꾸지 않는다. 기본·학습 모델 모두 같은 4비트로 내보낸다.
    zero = read_adapter(str(adapter_path))
    for values in zero["lora"].values():
        values["B"] = np.zeros_like(values["B"])
    zero_path = output / "baseline_adapter.safetensors"
    write_adapter(str(zero_path), zero)
    for adapter, filename in [(zero_path, "baseline.pending.cact"), (adapter_path, "tuned.pending.cact")]:
        build_main(SimpleNamespace(checkpoint=str(checkpoint), lora=str(adapter),
                                   out=str(output / filename), layers=20, platform=None, upload=False))
    for name in ("baseline", "tuned"):
        (output / f"{name}.pending.cact").replace(output / f"{name}.cact")
    marker.unlink()
    print("저장 완료: baseline.cact, tuned.cact. 다음에는 같은 평가 문항으로 비교하세요.")


def trained_path(directory, filename="tuned.cact"):
    """이전 파일이 남았더라도 중단된 학습 결과는 읽지 않는다."""
    directory = Path(directory)
    if (directory / ".training-in-progress").exists():
        raise RuntimeError("학습 또는 저장이 완료되지 않았습니다. 12주차 uv run ex02를 다시 실행하세요.")
    for name in ("baseline.cact", "tuned.cact"):
        if not (directory / name).is_file():
            raise FileNotFoundError("먼저 12주차 uv run ex02로 모델 두 개를 저장하세요.")
    return directory / filename
