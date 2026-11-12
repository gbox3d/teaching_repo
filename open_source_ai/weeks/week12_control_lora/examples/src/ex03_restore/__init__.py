from shared import Board, MODELS_DIR, evaluate, load_cases, needle_predictor, trained_path


def main():
    paths = [trained_path(MODELS_DIR, name) for name in ("baseline.cact", "tuned.cact")]
    with Board() as board:
        for path in paths:
            print("\n비교 모델:", path.name, "(20층, 4비트, confidence 없음)")
            evaluate(needle_predictor(path), board, load_cases())
