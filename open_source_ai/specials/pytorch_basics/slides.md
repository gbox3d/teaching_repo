---
marp: true
theme: default
paginate: true
---

<!-- _class: lead -->

# 1교시 · 설명 20분
## 텐서 연산과 파일 저장

---

## 0–3분 · 이번 시간의 작업

숫자 입력 → 텐서 생성 → 연산 → 저장 → 종료 → 복원.

모델의 입력·가중치·계산 결과도 텐서로 다룬다. 먼저 이 자료를 계산하고 보관한다.

---

## 3–6분 · 텐서를 만들고 연산한다

```python
tensor = torch.tensor([2.0, 3.0])
print(tensor + 1)
print(tensor * 2)
print(tensor.sum())
```

각 값에 연산을 적용한다. 결과는 `[3, 4]`, `[4, 6]`, `5`다.

---

## 6–9분 · 계산 결과를 저장한다

```python
result = tensor * 2
torch.save(result, TENSOR_PATH)
```

ex01은 `outputs/tensor.pt`에 2배 한 값을 저장한다. `/bye`로 종료한다.

---

## 9–12분 · 다른 실행에서 불러온다

```python
tensor = torch.load(filename, map_location="cpu", weights_only=True)
print(tensor + 1)
```

ex02에 파일 경로를 입력한다. `[4, 6]`을 읽고 `[5, 7]`을 계산한다.

---

## 12–16분 · 값과 속성을 확인한다

shape `(2,)`는 1차원 숫자 두 개, dtype `float32`는 숫자의 저장 형식, device는 계산 장치다.

다른 입력을 저장하면 같은 파일의 내용이 바뀐다. 텍스트 편집기 대신 torch.load로 확인한다.

---

## 16–20분 · 실습 인계

[1교시 실습](lab.md#1교시-실습--텐서-연산과-파일-저장)

`2 3`, `-1 4`로 저장·복원을 반복한다. 실습 30분 뒤 휴식 10분.

---

<!-- _class: lead -->

# 2교시 · 설명 20분
## 작은 데이터로 회귀 모델 학습

---

## 0–3분 · 예측할 값과 데이터

CSV 6행은 가상 공부 시간과 연습 점수다. 실제 학생 성적이 아니다.

시간 1·2·3·4·5·6에 점수 43·51·54·62·64·72가 있다. 목표는 새 시간의 점수를 숫자로 예측하는 것이다.

---

## 3–6분 · 직선 하나를 모델로 쓴다

```python
model = nn.Linear(1, 1)
```

`점수 = 가중치 × 시간 + 편향`이다. 입력 한 값에서 출력 한 값을 만든다.

---

## 6–9분 · 오차를 숫자로 잰다

```python
predictions = model(hours)
loss = nn.MSELoss()(predictions, scores)
```

MSE는 예측과 정답의 차이를 제곱해 평균한 값이다. 학습 자료의 오차를 줄인다.

---

## 9–12분 · 가중치를 갱신한다

```python
optimizer.zero_grad()
loss.backward()
optimizer.step()
```

이전 기울기를 비우고, 이번 기울기를 계산하고, 가중치를 바꾼다.

---

## 12–16분 · 한 조건만 바꿔 비교한다

ex03의 EPOCHS를 1000에서 20으로 바꿔 MSE·회귀식·2.5시간의 예측을 비교한다.

기본 설정으로 복원해 마지막 모델을 다시 저장한다.

---

## 16–20분 · 실습 인계

[2교시 실습](lab.md#2교시-실습--작은-데이터로-회귀-모델-학습)

CSV → 학습 → 예측 → 가중치 저장을 확인한다. 실습 30분 뒤 휴식 10분.

---

<!-- _class: lead -->

# 3교시 · 설명 20분
## 저장한 모델로 예측

---

## 0–3분 · 학습한 값을 보관한다

```python
torch.save(model.state_dict(), MODEL_PATH)
```

state_dict는 학습한 가중치·편향을 담는다. 이 예제의 파일은 `outputs/regression.pt`다.

---

## 3–6분 · 같은 모델 구조에 채운다

```python
model = create_regression()
weights = torch.load(MODEL_PATH, weights_only=True)
model.load_state_dict(weights)
```

파일에서 읽은 값을 같은 Linear(1, 1) 구조에 채운다.

---

## 6–9분 · 다시 학습하지 않고 계산한다

```python
model.eval()
with torch.no_grad():
    prediction = model(new_hours)
```

ex04에는 학습 루프가 없다. 같은 입력의 예측을 ex03과 비교한다.

---

## 9–12분 · 학습 범위 밖을 살펴본다

자료는 1~6시간이다. 10시간도 숫자는 나오지만 그 값이 정확하다고 보장할 수 없다.

학습 자료에 맞춘 오차와 새 자료에서의 품질을 구분한다.

---

## 12–16분 · 파일과 실행 위치

명령은 같은 프로젝트 루트에서 실행한다. outputs는 실행 결과이며 Git에 넣지 않는다.

없는 모델 파일이면 ex03부터 실행한다. 숫자 입력은 빈 줄·문자를 구분해 처리한다.

---

## 16–20분 · 실습 인계

[3교시 실습](lab.md#3교시-실습--모델을-불러와-예측)

같은 모델의 예측을 새 실행에서 재현한다. 실습 30분 뒤 휴식 10분.
