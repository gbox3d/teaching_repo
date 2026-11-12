# 주차별 강의 자료

## 공통 실습 가이드

- [uv 사용 가이드](../uv_guide.md): 최신 설치·갱신, 수업용 Python 선택, `uv run`, 의존성·lock 관리. 1주차 첫 실행과 3주차 프로젝트 실습에서 함께 읽는다.
- [GitHub 소스 배포 가이드](../github_distribution.md): 커밋할 파일과 제외할 파일, 이미 추적한 파일, 비밀정보·모델·데이터, 새 clone에서의 재현 검증. 2·3·14주차에 다시 확인한다.

## 실습 시간과 예제를 맞춰 읽는 법

모든 주차의 `examples/`는 `period1/`·`period2/`·`period3/`로 구분한다.
**`lab.md`의 교시 → 같은 번호의 예제 README → 해당 시간의 파일** 순서로 읽는다.

- 각 README의 시간표는 해당 실습지의 30분 시간표다. 설명·시연 20분과 휴식 10분은 별도다.
- 폴더마다 제공 코드·참조 구현·학생용 양식 중 어떤 자료인지 표시한다. TODO와 평가 문제는 직접 해결한다.
- 실행에 필요한 소스·설정·작은 데이터의 위치를 각 교시 README에 밝힌다. 5주차 규격으로 개편한 예제는 한 uv 프로젝트의 `src/`를 함께 사용한다. 10~13주차의 보드 연결·평가는 공용 `tools/bleuno-control`을 가져온다.
- 개인 실습은 이전 교시의 작업을 이어간다. 다음 폴더 전체를 덮어쓰지 않고, 실습지에서 지정한 새 파일·변경 부분만 적용한다.
- 이전에 만든 인덱스·학습 어댑터·보고서가 필요하면 해당 README의 준비 절차에 따라 전달한다.
- 기존 통합 예제 경로는 이전 링크와 선택 확장용으로 남아 있다. 기본 실습 진입점은 각 주차의 `examples/README.md`다.


## 운영 기준

- 15주, 주 3시간 = **60분 블록 3개**(1·2·3교시)
- 매 블록: 설명·시연 20분 + 직접 해결 실습 30분 + 휴식 10분
- 주당 합계: 설명·시연 60분 + 실습 90분 + 휴식 30분
- 분반 시간표에 따라 블록이 `2 + 1` 또는 `1 + 2`로 이틀에 나뉜다. 블록 순서는 바꾸지 않으며, 각 블록은 하루가 바뀌어도 이어서 시작할 수 있도록 "이어받는 것"을 밝힌다.
- 실습 순환: 문제 읽기 → 예상 → 실행·구현 → 관찰 → 오류 설명 → 기록·변형
- 실습 결과는 개인·팀 저장소에 누적하고, 4·8·12·15주차 종합과제에서만 제출한다.
- 평가 주차(8·15주차)는 기관 시간표와 분반 인원에 따라 실제 운영 시간이 달라질 수 있으며, 공개 자료에는 평가 구조와 연습 절차만 둔다.

## 주차 폴더 구성

각 폴더는 같은 구조를 사용한다.

| 파일·폴더 | 역할 |
|---|---|
| `README.md` | 학습 질문, 목표, 누적 결과물, 3블록 흐름, 완료 기준, 제출 증거 |
| `slides.md` | Marp 호환 PT 원고. 세 번의 20분 설명·시연용. `---`가 슬라이드 구분자 |
| `lab.md` | 세 번의 30분 실습 문제, 시간 배분, 단계별 힌트, 검증, 확장 |
| `examples/` | uv 프로젝트 형태의 실행 예제와 템플릿. `uv.lock`은 환경 기준표 확정 후 기준 PC에서 생성한다 |
| `walkthrough.md` | 1·3·4·5·6·7·10·12주차. 시연·실습을 순서대로 재현하는 절차서 |
| 평가 문서 | 4·8·12·15주차 종합과제 안내·루브릭, 8주차 실기평가 구조·루브릭, 12주차 제어 모델 학습 과제, 14주차 공개 평가 규격, 15주차 AI 성능·레포트 루브릭 |

