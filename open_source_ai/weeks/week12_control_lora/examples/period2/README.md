# 12주차 2교시 짧은 로컬 LoRA 학습과 저장

[실습지](../../lab.md) · [예제 전체 안내](../README.md) · [따라하기](../../walkthrough.md)

## 실행 위치와 소스

1교시와 같은 `open_source_ai/weeks/week12_control_lora/examples` 프로젝트에서 이어 간다. 이 `period2/`로 소스나 환경을 복사하지 않는다. `[project.scripts]`의 `ex02_train:main`과 [src/ex02_train/__init__.py](../src/ex02_train/__init__.py)를 읽는다.

```powershell
uv run ex02
```

공식 cactus 컴포넌트로 학습·내보내기를 수행한다. 의존성은 `cactus-compute[train]==4.2.0`이다. 학습 원본은 `src/shared/data/train_examples.jsonl`이다. 공용 함수가 스키마를 합친 `models/training_input.jsonl`을 만들며 이 파일은 평가 결과가 아닌 학습 입력이다. 산출 경로와 실패 시 확인 위치는 [전체 안내](../README.md)를 따른다. Mac arm64 CPU 실측은 [주차 안내](../../README.md)를 참고하고 Metal·CUDA 등 다른 환경은 수업 전에 확인한다.

## 실습 순서

30분의 세부 시간은 [실습지](../../lab.md)가 정본이다.

| 순서 | 읽거나 실행할 것 | 확인할 근거 |
|---|---|---|
| 설정 | 학습 모듈 맨 위 `EPOCHS`, `BATCH_SIZE`, `MAX_LEN`, `LEARNING_RATE` | 실제 값과 선택 이유 |
| 길이 | 도구 정의·reasoning·정답 호출을 포함한 렌더링 | 모든 예제의 최장 토큰 길이와 초과 여부 |
| 학습 | `uv run ex02` | 실제 loss 변화, 완료 또는 실패 위치 |
| 저장·내보내기 | `adapter.safetensors`, `tuned.cact` | 두 파일의 실제 위치와 생성 확인 |

현재 초기값은 `EPOCHS=4`, `BATCH_SIZE=4`, `MAX_LEN=1024`, `LEARNING_RATE=1e-4`이며 데이터·실행 환경에 맞춰 조정할 수 있다. 모든 렌더링 예제의 최장 토큰 길이를 학습 전에 검사하고 `MAX_LEN` 초과 시 중단한다.

`models/adapter.safetensors`는 LoRA 변화량이다. 내보내기는 기본 체크포인트와 변화량을 병합해 추론용 `models/tuned.cact`를 만든다. 공용 함수는 B=0인 `models/baseline_adapter.safetensors`와 기본 4bit·20L의 `models/baseline.cact`도 만든다. B=0 어댑터는 기본 가중치를 바꾸지 않는다. 기본 체크포인트는 `models/checkpoints/needle3.safetensors`다. 어댑터 파일을 추론 API의 `weights=`에 바로 넣지 않는다. 파일명을 바꾸는 것으로 형식을 변환할 수 없다.

loss 감소와 미학습 문항 성공은 별도로 확인한다. 관찰하지 않은 학습 시간·성공률은 적지 않는다. 실습 시간이 끝나도 학습이 진행 중이면 그 상태를 기록한다. 사전 준비 산출물을 썼다면 자기 학습 결과와 구분한다.

## 다음 교시에 넘길 내용

수정 데이터와 실제 상수, 길이 점검, loss 관찰, 어댑터·`.cact`의 실제 저장 위치를 보존한다. 내보내기 실패는 저장 성공과 구분한다. 학습 프로세스를 종료한 뒤 3교시 `uv run ex03`의 새 프로세스에서 복원한다. scripts 자체를 고친 경우에는 먼저 `uv sync`를 다시 실행한다.
