from shared import Board, DATA_FILE, chat, load_cases, needle_predictor, read_training


def main():
    rows = read_training(DATA_FILE)
    overlap = {r["query"] for r in rows} & {r["query"] for r in load_cases()}
    if overlap:
        raise ValueError("학습과 평가에 같은 문장이 있습니다: " + str(overlap))
    print(f"학습 {len(rows)}개, 무호출 {sum(not r['answers'] for r in rows)}개")
    print("첫 학습 예:", rows[0])
    predict = needle_predictor()
    with Board() as board:
        chat(predict, board)
