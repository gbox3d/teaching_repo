"""새 실행에서 저장한 회귀 모델을 불러와 예측한다."""

import torch

from shared import MODEL_PATH, create_regression, predict_interactively


def main():
    if not MODEL_PATH.exists():
        print("저장한 모델이 없습니다. 먼저 uv run ex03으로 학습하세요.")
        return
    model = create_regression()
    weights = torch.load(MODEL_PATH, map_location="cpu", weights_only=True)
    model.load_state_dict(weights)
    model.eval()
    print("불러온 모델:", MODEL_PATH)
    predict_interactively(model)
