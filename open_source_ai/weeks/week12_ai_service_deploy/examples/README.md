# 12주차 예제 Needle3 데이터·학습·복원

주차 `examples/`의 uv 프로젝트 하나를 세 교시가 함께 사용한다. `period1`~`period3`에는 실행 순서 안내만 둔다. 코드·학습 데이터·설정·산출물을 교시마다 복사하거나 새 프로젝트로 나누지 않는다.

## 전체 저장소에서 실행

Python 3.12를 사용한다. 처음 받는 경우 개인 작업 위치에서 다음을 실행한다. 이미 clone했다면 기존 저장소의 같은 위치로 이동한다.

```powershell
git clone https://github.com/gbox3d/teaching_repo.git
Set-Location teaching_repo/open_source_ai/weeks/week12_ai_service_deploy/examples
uv sync
uv run ex01
```

`tools/bleuno-control`의 `src/bleuno_control` 로컬 의존성 때문에 `examples/`만 복사하면 안 된다. 엔진·기본 추론 모델·학습용 체크포인트·학습 의존성은 수업 전에 준비한다. 수업의 의존성은 `cactus-compute[train]==4.2.0`이다. Metal·CUDA 등 다른 환경은 수업 전에 준비·점검한다. Mac arm64 CPU 실측은 [주차 안내](../README.md)에서 확인한다.

## 교시별 명령과 결과

| 교시 | 안내 | 같은 프로젝트에서 실행 | 확인할 결과 |
|---|---|---|---|
| 1교시 | [데이터 점검과 대화](period1/README.md) | `uv run ex01` | 정답 호출 수정 이유, 실제 입력·호출 관찰 |
| 2교시 | [LoRA 학습과 저장](period2/README.md) | `uv run ex02` | 실제 학습 설정·loss, `adapter.safetensors`, `tuned.cact` |
| 3교시 | [새 프로세스 복원·비교](period3/README.md) | `uv run ex03` | 동일 미학습 문항의 학습 전후 호출·오류 분석 |

대화는 입력·호출 확인·다음 입력을 반복하고 빈 입력은 건너뛰고 `/bye`로 종료한다. 반복 입력과 문맥 유지는 다르다. 제공 예제는 모델 인스턴스를 재사용하고 입력마다 이력을 초기화한다. 앞 문맥을 참조하는 명령에는 필요한 정보를 다시 적는다.

## 소스 읽기와 패키지 역할

`pyproject.toml`의 `[project.scripts]`에서 `ex01`, `ex02`, `ex03`가 가리키는 `<패키지>:main`을 읽고 `src/`의 해당 패키지를 연다. `main()`은 실행 시작 함수이며 `[build-system]`의 `uv_build`는 패키지 빌드·설치 방법이다. scripts를 바꾸면 `uv sync`로 설치된 명령을 갱신한다. 단순히 파일을 저장하는 것만으로 새 명령이 등록되지는 않는다.

학습 설정은 학습 모듈 맨 위 `EPOCHS`, `BATCH_SIZE`, `MAX_LEN`, `LEARNING_RATE`에서 바꾼다. 데이터와 산출 경로는 `src/shared/__init__.py`의 `DATA_FILE`, `MODELS_DIR`을 읽어 확인한다. 실행 옵션이나 별도 설정 파일을 늘리지 않는다.

배포 예제 밖에서 `uv init --package --python 3.12 --vcs none week12-package-check`를 한 번 실행해 `.python-version`, `pyproject.toml`, `src/`를 확인한다. 구조 확인 뒤 원래 예제로 돌아온다. [실습지](../lab.md)에 절차와 시간 배분이 있다.

## 호출과 산출물 계약

함수는 `turn_on(index)`, `turn_off(index)`, `set_brightness(index, value)`, `read_environment()`다. `index`는 정수 0~3, `value`는 정수 0~255다. 실행기는 모델 제안의 함수 허용 목록과 인자 이름·타입·범위를 검사하고 실행 뒤 `GET /state`를 확인한다. 형식과 의도는 별도로 판단한다. 센서값은 함수 반환에서 읽는다.

TCP는 대화·세션 동안 한 번 연결하고 유지한다. 연결 해제 시 LED가 초기화된다. 같은 조건 비교에서는 상태를 맞추며, 문항 사이 이력 초기화와 연결 해제를 혼동하지 않는다.