PT 원고는 내용 변경 이력을 추적하기 위해 Markdown으로 관리한다. 필요할 때 Marp CLI 또는 VS Code Marp 확장으로 HTML, PDF, PPTX로 내보낼 수 있다. 강의 대본과 실습 해답은 강의자가 별도 관리한다(비공개).

## 주차 목록

| 주차 | 챕터 | 주제 | 누적 산출물 | 폴더 |
|---:|---|---|---|---|
| 1 | 1장 | 오리엔테이션과 오픈소스 AI 생태계 | 환경 점검표, 첫 uv 실행, 개인 저장소 | [`week01_oss_ai_ecosystem`](week01_oss_ai_ecosystem) |
| 2 | 1장 | Git/GitHub 협업과 라이선스 | PR·리뷰 근거, LICENSE, 라이선스 표 | [`week02_git_github_license`](week02_git_github_license) |
| 3 | 1장 | 재현 가능한 Python 오픈소스 프로젝트 | uv 프로젝트, CLI, 설정 로더 | [`week03_reproducible_python`](week03_reproducible_python) |
| 4 | 1장 종합 | Ollama와 로컬 LLM | Ollama 클라이언트, Modelfile, 1차 종합과제 | [`week04_ollama_local_llm`](week04_ollama_local_llm) |
| 5 | 2장 | LangChain 맛보기 | 프롬프트 연결, 대화 기억·스트리밍 | [실행 예제](week05_langchain_basics/README.md) |
| 6 | 2장 | 임베딩·검색·RAG | 신화 50편 검색, 출처 있는 신화 도우미, 내 문서 도우미 | [실행 예제](week06_embeddings_rag/README.md) |
| 7 | 2장 | PEFT/LoRA 경량 파인튜닝 | 작은 데이터·어댑터·전후 비교 | [실행 예제](week07_peft_lora/README.md) |
| 8 | 2장 종합 | 수시평가와 2차 종합과제 | 실기평가, 출처 기록·RAG 미니프로젝트 | [`week08_midterm`](week08_midterm) |
| 9 | 3장 | Streamlit으로 AI 앱 만들기 | 첫 화면, 대화 앱, 문서 RAG 앱 | [실행 예제](week09_streamlit_apps/README.md) |
| 10 | 3장 | 시뮬레이터와 Ollama 툴 호출 | 자연어 요청·함수·인자·실제 LED 상태 | [실습 자료](week10_simulator_control/README.md) |
| 11 | 3장 | 초소형 모델의 툴 호출 | Needle 제어, 같은 문항의 정확도·시간 비교 | [`week11_tiny_tool_calling`](week11_tiny_tool_calling) |
| 12 | 3장 종합 | 제어 모델 LoRA 학습·복원 | 명령 데이터, 어댑터, 같은 조건의 전후 비교 | [`week12_control_lora`](week12_control_lora) |
| 13 | 4장 | 제어 평가와 Streamlit 앱 | 실패 분석, 개선 실험, LED 제어 화면 | [`week13_control_streamlit`](week13_control_streamlit) |
| 14 | 4장 | 기말 챗봇 과제와 공개 성능 평가 | 공개 평가세트·도구, 개선 실험, 개발 보고서 | [`week14_chatbot_project`](week14_chatbot_project) |
| 15 | 4장 종합 | AI 성능 평가와 개발 보고서 | 발표 항목을 비공개 성능 평가로 대체, 레포트 별도 평가 | [`week15_final_evaluation`](week15_final_evaluation) |

## 누적 프로젝트 줄거리

