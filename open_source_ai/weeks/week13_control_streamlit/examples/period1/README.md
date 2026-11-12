# 13주차 1교시: 같은 조건의 학습 전후 제어 평가

[실습 문제와 시간표](../../lab.md#1교시-실습-학습-전후-제어-평가) · [예제 색인](../README.md)

## 이어받는 자료

12주차의 `tuned.cact`와 비교용 기본 4bit·20층 모델을 사용한다. `adapter.safetensors`는 LoRA 변화량이며 바로 추론에 넣는 `.cact`와 다르다. 배포 기본 2bit를 비교 기준으로 섞지 않는다. `shared.MODELS_DIR`이 가리키는 12주차 `examples/models/baseline.cact`와 `tuned.cact`를 읽으므로 모델 복사는 필요 없다.

## 실행 위치와 명령

`teaching_repo` 전체 clone의 `open_source_ai/weeks/week13_control_streamlit/examples`에서 실행한다. 이 `period1/` 폴더는 안내만 담는다.

```sh
uv sync
uv run ex01
```

[ex01_evaluate](../src/ex01_evaluate/__init__.py)가 16문항을 순차 자동 처리한다. 대화 입력 반복이 아니다. 공용 도구·생성 조건은 [models.py](../../../../../tools/bleuno-control/src/bleuno_control/models.py), 초기 상태와 지표는 [evaluation.py](../../../../../tools/bleuno-control/src/bleuno_control/evaluation.py)에서 확인한다. 초기 LED `[0, 64, 128, 255]`를 매 문항 다시 설정하고 `GET /state`로 읽는다. 기본·학습 모델 모두 같은 미학습 문항과 독립 대화 조건을 사용한다.

## 관찰할 내용

예상 호출, 모델의 호출 제안, 검증 통과 여부, 함수 반환, 실제 상태를 나란히 적는다. 함수 선택이 맞아도 인자가 틀릴 수 있고, 형식이 맞아도 의도가 틀릴 수 있다. 센서값은 함수 반환을 근거로 판단한다. 호출 없는 정답 문항에서 불필요한 제어가 발생했는지도 확인한다.

평가 문항은 한국어 8·영어 8, 호출 10·무호출 6이다. 학습 48개와 정확 문자열이 다르지만 의미 독립성까지 증명한 것은 아니다. 교재 준비 과정의 결과는 [실측 표](../../README.md#수업-준비-환경의-단일-실측)에서 읽는다. 실측하지 않은 성공률·시간은 채우지 않는다. 실행 실패를 분모에서 제외해 성공률을 높이지 않는다. 터미널 출력은 2교시 오류 분석에 이어 쓴다.

## 종료와 장애

평가가 끝나면 TCP 연결을 해제한다. 연결 해제 시 LED 초기화와 다음 비교의 초기 상태 설정은 별개다. 모델이 없으면 12주차 `examples/models/`의 저장 결과를 확인한다. 연결 실패는 시뮬레이터의 TCP `127.0.0.1:8266`과 HTTP `http://127.0.0.1:8080/state`를 확인한다. 실패 단계와 오류를 기록한다.
