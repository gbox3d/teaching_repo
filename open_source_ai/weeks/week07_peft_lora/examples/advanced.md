# 선택 심화 — LoRA 내부 확인

기본 실습의 저장·복원·전후 비교를 마친 뒤 읽는다. 아래 활동은 필수 완료 조건이 아니다.

## rank와 학습 파라미터

LoRA는 원래 가중치 W를 고정하고 작은 행렬 A와 B로 만든 변화를 더한다.

```text
y = W x + (alpha / r) B A x
A: (r, in) / B: (out, r)
추가 파라미터 수: r × (in + out)
```

이 예제는 `q_proj`, `v_proj`에만 붙이고 `alpha = 2 × RANK`로 둔다. 이는 수업의 고정 설정이며 모든 모델의 최적 설정은 아니다. `RANK`를 4 또는 16으로 바꿀 때는 다른 조건을 유지하고 공용 `ADAPTER_DIR`도 새 이름으로 바꾼다. `print_trainable_parameters()`의 수와 같은 질문의 답을 비교한다. rank가 크다고 항상 답이 나아지지 않는다.

## 메모리 관찰

원래 가중치, 학습하는 부분의 그래디언트·옵티마이저 상태, 중간 계산값이 메모리를 쓴다. LoRA는 학습할 파라미터 수를 줄여도 기본 모델을 메모리에 불러와야 한다. 길이와 배치도 메모리에 영향을 준다.

기본 코드는 CPU·CUDA·MPS에서 같은 저장·복원 흐름을 보여 주기 위해 float32를 쓴다. 작은 어댑터 파일의 크기만으로 필요한 VRAM을 계산하지 않는다. GPU 도구나 작업 관리자로 관찰하고 실제 사용량과 예측을 구분한다. bf16·QLoRA 설정은 별도 확장이다.

## 답변만 학습하는 마스킹

[shared/training.py](src/shared/training.py)의 `training_examples()`를 읽는다. 동일한 chat template로 질문까지의 토큰과 정답까지의 토큰을 만든다.

```text
입력: [system] [질문] [assistant 시작] [정답] [끝 토큰]
라벨: [-100 … 질문 부분은 제외 …] [정답] [끝 토큰]
```

`-100`은 loss 계산에서 제외하는 값이다. 질문을 정답으로 채점하지 않고 제공한 답변 부분을 학습한다. 패딩 라벨도 같은 값으로 가린다. 길이가 넘으면 조용히 답변을 잘라 버리지 않고 오류로 알려 준다. 다른 모델의 템플릿으로 변경할 때는 질문 접두부와 정답의 경계가 맞는지 다시 확인한다.

## 병합과 실행기 변경

`merge_and_unload()`는 학습한 변화를 기본 가중치에 합친다. 어댑터를 붙인 모델과 병합 모델은 같은 변화를 담지만 계산 정밀도에 따라 출력 차이가 생길 수 있다. Ollama의 양자화·템플릿·생성 설정까지 달라지면 전후 비교 조건이 더 바뀐다. 학습 효과는 `ex04`, 배포 동작은 Ollama 실행으로 나눠 확인한다.

- [PEFT LoRA 설정](https://huggingface.co/docs/peft/package_reference/lora)
- [Transformers chat template](https://huggingface.co/docs/transformers/chat_templating)
- [Ollama 가져오기](https://docs.ollama.com/import)
