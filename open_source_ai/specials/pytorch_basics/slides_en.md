---
marp: true
theme: default
paginate: true
---

<!-- _class: lead -->

# Block 1 · 20 min talk
## Tensor Operations and Persistence

---

## 0–3 min · The Task

Enter numbers → create a tensor → calculate → save → exit → reload.

Models also use tensors for inputs, weights, and results.

---

## 3–6 min · Create and Calculate

Create `[2.0, 3.0]`. Adding 1 gives `[3, 4]`, multiplying by 2 gives `[4, 6]`, and the sum is 5.

---

## 6–9 min · Save the Result

`torch.save(result, TENSOR_PATH)` saves the doubled values to `outputs/tensor.pt`. Exit ex01 before loading.

---

## 9–12 min · Reload in Another Process

Run ex02 and enter the file path. `torch.load(..., map_location="cpu", weights_only=True)` restores `[4, 6]`; adding 1 gives `[5, 7]`.

---

## 12–16 min · Inspect Values and Properties

Shape `(2,)` means two values in one dimension. dtype is their numeric format; device is the compute device. Saving a new input overwrites the file.

---

## 16–20 min · Lab Handoff

[Block 1 lab](lab.md#1교시-실습--텐서-연산과-파일-저장). Save and reload two inputs. Lab: 30 minutes; break: 10 minutes.

---

<!-- _class: lead -->

# Block 2 · 20 min talk
## Train Regression on Small Data

---

## 0–3 min · Data and Prediction Target

Six fictional rows map hours 1–6 to scores 43, 51, 54, 62, 64, 72. Predict a numeric score for a new number of hours.

---

## 3–6 min · Use a Straight Line

`nn.Linear(1, 1)` represents score = weight × hours + bias: one numeric input, one numeric output.

---

## 6–9 min · Measure Error

MSE averages squared differences between predictions and targets. Training reduces error on this data.

---

## 9–12 min · Update Parameters

Clear previous gradients, compute current gradients, then update parameters. This is the update part of training.

---

## 12–16 min · Change One Condition

Compare 1000 and 20 epochs: MSE, fitted line, and prediction at 2.5 hours. Restore the default and save the final model.

---

## 16–20 min · Lab Handoff

[Block 2 lab](lab.md#2교시-실습--작은-데이터로-회귀-모델-학습). Inspect data, training, predictions, and saved weights. Lab: 30 minutes; break: 10 minutes.

---

<!-- _class: lead -->

# Block 3 · 20 min talk
## Predict with Saved Weights

---

## 0–3 min · Persist Learned Values

state_dict contains learned weights and bias. Save it to `outputs/regression.pt`.

---

## 3–6 min · Restore the Same Architecture

Create the same Linear(1, 1) architecture, load the state dictionary, and populate its parameters.

---

## 6–9 min · Predict without Retraining

ex04 has no training loop. Use eval and no_grad, then compare its prediction with the training process for the same input.

---

## 9–12 min · Inspect Out-of-Range Inputs

Training data covers 1–6 hours. A prediction at 10 hours exists but is not guaranteed to be accurate. Distinguish training error from performance on new data.

---

## 12–16 min · Files and Working Directory

Use the same project root. outputs contains runtime artifacts and is ignored by Git. If weights are missing, run ex03 first.

---

## 16–20 min · Lab Handoff

[Block 3 lab](lab.md#3교시-실습--모델을-불러와-예측). Reproduce predictions in a new process. Lab: 30 minutes; break: 10 minutes.
