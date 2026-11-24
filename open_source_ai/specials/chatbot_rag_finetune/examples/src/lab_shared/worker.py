"""질문 문자열만 받는 JSON Lines 워커. 통신 규칙은 14주 shared.worker와 같다.
다른 점: 봇 모듈 이름을 첫 인수로 받아(파이썬 식별자만 허용) importlib로 불러 그 모듈의 answer를 쓴다.
그 모듈에 호출할 수 있는 answer가 없으면 워커를 끝내지 않고 질문마다 ok:false로 답한다."""

import importlib
import json
import sys

from shared import MAX_QUESTION_LENGTH, configure_utf8


def main() -> None:
    configure_utf8()
    if len(sys.argv) != 2 or not sys.argv[1].isidentifier():
        raise SystemExit("사용법: python -m lab_shared.worker <봇 모듈 이름>")
    bot = sys.argv[1]
    protocol_output = sys.stdout
    # 봇의 print와 import 때 출력을 프로토콜에서 분리한다.
    sys.stdout = sys.stderr
    # answer가 없다고 여기서 끝내면 채점기가 문항마다 워커를 다시 시작해 같은 traceback이 되풀이된다.
    answer = getattr(importlib.import_module(bot), "answer", None)

    for line in sys.stdin:
        try:
            question = json.loads(line)
            if type(question) is not str or not question.strip() or len(question) > MAX_QUESTION_LENGTH:
                raise ValueError("질문은 비어 있지 않은 길이 제한 내 문자열이어야 합니다.")
            if callable(answer):
                result = {"ok": True, "response": answer(question)}
            else:
                result = {"ok": False, "error": f"{bot}에 answer(question) 함수가 없습니다."}
            output = json.dumps(result, ensure_ascii=False, allow_nan=False)
        except Exception as exc:
            output = json.dumps({"ok": False, "error": f"{type(exc).__name__}: {exc}"[:1000]},
                                ensure_ascii=False)
        protocol_output.write(output + "\n")
        protocol_output.flush()


if __name__ == "__main__":
    main()
