from shared import Board, MODEL, evaluate, load_cases, needle_predictor, ollama_predict


def main():
    predictors = [
        ("Ollama " + MODEL, lambda question: ollama_predict(question, model=MODEL)),
        ("Needle 3 배포본", needle_predictor()),
    ]
    with Board() as board:
        for name, predict in predictors:
            print("\n모델:", name)
            evaluate(predict, board, load_cases())
