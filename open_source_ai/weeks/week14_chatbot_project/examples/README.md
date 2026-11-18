# 14주차 원광대학교 소개 챗봇과 공개 시험

한 uv 프로젝트에서 원광대학교 소개 챗봇을 실행하고, 공개 20문항으로 개선 전후를 비교한다. 학생이 수정하는 파일은 [student_bot](src/student_bot/__init__.py) 하나다. 공개 질문·정답과 채점기는 그대로 두고 검색 방식이나 프롬프트를 고친다.

| 교시 | 안내 | 진입점 | 실행 |
|---|---|---|---|
| 1 | [자료 검색과 대화](period1/README.md) | [ex01_chat](src/ex01_chat/__init__.py) | `uv run ex01` |
| 2 | [공개 시험과 오답 확인](period2/README.md) | [ex02_evaluate](src/ex02_evaluate/__init__.py) | `uv run ex02` |
| 3 | [학생 함수 개선과 재평가](period3/README.md) | [ex03_improve](src/ex03_improve/__init__.py) | `uv run ex03`, `uv run evaluate` |

명령은 `pyproject.toml`이 있는 `examples/` 루트에서 실행한다. `period1`~`period3`에는 안내만 있으며, 교시마다 프로젝트나 자료를 복사하지 않는다. `ex01`과 `ex03`은 같은 공용 대화 함수와 같은 `student_bot.answer(question)`을 호출한다. `evaluate`는 `ex02`와 같은 명령이다.

## 설치와 프로젝트 구조

Python 기준 버전은 3.12다. 이 예제 폴더를 개인 실습 공간에 처음 한 번 복사하고 숨김 파일 `.python-version`도 포함한다. 이미 작성한 실습 폴더는 덮어쓰지 않는다.

```powershell
uv sync
ollama list
```

`qwen3.5:2b`가 없다면 수업 전에 `ollama pull qwen3.5:2b`로 다운로드한다. Ollama가 실행 중이어야 대화와 공개 시험이 동작한다.

프로젝트를 처음 만드는 구조 연습은 별도의 빈 위치에서 다음 명령으로 한다. 완성 예제가 있는 `examples/` 안에서 다시 초기화하지 않는다.

```powershell
uv init --package --python 3.12 --vcs none wku-bot
```

생성된 `.python-version`, `pyproject.toml`, `src/`를 이 예제와 비교한다. 각 패키지의 `main()`은 명령 시작점이다. `[project.scripts]`는 `ex01` 같은 이름을 `패키지:main`에 연결하고, `[build-system]`의 `uv_build`는 패키지를 설치한다. 공용 `shared`를 포함한 여러 패키지를 `[tool.uv.build-backend]`에 등록했다. scripts를 바꿨다면 `uv sync`를 다시 실행한다. Python 코드만 수정할 때는 같은 명령을 다시 실행하면 된다. `uv.lock`은 함께 배포한다.

## 대화와 학생 수정 파일

```powershell
uv run ex01
```

```text
나> 원광대학교를 상징하는 새는 무엇인가요?
AI> {"answers": ["봉황"], "sources": ["wku-symbols"], "abstain": false}
나> 오늘 학생식당 저녁 메뉴는 무엇인가요?
AI> {"answers": [], "sources": [], "abstain": true}
나> /bye
```

위 출력은 형식 예시이며 실행 결과를 보장하지 않는다. 빈 입력은 건너뛰고 `/bye`, Ctrl+C 또는 입력 종료로 끝낸다. 질문을 반복해서 입력하지만 이전 대화 이력은 모델에 보내지 않는다. 학생은 `answer`가 앞선 질문의 답에 의존하지 않도록 작성한다. 워커와 모델 캐시는 유지하며, 도구가 문항마다 학생 코드의 메모리를 초기화하지는 않는다.

학생 파일 위쪽의 `MODEL`, `OLLAMA_URL`, `TOP_K`와 프롬프트를 읽는다. 기본 모델은 `qwen3.5:2b`, 주소는 `http://127.0.0.1:11434/api/chat`, 검색 문서는 3개다. 한글 두 글자 조각 등을 이용한 단순 일치 검색으로 `corpus.json`의 문서를 고르고, 표준 라이브러리 `urllib`로 Ollama에 전달한다. 외부 프록시를 거치지 않는 로컬 연결을 사용한다. 명령행 옵션과 `.env`는 사용하지 않는다.

