"""모델은 호출을 제안하며 실제 실행은 Board가 담당한다."""

import json
from copy import deepcopy
from threading import Lock

from . import DATA_DIR, http_json

TOOLS = json.loads((DATA_DIR / "tools.json").read_text(encoding="utf-8"))


def ollama_predict(question, model="qwen3.5:2b", url="http://127.0.0.1:11434/api/chat"):
    body = http_json(url, {
        "model": model,
        "messages": [
            {"role": "system", "content": "Use only the provided LED tools. LED indices are 0 to 3 and brightness is 0 to 255. Never guess missing indices or values. Unsupported, ambiguous, or invalid requests require no tool call. Each request is independent."},
            {"role": "user", "content": question},
        ],
        "tools": [{"type": "function", "function": tool} for tool in TOOLS],
        "stream": False, "think": False,
        "options": {"temperature": 0, "num_predict": 256},
    }, timeout=120)
    return [{"name": item["function"]["name"], "arguments": item["function"]["arguments"]}
            for item in body["message"].get("tool_calls", [])]


def needle_predictor(weights=None, descriptions=None):
    import cactus

    tools = deepcopy(TOOLS)
    for tool in tools:
        if descriptions and tool["name"] in descriptions:
            tool["description"] = descriptions[tool["name"]]
    agent = cactus.Cactus(tools=tools, weights=str(weights) if weights else None, auto_date=False)
    lock = Lock()

    def predict(question):
        with lock:
            agent.reset()  # 이전 질문의 문맥을 빼고 문항마다 독립적으로 비교한다.
            result = agent.complete(question, max_new_tokens=256)
        if not result.get("success"):
            raise RuntimeError(result.get("error") or "Needle 응답 실패")
        if result.get("validation", {}).get("ungrounded"):
            return []
        return result["function_calls"]

    return predict
