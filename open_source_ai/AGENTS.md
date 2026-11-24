# 오픈소스 AI 교재·실습 작성 지침

`open_source_ai/`를 맡은 에이전트가 처음 읽는 문서다. 같은 폴더의 `CLAUDE.md`는 이 파일을 불러오는 한 줄만 둔다. 저장소 전체의 구조·결정·작업 이력은 [`_forAI/`](../_forAI/README.md)에 있다.

## 과목과 먼저 읽을 문서

오픈소스 생태계·Git·uv에서 시작해 Ollama, LangChain, RAG, LoRA, Streamlit, 초소형 모델의 시뮬레이터 제어, 챗봇 성능 평가까지 이어지는 15주 공용 교재다. 한 주는 60분 블록 3개(1·2·3교시)이고 블록마다 설명·시연 20분, 실습 30분, 휴식 10분이다. 자료는 일차가 아니라 교시 단위로 쓴다. 저장소는 GitHub 공개 저장소이며 슬라이드는 GitHub Pages 도서관으로 배포된다.

1. [과목 README](README.md): 범위와 진입점
2. [주차 색인](weeks/README.md): 운영 기준, 주차 목록, 검증용 기본값
3. [제작 계획 10절](materials_plan.md#10-1015주차-개편안-2026-11-12): 10~15주차 개편 결정과 실측 범위. 1~9절은 초판 이력이다.
4. [`_forAI/`](../_forAI/README.md): README, inventory, memo, dev_log, plan 순서. 이 과목의 대기 작업은 plan의 '기존 과목의 대기 작업'과 '오픈소스 AI 후속 작업'에 있다. `_forAI`와 이 파일·`weeks/README.md`가 다르면 이 파일을 따르고 다른 점을 보고에 적는다.
5. 10~13주차를 고칠 때: [WlEno 시뮬레이터](../tools/wleno/README.md), [공용 제어 도구](../tools/bleuno-control/README.md)
6. 14·15주차를 고칠 때: [평가 명세](weeks/week14_chatbot_project/evaluation_spec.md)

## 폴더와 파일

```text
open_source_ai/
├─ README.md, AGENTS.md, CLAUDE.md
├─ materials_plan.md       제작 계획. 10절이 10~15주차 개편 결정
├─ ta_setup_guide.md       조교 설치 목록과 10~13주차 준비 표
├─ uv_guide.md             uv 설치, 수업용 Python, uv run
├─ github_distribution.md  커밋할 파일과 제외할 파일
├─ weeks/README.md         운영 기준, 주차 목록, 검증용 기본값
├─ weeks/weekNN_<주제>/     정규 15주
└─ specials/
   ├─ huggingface_hub/, pytorch_basics/    사이트에 올린 선택 특강
   ├─ chatbot_rag_finetune/               사이트에 올린 기말 챗봇 개선 특강(평가·RAG·파인튜닝·추론 버그 잡기, 4교시)
   ├─ reasoning_tips/                     팁엔트릭엔 추론, 독립 복습 자료
   └─ project_delivery/                    이전 10~13주차 원고 보존(사이트 미등록)
```

| 주차 폴더의 파일 | 역할 |
|---|---|
| `README.md` | 학습 질문, 목표, 3교시 흐름, 완료 기준, 제출 증거 |
| `slides.md`, `slides_en.md` | Marp 원고 한국어판과 영문판. 사이트가 둘 다 렌더한다 |
| `lab.md` | 교시별 30분 실습. 예상·관찰 표와 단계별 힌트만 둔다 |
| `walkthrough.md` | 시연·실습 재현 절차. 1·3·4·5·6·7·9·10·11·12·13주차에 있다 |
| `examples/` | 실행 예제. 규격은 아래 목록 |
| 평가 문서 | 4·8·12·15주차 `assignment_brief.md`·`assignment_rubric.md`, 8주차 `exam_structure.md`·`exam_rubric.md`, 14주차 `evaluation_spec.md`·`report_template.md`·`assignment_brief.md`, 15주차 `final_review_rubric.md`·`presentation_rubric.md` |

15주차 `presentation_rubric.md`는 파일 이름만 남았고 내용은 기존 발표 항목을 대신하는 AI 성능 루브릭이다.

- 5·6·7·9~14주차 `examples/`는 아래 '예제 코드'의 5주차 규격을 따르는 uv 프로젝트 하나다(`.python-version` 3.12, `uv.lock` 포함). `examples/`에서 `uv sync` 후 `uv run exNN`으로 실행한다. 9주차 Streamlit 앱은 예외로 `uv run streamlit run src/<예제>/app.py`를 쓴다(아래 '예제 코드').
- 1~4·8주차는 교시 폴더별 파일·템플릿 구조이고, 15주차 `examples/`에는 안내 README만 있다. 이 주차들을 크게 고칠 때는 5주차 규격으로 옮긴다.
- 10~13주차는 `[tool.uv.sources]`의 상대 경로로 저장소의 `tools/bleuno-control`을 쓴다. 저장소 전체를 복제해야 실행되며 주차 폴더만 떼어 내면 경로가 끊긴다. 13주차는 12주차 `examples/models/`의 학습 결과를 그대로 읽는다(`src/shared`의 `MODELS_DIR`).
- 특강 `chatbot_rag_finetune`은 uv 프로젝트가 둘이다. `examples/`(명령 `ex04`~`ex07`)는 14주차 예제 프로젝트를 `[tool.uv.sources]`의 상대 경로로 설치하고, `finetune/`(명령 `prepare`·`ft01`·`ft02`)은 7주차와 같은 torch·transformers·peft 버전을 쓴다. `ex06`의 학습 예시는 특강 루트의 `outputs/sft/`에 생기고, 학습·변환 산출물과 `finetune/tools/llama.cpp/`는 특강 루트의 `.gitignore`로 막는다.
- 시뮬레이터 `tools/wleno`는 uv 프로젝트가 아니다. Python 3.10 이상의 표준 라이브러리로 실행되고 창은 Tkinter를 쓴다. 수업 문서는 저장소 루트에서 `python tools/wleno/main.py --bind 127.0.0.1`로 켜게 한다(TCP 8266, HTTP 8080).

주차 폴더 이름 `weekNN_<영문 주제>`가 콘텐츠 ID다. `site/catalog.json`의 chapter `id`와 비공개 대본·해답 폴더도 같은 이름을 쓴다. 이름을 바꾸면 catalog의 `formerIds`에 옛 이름을 넣어 옛 슬라이드 주소를 살린다(2026-11-13 10~15주차 폴더 이름 변경 사례).

## 수업과 예제 작성 규칙

수업 설계

- 예제는 수업 시간 안에 학생이 실행하고, 직접 바꾸고, 결과까지 확인할 수 있어야 한다. 교시당 설명·시연 20분, 실습 30분, 휴식 10분을 기준으로 필수 활동을 구성한다.
- 단순하게 만들되 학습에 필요한 기능을 생략한 일회성 시연으로 끝내지 않는다. 첫 호출을 배우는 Hello 예제 이후에는 터미널에서 직접 질문을 입력하고 답을 받은 뒤 다음 질문을 할 수 있게 한다.
- 대화형 예제는 입력 안내, 빈 입력 처리, 명확한 종료 방법을 갖춘다. 입력을 반복하는 것과 대화 이력을 보내 문맥을 유지하는 것을 구분해 설명한다.
- 예제 하나에 새 개념 하나를 중심으로 가르친다. 짧고 읽기 쉬운 반복문과 공식 라이브러리를 우선하고, 실습에 불필요한 클래스·공통 프레임워크·복잡한 설정 계층을 추가하지 않는다.
- 비교 실습은 같은 질문과 필요한 조건만 바꿔 관찰할 수 있게 한다. 필수 실습과 선택 확장을 구분하고 모델·의존성 다운로드는 수업 전에 준비한다.
- 정규 흐름은 4주차 Ollama, 5주차 LangChain, 6주차 임베딩·RAG, 7주차 LoRA, 8주차 평가, 9주차 Streamlit 앱 순서다. Hugging Face 상세 분석과 PyTorch는 선택 특강으로 둔다. PyTorch 특강은 텐서 연산·저장·불러오기부터 작은 가상 데이터의 회귀 모델로 마무리하며 정규 수업의 선행 조건으로 두지 않는다. 특강 보고서를 정규 과제의 필수 조건으로 다시 넣지 않는다.
- `specials/reasoning_tips`의 「팁엔트릭엔 추론」은 터미널 예제를 쓰는 독립 복습 자료다. 주차·교시·수업 시간을 배정하거나 정규 주차의 후속 실습으로 연결하지 않는다. 사이트에서는 `special` 유형을 재사용하되 한국어 표시는 `복습`, 영어 표시는 `Review`로 구분한다.
- Ollama 다음에 학습 도구를 도입할 때는 기존 대화, 실행과 학습의 차이, 짧은 Transformers 대화, 데이터 수정·LoRA 학습·저장·복원 순서로 연결한다(2026-11-11 사용자 승인). 도구 전환 이유를 설명하기 전에 rank·VRAM 계산·Trainer 내부·마스킹 구현을 필수 과제로 요구하지 않는다. 학습 전후는 같은 기본 모델과 입력·생성 조건에서 비교하고, Ollama 재사용은 사전에 검증한 가져오기 경로로 시연한다.
- 2026-11-13 승인에 따라 10~13주차는 시뮬레이터 제어, 초소형 툴 호출 모델, 로컬 LoRA 학습·저장·복원, 제어 평가와 Streamlit 앱으로 연결한다. 공용 TCP 연결·검증·평가는 `tools/bleuno-control`을 재사용한다. 모델의 호출 제안과 실제 실행을 분리하고, 명령의 응답과 함께 시뮬레이터 상태로 성공을 확인한다. 학습 전후에는 같은 모델·깊이·양자화·입력 조건을 적용한다.
- WlEno(프로토콜 2.0.0)는 TCP 연결·해제 때 LED·센서 상태를 초기화하지 않고, 범위 밖 번호·밝기를 오류로 거부한다. 비교할 초기 상태(문항마다 LED `[0, 64, 128, 255]`)는 명령으로 맞추고 `GET /state`로 확인한다. 모델 도구는 `turn_on`·`turn_off`·`set_brightness`·`read_environment` 네 개이며 센서 값을 바꾸는 `POST /set`은 모델에 주지 않는다.
- 정규 앱이 동작한 뒤 남는 시간에 얼굴·이미지 임베딩 유사도, 음성 인식·출력, 약 1B급 소형 모델, 다른 생성 방식 중 하나를 선택해 소개한다. 실제 입출력을 확인하는 시연으로 구성하고 모든 선택 주제를 필수 실습에 덧붙이지 않는다.
- 기말과제는 기존 발표 점수를 챗봇의 AI 성능 평가 점수로 대체하고, 레포트 점수는 개발 내용을 정리한 보고서로 별도 평가한다(2026-11-12 사용자 지시). 기존 성적 반영 비율을 유지하며 임의의 통합 비율을 만들지 않는다. 14주차에 과제 규칙·공개 평가세트·평가 도구를 제공하고, 제출 버전은 같은 규격의 비공개 문항으로 평가한다. 이번 공개 적용 과제의 대상은 원광대학교 소개 챗봇이며 실제 강좌 배점·마감·학생 자료와 비공개 정답은 학교 저장소에 둔다.

예제 코드

- 실행 가능한 Python 예제는 배포 표준 구조로 둔다(2026-10-16). 예제 하나가 `src/<모듈>/__init__.py` 패키지 하나이고 진입점은 `def main()`이다. `pyproject.toml`에 `[project.scripts]`(`<명령> = "<모듈>:main"`), `[build-system]`(`uv_build`), 패키지 이름이 프로젝트 이름과 다르면 `[tool.uv.build-backend] module-name`을 둔다. 실행 안내는 `uv run <명령>`이며 `uv run python 파일.py`로 단순화하지 않는다. `main`·`[build-system]`이 왜 필요한지와 scripts를 고치면 `uv sync`를 다시 해야 한다는 점을 문서에 설명한다.
- 매 주차(챕터)에 uv로 **특정 Python 버전을 지정해 프로젝트를 만드는 단계**를 넣는다(2026-10-16). 과목 기준 버전(현재 3.12)으로 `uv init --package --python 3.12 --vcs none <이름>`을 실행해 `.python-version`·`pyproject.toml`·`src/` 구조를 직접 확인하게 하고, 교재 예제 폴더에도 같은 버전의 `.python-version`을 둔다.
- 여러 예제가 함께 쓰는 코드(설정값·모델 ID·도우미 함수)는 `src/` 안의 공용 패키지로 두고 라이브러리처럼 `from <패키지> import ...`로 쓴다(2026-10-16). 형제 `.py` 파일을 직접 import하거나 같은 코드를 예제마다 복사하지 않는다. 공용 패키지는 `[tool.uv.build-backend] module-name`에 넣고, 명령이 필요 없으면 `[project.scripts]`에는 올리지 않는다. 여러 주차가 함께 쓰는 10~13주차 제어 코드만 저장소의 `tools/bleuno-control`에 둔다.
- 5주차 `week05_langchain_basics/examples`를 예제 구조의 기준으로 삼는다(2026-10-29 사용자 지시). 주차의 `examples/`에 uv 프로젝트 하나와 `pyproject.toml`·`.python-version`·`uv.lock`을 두고, 예제별 `src/exNN_<주제>/__init__.py`의 `main()`을 `uv run exNN`으로 실행한다. 공용 코드는 `src/shared/`에 한 번만 두며 예제끼리 직접 import하지 않는다. `period1`~`period3`에는 해당 교시의 소스와 실행 순서를 안내하는 README만 둔다. 문서·평가셋·환경 설정·산출물은 한 프로젝트에서 이어 쓰며 교시마다 복사하거나 다시 생성하게 하지 않는다. 새 예제와 구조 개편에 이 기준을 적용한다.
- 9주차 Streamlit 화면 예제는 `examples/`에서 `uv run streamlit run src/<예제>/app.py`로 직접 실행한다. 슬라이드와 실습지에도 학생이 수정할 `app.py` 경로를 명령에 표시한다.
- 예제에 명령행 옵션(argparse)·`.env` 설정 계층·결과 JSON 저장·직접 만든 예외 클래스 같은 실무 앱 구조를 넣지 않는다(2026-11-05 사용자 지시, "커맨드라인 파라미터 남발 금지"). 바꿔 볼 값은 파일 맨 위의 대문자 상수(`TOP_K`, `CHUNK_SIZE` 등)로 두고 학생이 값을 고쳐 같은 명령을 다시 실행해 비교한다. 자료는 작위적인 수업 규칙 문서 대신 학생이 흥미를 느끼는 공유 저작물(예: 6주차 그리스·로마 신화 요약)을 교재용으로 새로 써서 `src/shared/data/`에 둔다. 저작권이 있는 소설 원문은 공개 교재에 넣지 않는다.
- `uv.lock`은 3·4주차 일부 교시와 5·6·7·9~14주차, 특강 `chatbot_rag_finetune`의 `examples/`·`finetune/`에 커밋되어 있다. 의존성을 바꿀 때만 `uv lock`으로 갱신하고, 검증할 때는 `--frozen`이나 `--locked`로 lock을 바꾸지 않는다.
- 코드 변경 시 README·실습지·따라하기·슬라이드의 실행 및 입력 안내도 맞춘다. 실제 입력, 응답, 다음 입력, 종료 흐름을 검증하고 확인하지 못한 실행 결과는 단정하지 않는다.

### LangChain 터미널 예제와 추론 복습

5주차처럼 각 예제의 `main()`에서 `input()`으로 질문을 받고 모델을 호출한 뒤 결과를 출력하는 흐름이 보이게 쓴다. 모델 설정과 출력·복구 도우미는 `src/shared/`에 두고 입력 반복문은 예제에 둔다. 완성된 답과 종료 사유는 `invoke()`로 읽는다. 답을 도착하는 대로 보여 주거나 생성 도중 추론 반복을 멈추는 예제에서 `stream()`을 쓴다.

[추론 복습 예제](specials/reasoning_tips/README.md)는 같은 질문을 세 프로그램에 각각 입력해 비교한다.

| 예제 | 학생이 터미널에서 확인할 내용 |
|---|---|
| ex01 · 기본 호출 | 모델의 추론을 켜 둔 채 `AI>`에 본문을 출력한다. 본문이 비면 안내를 표시한다. |
| ex02 · 완성 응답 관찰 | 한 번의 `invoke()`가 끝나면 모델이 보낸 `reasoning_content` 원문을 `추론>`에 표시하고 글자 수·종료 사유와 `AI>` 본문을 차례로 출력한다. |
| ex03 · 생성 중 복구 | `추론>`에는 받은 원문을 조각마다 즉시 출력한다. `AI>` 본문은 터미널에서 한 글자씩 표시한다. 이어쓰기용 추론은 해당 요청에만 쓰고 대화 이력에는 사용자 질문과 최종 답을 남긴다. |

이 복습 자료를 고치면 세 예제에 같은 질문을 입력해 출력 순서를 확인한다. 교육 흐름, 실행 동작, 설치·실행 재현성은 독립 검토자 세 명이 각각 10점 만점으로 평가한다. 세 점수가 모두 9점을 넘을 때까지 지적 사항을 수정하고 다시 검증한다.

## 고친 뒤 같이 맞출 곳

| 바꾼 것 | 같이 고칠 곳 |
|---|---|
| 예제 코드, 실행 명령, 입력 방식 | 주차 `README.md`, `examples/README.md`, `examples/periodN/README.md`, `lab.md`, `walkthrough.md`의 코드·명령 인용, `slides.md`·`slides_en.md` |
| `slides.md` 내용 | `slides_en.md`를 같은 장 수로 맞춘다. 비공개 대본의 구간 제목·분 범위도 바뀐다 |
| 슬라이드 장 수 | `scripts/render-site.mjs`의 `EXPECTED_SLIDES`, `scripts/check-site.mjs`의 `EXPECTED_SLIDES`와 `EXPECTED["open-source-ai"].slides`, `site/catalog.json` 과목 `summary` |
| 덱 추가·삭제·이름 변경 | `site/catalog.json`의 chapters와 `formerIds`, 두 스크립트의 `EXPECTED_DECKS`와 과목 `decks` |
| 시뮬레이터 실행 명령 | 10주차 6개 파일(README, `examples/README.md`, lab, walkthrough, slides 한영), 11주차 4개 파일(README, `examples/README.md`, lab, walkthrough), 12주차 `examples/period1/README.md`. `git grep -n "wleno/main.py" -- open_source_ai`로 찾는다 |
| `tools/bleuno-control`의 함수·검증·평가·학습, `tools.json`, `control_cases.json` | 10~13주차 문서와 `src/shared`, `materials_plan.md` 10절, `weeks/README.md` 기본값 표, `ta_setup_guide.md` 10~13주차 표 |
| `tools/wleno`의 명령·응답·포트 | Android 11~15주차(`android_programming/iot_sim/lab.md`, `tools/wleno/android/`)도 같은 시뮬레이터를 쓴다. 혼자 바꾸지 않고 Android 담당 작업과 맞춘다 |
| 생성 모델 기본값 | 기본값이 둘로 갈려 있다. 4~7·9~11·14주차와 특강 `chatbot_rag_finetune`의 `rag_bot`은 `qwen3.5:2b`, 1~3주차와 8주차 `period3/config.py`·두 `broken_project/report.py`·두 `make_broken_repo.ps1`은 초판 흐름의 `qwen3:8b`다(8주차 README·lab·slides는 `qwen3.5:2b`). 바꿀 때 같이 볼 곳: 각 주차 예제 상수, 5·6·9주차 `src/shared`와 8주차의 `OLLAMA_MODEL` 기본값, 4주차 `examples/period3/Modelfile`, 14주차 `examples/tests/test_evaluation.py`의 모델 이름 단언, `tools/bleuno-control/src/bleuno_control/models.py` 기본 인수, `weeks/README.md` 기본값 표, `ta_setup_guide.md`. 찾기: `git grep -n --untracked -e "qwen3.5:2b" -e "qwen3:8b" -- open_source_ai ':!open_source_ai/specials/project_delivery'` |
| 12주차 학습 데이터·저장 이름 | 13주차 `src/shared`의 `MODELS_DIR`와 모델 파일 이름, `ta_setup_guide.md` 10~13주차 표 |
| 14·15주차 평가 규칙 | 정본은 `evaluation_spec.md`다. `examples/src/shared/evaluation.py`, `examples/tests/test_evaluation.py`, `report_template.md`, 15주차 `assignment_rubric.md`·`final_review_rubric.md`·`presentation_rubric.md` |
| 14주차 `student_bot`의 응답 계약·시스템 지시·요청 방식 | 특강 `chatbot_rag_finetune/examples/src/rag_bot`(같은 계약과 시스템 지시의 사본, 검색만 다르다), 특강 `examples/tests/test_rag_examples.py` |
| 14주차 `shared/worker.py`의 워커 통신 규칙 | 특강 `examples/src/lab_shared/worker.py`(같은 규칙을 따르고 실행할 봇 이름을 받는다), 특강 `examples/tests/test_lab_shared.py` |
| 14주차 `shared/evaluation.py`의 시간 제한·함수, `shared/data`(참고 자료 `corpus.json`, 공개 20문항) | 특강 `ex04`~`ex07`과 `examples/tests/`, `lab_shared/data/README.md`, 특강 `walkthrough.md`·`lab.md`·`slides.md`·`slides_en.md`·`period2` 안내의 문서 수(5개)·`n/16`·준비 질문 120초·3–6분 예시 |
| 특강 `rag_bot`의 상수 이름(`MODEL`·`TOP_K`·`MIN_SCORE` 등)과 요청 값(`"think": False`, `"num_predict": 512`), `answer()`·`rank()`·`retrieve()`·`messages()`, `SYSTEM_PROMPT` | 특강 `examples/debugging.md`의 버그 심기 표, `ex05_search`·`ex06_make_sft`, 특강 `walkthrough.md`·`lab.md`·`slides.md`·`slides_en.md`, `period2`~`period4` 안내 |
| 특강 `ex04`·`ex07`의 상수(`BOT`, `QUESTION_SET`, `RESPONSE_WIDTH`, `SHOW_PROMPT` 등)와 출력 형식(실패 종류 표, [1]~[6] 구역) | 특강 `period1`·`period4` 안내, `examples/debugging.md`, `lab.md`·`slides.md`·`slides_en.md`의 1·4교시, `tests/test_ex04_my_eval.py`·`test_ex07_inspect.py` |
| 특강 `finetune/src`의 상수(`STEPS`, `MAX_LENGTH`, `DTYPE` 등)와 명령 | 특강 `walkthrough.md`의 '7주차와 다른 값' 표, `period3` 안내, `slides.md`·`slides_en.md` |

사이트 빌드는 슬라이드의 상대 `.md` 링크를 GitHub 주소로 바꾸기만 하고 대상이 있는지 보지 않는다. README·lab·walkthrough의 링크는 자동 검사가 없다. 바꾼 링크는 대상 파일과 앵커를 직접 확인한다.

## 검증 명령

모두 저장소 루트에서 실행한다. 2026-11-18 작업 상태에서 아래 명령은 모두 통과했다.

```powershell
# 1. Python 문법(모델·네트워크 불필요). 캐시를 저장소 밖에 써서 __pycache__/를 남기지 않는다
$env:PYTHONPYCACHEPREFIX = "$env:TEMP\pycache-check"
python -m compileall -q open_source_ai tools/bleuno-control tools/wleno

# 2. 단위 시험(Ollama·Needle·시뮬레이터 불필요)
python -B -m unittest discover -s tools/wleno/tests
uv run --frozen --directory tools/bleuno-control python -B -m unittest discover -s tests
uv run --frozen --directory open_source_ai/weeks/week14_chatbot_project/examples python -B -m unittest discover -s tests
uv run --frozen --directory open_source_ai/specials/chatbot_rag_finetune/examples python -B -m unittest discover -s tests

# 3. 사이트(Node.js 24 이상). 슬라이드·catalog를 바꿨을 때
npm run build
npm test
```

| 명령 | 통과 기준(2026-11-18 값) |
|---|---|
| `compileall` | 종료 코드 0 |
| WlEno 시험 | 35개 OK |
| `bleuno-control` 시험 | 15개 OK |
| 14주차 채점 도구 시험 | 28개 OK(2026-11-19 평가셋 v1.1 뒤) |
| 특강 `chatbot_rag_finetune` 시험 | 89개 OK(2026-11-24) |
| `npm run build` | 이 과목의 덱·장 수가 `scripts/check-site.mjs`의 `EXPECTED["open-source-ai"]`와 맞고 영문판도 같은 수여야 한다. `영문판 장수가 한국어판과 다릅니다` 경고가 이 과목에 없어야 한다(경고만 내고 빌드는 계속된다) |
| `npm test` | 사이트 검사, 슬라이드 맞춤 시험, 실습 시험 모두 통과 |

`uv run`은 해당 폴더에 `.venv/`를 만들며 이 폴더는 Git에서 제외된다. 여러 작업이 동시에 `npm run build`를 돌리면 `dist/`가 충돌하므로 한 번에 하나만 실행한다.

시뮬레이터 연동은 손으로 확인한다. 터미널 A에서 `python tools/wleno/main.py --bind 127.0.0.1 --no-window`를 켜고, 터미널 B의 10주차 `examples/`에서 `uv sync` 뒤 `uv run ex01`에 `on 0`, `pwm 1 128`, `sensor`, `/bye`를 입력한 다음 HTTP 8080의 `GET /state`와 대조한다. Ollama는 필요 없다. 2026-11-18에는 이 절차 대신 `bleuno_control.Board`를 직접 연결해 재연결 뒤 LED 유지와 번호 4 거부만 확인했다.

다음 확인은 무거워서 2026-11-18에 실행하지 않았다. 바꾼 범위에 해당하면 실행하고, 못 하면 보고에 미검증으로 적는다.

- 10주차 Ollama `qwen3.5:2b` 툴 호출(`uv run ex02`, `ex03`)
- 11~13주차 `cactus-compute==4.2.0`·Needle 가중치 설치와 추론, 12주차 `uv run ex02` 학습(Mac M1 Max CPU에서 약 339.4초 기록), 13주차 Streamlit 앱(8501)
- 7주차 PyTorch 학습·병합과 GGUF 변환
- `ruff check --select E9,F63,F7,F82`(8주차 `broken_project` 두 폴더 제외)

## 하지 말 것

- 강의 대본, 실습 해답, 비공개 평가 문항과 정답을 공개 저장소에 넣지 않는다.
- `lab.md`에 실측 결과를 정답처럼 적지 않는다. 측정하지 않은 실행 시간·VRAM·tokens/s를 사실로 쓰지 않는다. 확인한 수치는 장비·버전·설정과 함께 쓰고 다른 환경의 결과로 넓히지 않는다(12주차 339.4초는 실습실 Windows·GPU 검증을 대신하지 않는다).
- 다른 과목 표현("1일차", "90분", "30분 설명")을 옮겨 오지 않는다. 이 과목은 "교시"와 20·30·10분이다.
- 초안의 `materials/` 챕터 구조를 되살리지 않는다.
- 모델 태그가 같은 빌드를 계속 가리킨다고 가정하지 않는다. 2026-09-03에 `qwen3:4b`가 생각 전용 빌드를 가리켜 `"think": false`가 무시된 일이 있었다. 생각 모드, 도구 호출, 컨텍스트 길이 같은 태그 의존 동작은 `ollama show`나 레지스트리 digest로 확인한다.
- 버전에 따라 바뀌는 CLI 명령 이름을 본문에 고정하지 않는다. Python API로 쓰거나 `--help`로 확인하게 한다.
- 10~13주차 문서에 연결·해제가 LED를 초기화한다는 옛 시뮬레이터 동작을 다시 쓰지 않는다. 시뮬레이터의 `ok` 응답만으로 제어 성공을 판정하지 않는다.
- 이전 10~13주차 원고(`specials/project_delivery/`)의 설정 방식과 제출 조건을 새 정규 과제에 적용하지 않는다.
- 기말 성적을 성능 80%·보고서 20% 같은 통합 비율로 바꾸지 않는다.
- 공용 교재에 학교명·분반·학수번호·실제 날짜·성적 비율·LMS 이름을 넣지 않는다. 루브릭은 100점 상대 배점만 둔다. 14·15주차의 원광대학교 소개 챗봇과 이 챗봇을 다루는 특강 `chatbot_rag_finetune`은 사용자 지시에 따른 예외다.
- 전역 `pip install`과 수업 시간 중 모델 다운로드를 안내하지 않는다.
- `.env`, 토큰, 학습 산출물(`models/`, `adapters/`, `outputs/`), 7주차 GGUF 변환 때 주차 폴더 아래에 clone하는 `tools/llama.cpp/`를 커밋하지 않는다.
- 8주차 `examples/mock_exam/broken_project`와 `examples/period1/broken_project`의 `pyproject.toml`은 모의 실기용으로 일부러 깨뜨린 파일이다. 고치지 않는다.
- 슬라이드 장 수를 바꾼 뒤 사이트 상수를 그대로 두지 않는다. 빌드가 실패한다.
- 사용자 동의 없이 커밋하거나 `_forAI/` 문서를 고치지 않는다.

## 완료 기준과 보고

다음을 모두 만족하면 완료다.

- 위 표에서 같이 고칠 곳을 모두 맞췄다.
- 바꾼 범위에 해당하는 검증 명령이 통과했다. 실행하지 못한 확인은 이유와 함께 미검증으로 남겼다.
- `slides.md`와 `slides_en.md`의 장 수가 같고 사이트 상수가 빌드 결과와 맞는다.
- 비밀정보, 실측 정답, 학교 운영 정보, 이 PC의 절대 경로가 공개 문서에 없다.
- `git status`에 의도한 파일만 바뀌어 있다.

보고는 한국어로 다음 순서로 쓴다.

1. 바꾼 수업 단위: 주차·교시별로 무엇을 왜 바꿨는지
2. 실행한 검증 명령과 결과(통과 개수, 빌드 출력의 덱·장 수)
3. 실행하지 않은 확인과 그 이유
4. 비공개 짝 저장소에 반영할 것(대본 구간, 해답, 실측값)
5. 발견했지만 고치지 않은 문제
6. 커밋 여부

## 비공개 짝 저장소와의 경계

`univ_scoring_works/teaching_materials_private/`에는 같은 주차 폴더 이름으로 강의 대본(`lecture_script.md`)과 실습 해답(`lab_solution.md`)이 있다. 8주차 실기평가 패킷, 15주차 기말 평가 자료, 챕터 퀴즈 은행도 그쪽에 둔다. 14·15주차의 비공개 최종 문항·정답과 실제 배점·마감·분반·학생 자료는 학교 비공개 자료에 있다.

- 공개 문서는 이 자료를 "강의자 별도 관리(비공개)"로만 가리키고 내용을 옮겨 오지 않는다.
- 대본의 구간 제목과 분 범위는 공개 `slides.md`와 같아야 한다. 슬라이드 구간을 바꾸면 보고의 4번에 적는다.
- 공개 `lab.md`의 정답과 실측 기록은 비공개 해답에 둔다.
- 비공개 저장소는 사용자가 요청할 때만 고친다.