실행을 확인한 Mac 환경에서는 `format`의 JSON Schema와 `"json"` 모드가 HTTP 501과 `structured output is unavailable`을 반환했다. 이 예제는 `format`을 생략하고 시스템 프롬프트에 세 키 JSON 예시를 넣는다. 응답을 `json.loads`로 읽은 뒤 대화 화면과 부모 채점기에서 형식을 검증한다. JSON 해석에 실패하면 원문 문자열을 부모에 전달해 형식 오류와 실제 출력을 함께 보여 준다. 형식 오류를 자동으로 재시도하지 않는다.

## 자료는 한 곳에서 관리한다

| 파일 | 역할 | 각 항목의 키 |
|---|---|---|
| [corpus.json](src/shared/data/corpus.json) | 챗봇이 읽는 소개 문서 5개 | `id`, `title`, `text`, `url`, `verified_at` |
| [public_questions.json](src/shared/data/public_questions.json) | 공개 시험 20문항 | `id`, `category`, `question` |
| [public_answers.json](src/shared/data/public_answers.json) | 공개 정답과 사실별 근거 | `id`, `expected`, `fact_sources`, `sources`, `abstain` |

세 파일은 JSON 배열이다. `expected`는 사실별 별칭 그룹 배열이다. 예를 들어 `[["익산시", "익산"], ["봉황"]]`은 두 사실을 요구한다. 한 그룹 안의 문자열은 그 사실의 허용 별칭이다. `fact`는 12문항, `composite`는 4문항, `unknown`은 4문항이다. `fact`에도 교훈 두 가지처럼 답이 여러 항목인 질문이 있다. 범주를 답 개수로 판단하지 않는다.

v1.1 공식 정답에서 `fact_sources[i]`는 `expected[i]`의 근거 문서 ID다. 위 예에서는 `["wku-location", "wku-symbols"]` 순서다. 한 문서가 여러 사실을 뒷받침하면 같은 ID를 반복한다. 전체 ID 집합은 `sources`와 같아야 한다. `unknown`은 두 필드와 `expected`가 모두 빈 배열이다.

원자료의 `url`과 `verified_at`은 출처 확인용이다. 챗봇은 제공된 요약만 읽으며 실시간 조회를 하지 않는다. JSON은 공용 패키지 내부 자료로 wheel에도 포함된다. 챗봇 코드에서는 공개·비공개 정답 파일을 읽지 않는다.

## 응답 계약

정상 응답은 다음 세 키만 가진 사전이다. 추가 키와 누락 키는 모두 형식 오류로 0점이다.

```json
{"answers": ["짧은 사실"], "sources": ["문서-ID"], "abstain": false}
```

| 필드 | 제한 |
|---|---|
| `answers` | 문자열 배열, 최대 16개, 항목마다 1~256자 |
| `sources` | 문서 ID 문자열 배열, 최대 16개, 항목마다 1~128자 |
| `abstain` | 실제 bool만 허용, `"false"`나 `0`은 불가 |
| 질문 | 비어 있지 않은 문자열, 최대 4,000자 |

빈 문자열, 공백만 있는 문자열, 정규화 뒤 빈 문자열이 되는 항목은 허용하지 않는다. JSON으로 표현할 때 bool은 `true`와 `false`, Python 사전에서는 `True`와 `False`다. 근거가 부족하면 `answers=[]`, `sources=[]`, `abstain=True`로 반환한다. `answers`에는 문장 전체 대신 질문이 요구한 사실을 항목별로 적는다. 한국어 조사를 자동으로 떼지 않으므로 `익산시는`은 `익산시`와 같지 않다.

## 공개 시험과 점수

```powershell
uv run ex02
```

각 문항의 `id`, `category`, 질문, `response`, `gold`, `subscores`, 점수, `error`, `latency`가 터미널에 출력된다. JSON 형식이나 키가 틀린 응답도 가능한 경우 원문을 보존한다. 통신·실행 오류처럼 응답을 받지 못했다면 `response`는 `null`이고 오류를 표시한다. 결과 파일은 자동 저장하지 않는다.

