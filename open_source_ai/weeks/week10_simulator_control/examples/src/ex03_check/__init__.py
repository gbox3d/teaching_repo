from wleno.control import Board, load_cases
from wleno.control.evaluation import evaluate

from shared import predict


def main():
    # 문항의 query는 모델에 보내고, calls는 채점할 때 정답으로 사용한다.
    cases = load_cases()
    print(f"고정 명령 {len(cases)}개로 모델의 함수 선택과 시뮬레이터 상태를 확인합니다.")
    with Board() as board:
        evaluate(predict, board, cases)
