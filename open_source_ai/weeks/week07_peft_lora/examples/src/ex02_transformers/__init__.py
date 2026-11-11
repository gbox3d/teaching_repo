"""같은 질문 입력을 유지하며, Python에서 학습용 작은 모델을 직접 실행한다."""

from shared import SYSTEM_PROMPT, answer, load_model, questions

PROMPT = SYSTEM_PROMPT  # 실습: ex01과 같은 형식 지시를 덧붙여 0.5B 모델도 따르는지 본다.


def main():
    tokenizer, model = load_model()
    for question in questions():
        print("AI>", answer(model, tokenizer, question, PROMPT))
