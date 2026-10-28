"""입력한 숫자를 텐서로 계산하고 두 배 한 결과를 파일로 저장한다."""

import torch

from shared import TENSOR_PATH


def main():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print("사용 장치:", device)
    print("숫자 두 개를 공백으로 구분해 입력하세요. 종료: /bye")
    while True:
        text = input("숫자> ").strip()
        if text == "/bye":
            break
        if not text:
            continue
        try:
            values = [float(value) for value in text.split()]
            if len(values) != 2:
                raise ValueError
        except ValueError:
            print("예: 2 3 처럼 숫자 두 개를 입력하세요.")
            continue
        tensor = torch.tensor(values, dtype=torch.float32, device=device)
        print("텐서:", tensor)
        print("shape:", tuple(tensor.shape), "dtype:", tensor.dtype, "device:", tensor.device)
        print("각 값에 1 더하기:", tensor + 1)
        result = tensor * 2
        print("각 값에 2 곱하기:", result)
        print("합계:", tensor.sum().item())
        TENSOR_PATH.parent.mkdir(parents=True, exist_ok=True)
        torch.save(result, TENSOR_PATH)
        print("2배 한 결과를 저장했습니다:", TENSOR_PATH)