`fact`와 `composite`는 다음 식을 적용한다.

```text
답변 F1 = 2 × 매칭된 사실 수 / (응답 사실 수 + 정답 사실 수)
출처 F1 = 2 × 인용한 문서 중 맞힌 사실의 근거인 문서 수 / (인용한 문서 수 + 문항 전체 필요 문서 수)
문항 점수 = 80 × 답변 F1 + 20 × 출처 F1
단, 답변 F1이 0이면 출처 득점도 0
```

정규화는 NFKC와 casefold를 적용하고 양끝 공백과 끝의 ASCII 마침표를 제거한다. 일반 단어 사이의 공백은 무시하며 URL과 축약 호스트 이름 내부의 공백은 보존한다. `lxp. wku.ac.kr`는 `lxp.wku.ac.kr`와 다른 값이다. 부호·조사·부정 표현과 URL 끝 `/`도 보존한다. 슬래시 유무 등 여러 표기를 허용하려면 정답 별칭에 등록한다. 답과 출처의 정규화 중복은 한 번만 센다.

정답은 별칭과 정확히 일치할 때 인정한다. 최대 이분 매칭으로 응답 하나를 사실 하나에만 배정한다. 한 사실의 여러 별칭을 나열해도 그 사실은 한 번만 맞힌 것으로 세며, 서로 다른 응답 항목은 정밀도의 분모에 남는다. 후보 답이나 무관한 출처를 나열하면 F1이 낮아진다.

