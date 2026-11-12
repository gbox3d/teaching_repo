from shared import Board, chat, needle_predictor

# 한 함수 설명만 바꾼 뒤 같은 문장으로 관찰한다.
DESCRIPTIONS = {
    "turn_on": "Turn on one explicitly numbered LED (0 to 3). 켜기, 점등.",
}


def main():
    predict = needle_predictor(descriptions=DESCRIPTIONS)
    with Board() as board:
        chat(predict, board)
