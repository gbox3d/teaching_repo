from shared import Board, MODELS_DIR, chat, needle_predictor, trained_path

# 설명을 바꾼 실험은 같은 설명의 학습 전후 비교와 따로 기록한다.
DESCRIPTIONS = {}


def main():
    path = trained_path(MODELS_DIR)
    predict = needle_predictor(path, descriptions=DESCRIPTIONS)
    with Board() as board:
        chat(predict, board)
