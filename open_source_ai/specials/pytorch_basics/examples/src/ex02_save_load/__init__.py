"""앞 프로그램에서 저장한 텐서를 읽어 다시 계산한다."""

import torch

from shared import TENSOR_PATH


def main():
    print("ex01에서 저장한 파일:", TENSOR_PATH)
    print("불러올 파일 경로를 입력하세요. 종료: /bye")
    while True:
        filename = input("파일> ").strip()
        if filename == "/bye":
            break
        if not filename:
            continue
        try:
            tensor = torch.load(filename, map_location="cpu", weights_only=True)
        except FileNotFoundError:
            print("파일이 없습니다. 먼저 uv run ex01로 저장하고 경로를 확인하세요.")
            continue
        print("불러온 텐서:", tensor)
        print("shape:", tuple(tensor.shape), "dtype:", tensor.dtype, "device:", tensor.device)
        print("불러온 값에 1 더하기:", tensor + 1)
