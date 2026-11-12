from shared import Board, chat, needle_predictor


def main():
    predict = needle_predictor()
    with Board() as board:
        chat(predict, board)