`adapter.safetensors`는 LoRA 변화량이고 `tuned.cact`는 기본 가중치와 병합한 추론 파일이다. 기본 체크포인트는 별도로 필요하다. `weights=`에는 `.cact`를 지정한다. 전후 비교는 기본·학습 모두 4bit·20L로 맞추며 일반 배포 기본 2bit 모델과 구분한다. 로컬 LoRA의 `confidence`는 `None`일 수 있다.

## 실제 모듈·데이터·산출 경로

| 명령·자료 | 위치 |
|---|---|
| `uv run ex01` | [src/ex01_data/__init__.py](src/ex01_data/__init__.py)의 `main()` |
| `uv run ex02` | [src/ex02_train/__init__.py](src/ex02_train/__init__.py)의 `main()` |
| `uv run ex03` | [src/ex03_restore/__init__.py](src/ex03_restore/__init__.py)의 `main()` |
| 주차 공용 경로 | [src/shared/__init__.py](src/shared/__init__.py)의 `DATA_FILE`, `MODELS_DIR` |
| 학생이 수정할 원본 | [src/shared/data/train_examples.jsonl](src/shared/data/train_examples.jsonl), 48개 `query`·`answers`·`reasoning` |
| 학습용 결합 파일 | `models/training_input.jsonl`, 공용 도구 스키마를 합친 학습 입력 |
| 학습 어댑터 | `models/adapter.safetensors` |
| 기본 비교용 어댑터 | `models/baseline_adapter.safetensors`, B=0으로 기본 가중치 유지 |
| 비교용 추론 파일 | `models/baseline.cact`, `models/tuned.cact`, 모두 4bit·20L |
| 기본 체크포인트 | `models/checkpoints/needle3.safetensors` |

원본 48행에는 공용 도구 스키마를 반복해서 넣지 않는다. `ex02`가 스키마를 합쳐 `models/training_input.jsonl`을 만든다. 이 파일은 명령 예제에 공통 도구 설명을 합친 학습 입력이다. 복잡한 내보내기는 공용 제공 함수가 처리하므로 학생은 학습 데이터와 상수를 수정한다.

실측에 사용한 시작값은 `EPOCHS=4`, `BATCH_SIZE=4`, `MAX_LEN=1024`, `LEARNING_RATE=1e-4`이며 데이터·실행 환경에 맞춰 조정할 수 있다. `MAX_LEN`은 모든 학습 예제의 렌더링 길이를 검사하는 한도다. 최장 토큰 길이가 한도를 넘으면 학습을 중단한다. 초과한 예제를 잘라서 학습하는 설정으로 사용하지 않는다.

평가는 16문항(한국어 8·영어 8, 호출 10·무호출 6)이며 학습 48개와 문자열이 다르다. 문자열이 다르다는 사실만으로 의미 독립성까지 증명할 수는 없다. 매 문항 LED를 `[0, 64, 128, 255]`로 복원한다. 함수 정확도, 호출 완전일치(호출 목록 순서·인자 값 포함), 실제 상태 성공, 오호출률, median·p95를 읽는다. 인자 이름·값의 대응과 함수 호출 목록의 순서를 대조하며 JSON 딕셔너리 키 나열 순서를 평가하지 않는다. 지연 출력은 초 단위이며 분모는 전체 16문항·무호출 6문항으로 구분한다.

## 수업 전 준비와 실패 확인

시뮬레이터의 TCP 제어와 HTTP `GET /state`를 준비한다. `ex01`은 기본 배포 모델의 대화이고 `ex03`는 저장한 두 4bit·20L 모델의 16문항 비교다. Mac arm64 CPU의 학습·저장·복원 실측은 [주차 안내](../README.md)를 참고한다. 자신의 실행 환경에서도 수업 전에 명령을 점검한다.

명령이 없으면 `[project.scripts]`와 `uv sync`, 데이터 오류는 `DATA_FILE`, 모델 로드 오류는 `MODELS_DIR`의 두 `.cact`와 엔진 버전을 확인한다. 전체 절차와 오류 위치는 [따라하기](../walkthrough.md)를 따른다.
학습이 중단되거나 두 모델의 저장이 끝나지 않으면 복원 명령이 실행을 막는다. 오류 원인을 해결한 뒤 `uv run ex02`를 다시 실행한다. 평가 문장과의 중복 검사는 학습 직전에도 수행한다.

## 공식 근거

[Fine-tuning Needle](https://cactuscompute.com/blog/finetuning-needle), [Needle Python Docs](https://cactuscompute.com/blog/needle-python-docs)를 참고한다. 함수 계약·명령·시간 구성은 수업 설계다. [따라하기](../walkthrough.md)와 [실습지](../lab.md)의 순서대로 진행한다.
