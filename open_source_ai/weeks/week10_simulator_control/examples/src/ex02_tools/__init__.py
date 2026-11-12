from shared import Board, chat, predict


def main():
    with Board() as board:
        chat(predict, board)