선택 특강은 [Hugging Face Hub 분석](../specials/huggingface_hub/README.md)과 [PyTorch 텐서·회귀 모델](../specials/pytorch_basics/README.md)이다. 정규 앱 실습의 선행 조건으로 두지 않는다. 앱 완성 후 남는 시간의 얼굴·이미지 유사도, 음성 인식·출력, 소형 모델 비교는 [9주차 선택 확장](week09_streamlit_apps/README.md#남는-시간의-선택-확장)을 참고한다.

학생(또는 팀)은 학기 내내 "로컬 AI 도우미"를 구현하며 배운 내용을 이어 쓴다. 기말과제는 14주차에 공개한 대학 소개 챗봇과 공통 평가 규격을 따른다. 개인·팀 제출 방식은 강좌 공지에서 정한다.

| 구간 | 누적 내용 | 종합 확인 |
|---|---|---|
| 1~4주 | 개인 저장소, 라이선스, uv 프로젝트 골격, Ollama API 클라이언트 CLI | 4주차 1차 종합과제 |
| 5~8주 | LangChain 대화, RAG, 작은 LoRA 실험 | 8주차 2차 종합과제·실기평가 |
| 9~12주 | Streamlit 앱, 시뮬레이터 제어, 초소형 모델, LoRA 학습·복원 | 12주차 3차 종합과제 |
| 13~15주 | 제어 평가·앱 연결, 공개 평가·개선 실험, 개발 보고서 | 15주차 기말과제: AI 성능 점수와 레포트 점수 |

## 교재 검증용 기본값

주차의 소스 상수와 `uv.lock`을 함께 확인한다. 새 예제는 모델·주소·학습 값을 대문자 상수로 두며, 환경변수와 명령행 옵션을 필수 설정 단계로 추가하지 않는다.

| 범위 | 기본값 | 확인할 위치 |
|---|---|---|
| 10주차 Ollama | `qwen3.5:2b`, `http://127.0.0.1:11434` | 주차 `src/shared`와 공용 `models.py` |
| 11주차 작은 모델 | Needle 3, `cactus-compute==4.2.0` | 공용 `needle_predictor` |
| 12주차 학습 | CPU에서 가능한 로컬 LoRA, 48개 명령 예제 | `ex02_train` 상수와 실제 소요 시간 |
| 13주차 앱 | 12주차의 `tuned.cact`, Streamlit | 주차 `src/shared`, `ex03_app` |
| 시뮬레이터 | TCP 8266, HTTP 8080, LED 0~3 | [공용 제어 도구](../../tools/bleuno-control/README.md) |

Ollama의 모델 태그, Needle 엔진·가중치, 학습 어댑터와 Python 패키지 버전을 기록한다.
모델 다운로드는 수업 전에 마치고, 실제 학기의 장비·모델 조건은 [환경 기준표](../../environment_baseline_template.md)에서 확정한다.
공용 코드와 모델을 사용하는 10~13주차는 저장소 전체 구조를 유지한다.

기존 거버넌스·데이터 평가·서비스 배포·CI 원고는 [선택 자료](../specials/project_delivery/README.md)에 보존했다. 이전 원고의 설정 방식과 제출 조건을 새 정규 과제에 적용하지 않는다.

## 자료 작성 원칙

- `slides.md`에는 20분 × 3에 필요한 핵심 개념만 두고 긴 발화는 대본으로 분리한다.
- 예제는 실습지의 교시·문제 순서와 일치하게 나눈다. Python은 uv 프로젝트로 구성하고, 작은 공개 샘플 데이터를 함께 제공한다.
- `lab.md`에는 정답 전체 대신 완료 조건, 관찰 항목과 단계별 힌트를 둔다.
- 모든 실습은 정상 경로와 최소 한 개의 실패·경계 경로를 확인한다.
- GPU가 없거나 실패할 때의 CPU·소형 모델 대체 경로를 예제와 대본에 함께 둔다.
- Python 환경·의존성·실행은 `uv`로 관리한다. 예제는 검증한 버전을 lock 파일에 고정하고 학기별 환경 기준표와 맞춘다.
- 비밀정보는 공개 자료에 넣지 않는다. 학생용 시작본과 강의자용 해답을 분리한다.
- 평가 문서에는 100점 상대 배점만 두고, 실제 성적 비율·마감·분반 정보는 학교 운영 문서에 둔다.

## 공식 기준 자료

- [Open Source Initiative — 오픈소스 정의와 라이선스](https://opensource.org/licenses)
- [OSI — Open Source AI Definition](https://opensource.org/ai)
- [GitHub Docs](https://docs.github.com/)
- [uv 문서](https://docs.astral.sh/uv/)
- [Ollama 문서](https://docs.ollama.com/)
- [Hugging Face Hub 문서](https://huggingface.co/docs/hub/)
- [Transformers 문서](https://huggingface.co/docs/transformers/)
- [PEFT 문서](https://huggingface.co/docs/peft/)
- [PyTorch 튜토리얼](https://docs.pytorch.org/tutorials/)
- [FastAPI 문서](https://fastapi.tiangolo.com/)
- [pytest 문서](https://docs.pytest.org/)
