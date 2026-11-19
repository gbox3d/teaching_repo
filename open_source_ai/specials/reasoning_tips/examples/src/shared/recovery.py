"""추론이 반복되면 스트림을 닫고 같은 질문의 본문을 한 번 이어 쓴다."""

import re
from collections import Counter
from contextlib import closing

from langchain_core.messages import AIMessage

import shared

REASONING_CHAR_LIMIT = 2048
SENTENCE_END = re.compile(r"[.!?。！？\n]+")


def repeats_sentence(thought):
    # 마지막 조각은 다음 청크에서 이어질 수 있으므로 끝난 문장만 센다.
    sentences = (" ".join(s.casefold().split()) for s in SENTENCE_END.split(thought)[:-1])
    counts = Counter(s for s in sentences if len(s) >= 20)
    return any(count >= 3 for count in counts.values())


def read_attempt(model, messages, limit):
    """한 요청을 읽고 (표시한 본문, 모은 추론, 중단 사유)를 반환한다."""
    answer_parts = []
    thought = ""
    leading_space = ""
    reason = "답변 본문 없이 생성이 끝났습니다."
    with closing(model.stream(messages)) as stream:
        for part in stream:
            text = part.text
            if not answer_parts:
                thinking = part.additional_kwargs.get("reasoning_content") if shared.REASONING else ""
                fragment = (thinking or "")[:limit - len(thought)]
                if fragment:
                    if not thought:
                        print("추론> ", end="")
                    print(fragment, end="", flush=True)
                    thought += fragment

                if not text.strip():
                    if thinking and len(thought) >= limit:
                        reason = "추론 글자 수 한도에 도달했습니다."
                        break
                    if fragment and SENTENCE_END.search(fragment) and repeats_sentence(thought):
                        reason = "같은 추론 문장이 세 번 나왔습니다."
                        break
                    leading_space += text
                    continue

                if thought and not thought.endswith("\n"):
                    print()
                print("AI> ", end="", flush=True)
                text = leading_space + text
            if text:
                shared.type_text(text)
                answer_parts.append(text)
    if answer_parts or (thought and not thought.endswith("\n")):
        print()
    return "".join(answer_parts), thought, reason


def answer_with_recovery(model, messages, *, limit=REASONING_CHAR_LIMIT):
    if shared.REASONING and limit < 1:
        raise ValueError("REASONING_CHAR_LIMIT에 1 이상의 글자 수를 지정하세요.")
    answer, thought, reason = read_attempt(model, messages, limit)
    if answer or not shared.REASONING:
        return answer

    if thought:
        # Qwen3.5의 Ollama 파서는 마지막 assistant 메시지의 줄바꿈을 본문 시작으로 읽는다.
        prefix = AIMessage(content="\n", additional_kwargs={"reasoning_content": thought})
        messages = [*messages, prefix]
        print(f"{reason} 수집한 추론 {len(thought):,}자에서 답변을 이어 씁니다.", flush=True)
    else:
        print(f"{reason} 같은 질문을 한 번 더 보냅니다.", flush=True)
    answer, _, _ = read_attempt(model, messages, limit - len(thought))
    return answer
