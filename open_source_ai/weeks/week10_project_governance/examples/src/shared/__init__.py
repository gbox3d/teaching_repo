from bleuno_control import Board, chat, load_cases
from bleuno_control.models import ollama_predict
from bleuno_control.evaluation import evaluate

MODEL = "qwen3.5:2b"


def predict(question):
    return ollama_predict(question, model=MODEL)
