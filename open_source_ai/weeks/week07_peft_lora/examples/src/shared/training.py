"""질문·답변을 학습 입력으로 바꾼다. 마스킹 구현은 선택 심화에서 읽는다."""

import json

from shared import messages


def training_examples(tokenizer, path, max_length):
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if not rows:
        raise ValueError("학습 데이터가 비어 있습니다.")
    examples = []
    for number, row in enumerate(rows, 1):
        if not row["instruction"].strip() or not row["output"].strip():
            raise ValueError(f"{number}번째 질문과 답변을 모두 채우세요.")
        prompt = messages(row["instruction"])
        prompt_ids = tokenizer.apply_chat_template(prompt, add_generation_prompt=True)
        full_ids = tokenizer.apply_chat_template(prompt + [{"role": "assistant", "content": row["output"]}])
        if len(full_ids) > max_length:
            raise ValueError(f"{number}번째 예시가 {max_length}토큰보다 깁니다. 질문·답변을 줄이세요.")
        # 질문은 정답이 아니다. 답변 토큰만 loss 계산에 사용한다.
        labels = [-100] * len(prompt_ids) + full_ids[len(prompt_ids):]
        examples.append({"input_ids": full_ids, "attention_mask": [1] * len(full_ids), "labels": labels})
    print(f"학습 데이터: {len(rows)}건 / 첫 답변:\n{rows[0]['output']}")
    return examples
