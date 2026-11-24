"""특강 예제의 공용 코드. 문항 세트를 읽고, 평가할 봇의 워커 명령을 만든다.
정답을 읽는 쪽은 평가·학습 예제뿐이다. 봇 코드에서는 load_set을 쓰지 않는다."""

import importlib.util
import json
import sys
from pathlib import Path

import shared

DATA_DIR = Path(__file__).parent / "data"
# 문항 세트 이름: (질문 파일, 정답 파일). public은 14주차 shared/data의 공개 20문항이다.
SETS = {
    "public": ("public_questions.json", "public_answers.json"),
    "mine": ("my_questions.json", "my_answers.json"),
    "train": ("train_questions.json", "train_answers.json"),
}


def load_set(name: str) -> tuple[list, list]:
    """문항 세트의 (질문 목록, 정답 목록)을 읽는다. 형식 검사는 14주 validate_dataset이 한다."""
    if name not in SETS:
        raise ValueError(f"문항 세트 이름은 {', '.join(SETS)} 중 하나여야 합니다: {name!r}")
    # 폴더는 부를 때마다 읽는다. 시험에서 DATA_DIR을 임시 폴더로 바꿔 쓴다.
    folder = shared.DATA_DIR if name == "public" else DATA_DIR
    questions_file, answers_file = SETS[name]
    questions = json.loads((folder / questions_file).read_text(encoding="utf-8"))
    answers = json.loads((folder / answers_file).read_text(encoding="utf-8"))
    return questions, answers


def worker_command(bot: str) -> list[str] | None:
    """평가 워커 명령. student_bot이면 None을 돌려 14주 공식 워커(shared.worker)를 그대로 쓴다."""
    if bot == "student_bot":
        return None
    # 모듈 위치만 찾고 import하지 않는다. 봇 코드는 워커 프로세스 안에서만 실행하고, answer가 있는지도 워커가 본다.
    if not bot.isidentifier() or importlib.util.find_spec(bot) is None:
        raise ValueError(f"BOT은 src 안에 있는 봇 패키지 이름이어야 합니다(예: rag_bot): {bot!r}")
    return [sys.executable, "-u", "-m", "lab_shared.worker", bot]
