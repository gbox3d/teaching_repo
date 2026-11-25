from wleno.control import Board, chat

from shared import predict


def main():
    with Board() as board:
        chat(predict, board)
