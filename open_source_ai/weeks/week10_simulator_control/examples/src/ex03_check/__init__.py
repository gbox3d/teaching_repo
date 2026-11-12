from shared import Board, evaluate, load_cases, predict


def main():
    with Board() as board:
        evaluate(predict, board, load_cases())
