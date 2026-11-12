"""질문 문자열만 받는 JSON Lines 워커. 정답 파일은 읽지 않는다."""

import json
import sys

from shared import MAX_QUESTION_LENGTH, configure_utf8


def main() -> None:
    configure_utf8()
    protocol_output = sys.stdout
    # 학생 함수의 print와 import 시 출력을 프로토콜에서 분리한다.
    sys.stdout = sys.stderr
    from student_bot import answer

    for line in sys.stdin:
        try:
            question = json.loads(line)
            if type(question) is not str or not question.strip() or len(question) > MAX_QUESTION_LENGTH:
                raise ValueError("질문은 비어 있지 않은 길이 제한 내 문자열이어야 합니다.")
            result = {"ok": True, "response": answer(question)}
            output = json.dumps(result, ensure_ascii=False, allow_nan=False)
        except Exception as exc:
            output = json.dumps({"ok": False, "error": f"{type(exc).__name__}: {exc}"[:1000]},
                                ensure_ascii=False)
        protocol_output.write(output + "\n")
        protocol_output.flush()


if __name__ == "__main__":
    main()
