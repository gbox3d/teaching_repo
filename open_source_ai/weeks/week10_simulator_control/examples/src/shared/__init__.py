from wleno.control.models import ollama_predict

MODEL = "qwen3.5:2b"


def predict(question):
    return ollama_predict(question, model=MODEL)
