"""가상 공부 시간·점수 데이터로 선형 회귀 모델을 학습하고 저장한다."""

import torch
from torch import nn

from shared import MODEL_PATH, create_regression, predict_interactively, training_data

EPOCHS = 1000
LEARNING_RATE = 0.02


def main():
    torch.manual_seed(42)
    hours, scores = training_data()
    model = create_regression()
    loss_function = nn.MSELoss()
    optimizer = torch.optim.SGD(model.parameters(), lr=LEARNING_RATE)
    print("설명용 가상 자료: 공부 시간 1~6시간, 연습 점수")
    for epoch in range(EPOCHS):
        predictions = model(hours)
        loss = loss_function(predictions, scores)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        if epoch == 0 or (epoch + 1) % 200 == 0:
            print(f"epoch={epoch + 1}, MSE={loss.item():.4f}")
    print(f"학습한 식: 점수 = {model.weight.item():.3f} × 시간 + {model.bias.item():.3f}")
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    torch.save(model.state_dict(), MODEL_PATH)
    print("학습한 가중치를 저장했습니다:", MODEL_PATH)
    model.eval()
    predict_interactively(model)
