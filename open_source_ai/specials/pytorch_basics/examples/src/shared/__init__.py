"""텐서·모델 저장 경로와 회귀 예제에서 함께 쓰는 함수를 모은다."""

import csv
from pathlib import Path

import torch
from torch import nn

TENSOR_PATH = Path("outputs/tensor.pt")
MODEL_PATH = Path("outputs/regression.pt")
DATA_PATH = Path(__file__).parent / "data/study_scores.csv"


def training_data():
    with DATA_PATH.open(encoding="utf-8", newline="") as source:
        rows = list(csv.DictReader(source))
    hours = torch.tensor([[float(row["hours"])] for row in rows])
    scores = torch.tensor([[float(row["score"])] for row in rows])
    return hours, scores


def create_regression():
    return nn.Linear(1, 1)


def predict_interactively(model):
    print("공부 시간을 입력하면 가상 연습 점수를 예측합니다. 종료: /bye")
    while True:
        text = input("시간> ").strip()
        if text == "/bye":
            break
        if not text:
            continue
        try:
            hours = float(text)
            if hours < 0:
                raise ValueError
        except ValueError:
            print("0 이상인 숫자를 입력하세요.")
            continue
        with torch.no_grad():
            prediction = model(torch.tensor([[hours]])).item()
        print(f"예측 점수: {prediction:.2f}")