공개 13번에서 도시만 맞히면 위치 문서만 인용했을 때 66.67점, 교조 문서만 인용했을 때 53.33점, 두 문서를 모두 인용했을 때 63.33점이다. `subscores.source_f1`의 분자에는 맞힌 사실의 근거만 들어가고 분모에는 인용한 문서가 모두 들어간다. [v1.1 규격의 계산 예](../evaluation_spec.md#사실과-출처-점수)

`fact_sources`가 없는 v1 정답을 읽으면 문항 전체의 필요 문서와 인용 문서를 비교한다. 이 경우 답변 F1이 0이어도 원래 출처 일치율을 표시하고 실제 부여하는 `source_points`는 0이다. 답변을 보류한 known 문항은 0점이다. `unknown`은 `abstain=true`, `answers=[]`, `sources=[]`를 모두 만족할 때만 100점이며 나머지는 0점이다.

마지막에 범주별 문항 수와 평균, 전체 문항 평균을 표시한다. 전체 평균은 문항별 점수 합을 전체 문항 수로 나눈 값이다. 세 범주의 평균을 다시 평균 내지 않는다. 시간 초과·실행 오류·형식 오류 문항도 0점으로 전체 수와 해당 범주에 포함한다. 소요 시간은 보고만 하고 점수에 더하거나 빼지 않는다.

## 워커와 비공개 평가 재사용

부모 평가 프로세스가 질문과 정답을 읽고 ID의 중복·누락·추가 및 범주를 검증한다. 자식 워커에는 JSON Lines로 질문 문자열만 보낸다. 정답, 문항 ID, 범주는 보내지 않는다. 워커는 여러 질문 동안 유지하며 Python의 일반 출력은 stderr로, 평가 응답은 stdout으로 분리한다. 파일과 프로세스 통신은 UTF-8을 명시한다.

처음과 워커 재시작 때마다 별도 준비 질문 한 개에 최대 120초를 허용한다. 모든 준비 응답·오류·시간을 `warmups`에 기록하고 점수와 문항별 소요 시간에서 제외한다. 이는 모델 로딩 준비이며 모델 가중치를 학습하는 과정이 아니다. 준비 응답의 형식만 틀렸다면 원문과 오류를 보고하고 같은 워커로 본 문항을 진행한다. 본 문항의 형식 오류도 그 문항만 0점이며 워커를 유지한다.

본 문항은 각각 최대 30초이며 시간 초과·통신·실행 오류 시 워커를 종료한다. 다음 문항에서는 새 워커의 준비 요청부터 다시 수행한다. 준비 요청 자체가 시간 초과나 실행 오류로 끝나면 아직 준비되지 않은 워커에 본 문항을 보내지 않는다. 해당 문항은 실행하지 못한 이유와 함께 오류 0점으로 남기고, 다음 문항에서 새 준비를 시도한다. 준비 질문 자체를 평가 문항 수에 추가하지 않는다.

평가 종료나 Ctrl+C 때 이 도구가 시작한 워커와 자식 프로세스, 파이프, 통신 스레드를 정리한다. POSIX는 전용 세션의 프로세스 그룹, Windows는 전용 [Job Object](https://learn.microsoft.com/en-us/windows/win32/procthread/job-objects)를 사용한다. 자식이 stdout 파이프를 물려받아도 워커 종료가 지연되지 않게 함께 종료한다. 외부 Ollama 서버 자체를 종료하지는 않는다.

[shared.evaluation](src/shared/evaluation.py)의 `evaluate(questions, answers)`는 파일 경로를 고정하지 않고 같은 스키마의 질문·정답 배열을 받는다. 교수용 비공개 runner에서도 이 API와 순수 함수 `score_response(response, gold)`를 재사용할 수 있다. `worker_command`는 관리자가 마련한 워커 명령을 지정할 때 사용하며, 그 워커도 질문 문자열만 받는 동일한 통신 계약을 따라야 한다.

이 공개 runner의 프로세스 분리는 보안 샌드박스가 아니다. 같은 계정과 파일 시스템의 공개 정답에 학생 코드가 접근하는 것을 차단하지 않는다. 교수용 비공개 평가는 정답 파일에 접근할 수 없는 별도 실행 환경과 권한으로 워커를 운영해야 한다. 부모가 정답을 읽는다는 사실이나 프로세스를 나눴다는 사실만으로 이 접근 제한이 성립하지 않는다.

## 개선과 검증

```powershell
uv run ex03
uv run evaluate
uv run python -m unittest discover -s tests -v
```

`student_bot`의 검색이나 프롬프트 한 부분을 바꿔 대화로 확인한 뒤 같은 공개 시험을 다시 실행한다. 질문을 보고 정답을 직접 분기하거나 정답 파일을 읽는 방식 대신 자료 검색과 응답 생성을 개선한다. 원래와 바뀐 답, 변경 이유, 남은 실패 문항을 비교한다.

테스트는 Ollama를 호출하지 않는다. 정답·0점·부분점수·답 나열·별칭 매칭·중복·부정 표현·형식 오류·20문항 집계와 실제 자식 프로세스의 시간 초과·재시작·종료를 확인한다. 테스트 대역은 `tests/` 안에만 있다. 실제 모델의 답변 품질은 공개 시험을 따로 실행해서 확인한다.

### 공개 평가 실행 기록

같은 로컬 모델 `qwen3.5:2b`로 공개 20문항을 실행한 기록이다. 점수는 100점 만점이며 시간은 준비 요청을 포함한다.

| 규격 | 측정일 | 전체 평균 | fact | composite | unknown | 시간 |
|---|---|---:|---:|---:|---:|---:|
| v1.1 | 2026-11-19 | **69.43** | 75.00 | 72.17 | 50.00 | 7.224초 |
| v1 | 2026-11-13 | 83.27 | 81.11 | 73.00 | 100.00 | 약 12.1초 |

v1.1은 `uv run evaluate`로 측정했다. 두 측정은 공개 문항과 채점 규격이 다르므로 챗봇 개선 전후의 비교에는 같은 버전으로 실행한 결과를 사용한다. 11월 13일의 기록 환경은 macOS arm64, Ollama 0.40.14, 모델 ID `dfaf2605162e`, `TOP_K=3`, temperature 0이었다. Windows의 프로세스 정리 동작은 실제 Windows 환경에서 추가 확인이 필요하다.

실습 순서와 과제 제출 안내는 [주차 실습지](../lab.md)를 따른다. [Ollama 채팅 API](https://docs.ollama.com/api/chat)와 [uv 빌드 백엔드](https://docs.astral.sh/uv/concepts/build-backend/)는 사용한 API와 패키징 방식의 공식 문서다.
