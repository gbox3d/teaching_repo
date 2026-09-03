# 주차별 강의 자료

## 운영 기준

- 15주, 주 3시간 = **60분 블록 3개**(1·2·3교시)
- 매 블록: 설명·시연 20분 + 직접 해결 실습 30분 + 휴식 10분
- 주당 합계: 설명·시연 60분 + 실습 90분 + 휴식 30분
- 분반 시간표에 따라 블록이 `2 + 1` 또는 `1 + 2`로 이틀에 나뉜다. 블록 순서는 바꾸지 않으며, 각 블록은 하루가 바뀌어도 이어서 시작할 수 있도록 "이어받는 것"을 밝힌다.
- 실습 순환: 문제 읽기 → 예상 → 실행·구현 → 관찰 → 오류 설명 → 기록·변형
- 실습 결과는 개인·팀 저장소에 누적하고, 4·8·12·15주차 종합과제에서만 제출한다.
- 평가·발표 주차(8·9·15주차)는 기관 시간표와 분반 인원에 따라 실제 운영 시간이 달라질 수 있으며, 공개 자료에는 평가 구조와 연습 절차만 둔다.

## 주차 폴더 구성

각 폴더는 같은 구조를 사용한다.

| 파일·폴더 | 역할 |
|---|---|
| `README.md` | 학습 질문, 목표, 누적 결과물, 3블록 흐름, 완료 기준, 제출 증거 |
| `slides.md` | Marp 호환 PT 원고. 세 번의 20분 설명·시연용. `---`가 슬라이드 구분자 |
| `lab.md` | 세 번의 30분 실습 문제, 시간 배분, 단계별 힌트, 검증, 확장 |
| `examples/` | uv 프로젝트 형태의 실행 예제와 템플릿. `uv.lock`은 환경 기준표 확정 후 기준 PC에서 생성한다 |
| `walkthrough.md` | 1·3·4·7·10·12주차. 시연·실습을 `할 일 → 예상 결과 → 확인` 순으로 재현하는 절차서 |
| 평가 문서 | 4·8·12·15주차 종합과제 안내·루브릭, 8주차 실기평가 구조·루브릭, 9주차 제안서 양식·발표 루브릭, 15주차 기말·발표 루브릭 |

PT 원고는 내용 변경 이력을 추적하기 위해 Markdown으로 관리한다. 필요할 때 Marp CLI 또는 VS Code Marp 확장으로 HTML, PDF, PPTX로 내보낼 수 있다. 강의 대본과 실습 해답은 강의자가 별도 관리한다(비공개).

## 주차 목록

| 주차 | 챕터 | 주제 | 누적 산출물 | 폴더 |
|---:|---|---|---|---|
| 1 | 1장 | 오리엔테이션과 오픈소스 AI 생태계 | 환경 점검표, 첫 uv 실행, 개인 저장소 | [`week01_oss_ai_ecosystem`](week01_oss_ai_ecosystem/) |
| 2 | 1장 | Git/GitHub 협업과 라이선스 | PR·리뷰 근거, LICENSE, 라이선스 표 | [`week02_git_github_license`](week02_git_github_license/) |
| 3 | 1장 | 재현 가능한 Python 오픈소스 프로젝트 | uv 프로젝트, CLI, 설정 로더 | [`week03_reproducible_python`](week03_reproducible_python/) |
| 4 | 1장 종합 | Ollama와 로컬 LLM | Ollama 클라이언트, Modelfile, 1차 종합과제 | [`week04_ollama_local_llm`](week04_ollama_local_llm/) |
| 5 | 2장 | Hugging Face Hub와 공개 자원 분석 | 모델 카드 분석, `SOURCES.md` | [`week05_huggingface_hub`](week05_huggingface_hub/) |
| 6 | 2장 | PyTorch 모델 활용 | 학습 루프, 임베딩, 실험 로그 | [`week06_pytorch_models`](week06_pytorch_models/) |
| 7 | 2장 | 임베딩·검색·RAG 응용 | 출처 있는 RAG 답변기, 평가셋 | [`week07_embeddings_rag`](week07_embeddings_rag/) |
| 8 | 2장 종합 | 수시평가와 2차 종합과제 | 실기평가, 라이선스 분석·RAG 미니프로젝트 | [`week08_midterm`](week08_midterm/) |
| 9 | 3장 | 프로젝트 제안과 오픈소스 거버넌스 | 팀 제안서, 팀 저장소, Issue·마일스톤 | [`week09_project_governance`](week09_project_governance/) |
| 10 | 3장 | PEFT/LoRA 경량 파인튜닝 | LoRA 어댑터, 실험 기록 | [`week10_peft_lora`](week10_peft_lora/) |
| 11 | 3장 | 데이터셋 구성과 모델 평가 | 데이터 카드, 평가 결과, 실패 분석 | [`week11_dataset_evaluation`](week11_dataset_evaluation/) |
| 12 | 3장 종합 | AI 서비스화와 배포 | FastAPI·Gradio 서비스, Dockerfile, 3차 종합과제 | [`week12_ai_service_deploy`](week12_ai_service_deploy/) |
| 13 | 4장 | 테스트·CI·보안·코드리뷰 | pytest·ruff, GitHub Actions, 감사 결과 | [`week13_test_ci_security`](week13_test_ci_security/) |
| 14 | 4장 | 릴리스와 커뮤니티 피드백 | v0.1.0 릴리스, 교차 재현, 피드백 Issue | [`week14_release_feedback`](week14_release_feedback/) |
| 15 | 4장 종합 | 기말평가와 프로젝트 발표 | 최종 시연, 재현 검증, 4차 종합과제 | [`week15_final_presentation`](week15_final_presentation/) |

## 누적 프로젝트 줄거리

학생(또는 2~3인 팀)은 학기 내내 하나의 "로컬 AI 도우미" 저장소를 키운다. 교재 예제는 이 줄거리를 따르는 참조 구현 조각이며, 학생 프로젝트 주제는 자유다.

| 구간 | 누적 내용 | 종합 확인 |
|---|---|---|
| 1~4주 | 개인 저장소, 라이선스, uv 프로젝트 골격, Ollama API 클라이언트 CLI | 4주차 1차 종합과제 |
| 5~8주 | 모델·데이터 라이선스 분석, 임베딩, 출처 있는 RAG 답변기 | 8주차 2차 종합과제·실기평가 |
| 9~12주 | 팀 제안, LoRA 실험, 데이터·평가, FastAPI/Gradio 서비스 베타 | 12주차 3차 종합과제 |
| 13~15주 | 테스트·CI·보안, v0.1.0 릴리스, 발표·재현 검증 | 15주차 4차 종합과제·기말평가·발표 |

## 교재 검증용 기본값

예제 코드는 모델 이름과 서버 주소를 환경변수로 읽는다. 아래는 교재를 작성·검증할 때 쓴 기본값이며, 실제 학기의 모델 ID·양자화·용량·버전은 [학기별 환경 기준표](../../environment_baseline_template.md)에서 담당 교수가 확정한다.

| 환경변수 | 기본값 | 용도 |
|---|---|---|
| `OLLAMA_HOST` | `http://localhost:11434` | Ollama 서버 주소 |
| `OLLAMA_MODEL` | `qwen3:8b` | 기본 생성 모델(RTX 4070 기준). CPU·소형 대체는 `qwen3:0.6b` |
| `OLLAMA_EMBED_MODEL` | `bge-m3` | Ollama 임베딩 모델 |
| `HF_TEXT_MODEL` | `Qwen/Qwen2.5-0.5B-Instruct` | Transformers 소형 생성 모델, LoRA 실습 기본 |
| `HF_EMBED_MODEL` | `intfloat/multilingual-e5-small` | sentence-transformers 임베딩 |
| `HF_HOME` | (설정 시) | Hugging Face 캐시 위치 |

모델 다운로드는 실습 시간에 하지 않는다. 수업 전 기준 PC에서 사전 캐시하고 여러 PC가 동시에 내려받지 않도록 배분한다.

### 생성 모델 태그를 고를 때

교재는 `think` 옵션으로 생각 과정을 켜고 끄는 것을 4주차에서 다루고, 이후 주차의 예제는 모두 생각 과정을 끈 상태로 답만 받는다.
따라서 기본 모델은 **생각 모드를 끌 수 있는 하이브리드 모델**이어야 한다.

Qwen3 계열에서 `0.6b`, `1.7b`, `8b`, `14b`, `32b` 태그는 생각 모드를 켜고 끌 수 있다.
`4b`, `30b`, `235b` 태그는 2507 갱신에서 생각 전용 빌드와 지시 전용 빌드로 나뉘었고, 접미사 없는 태그는 **생각 전용 빌드**를 가리킨다.
생각 전용 빌드에 `"think": false`를 보내도 생각 과정이 사라지지 않으므로 기본 모델로 쓰지 않는다.

환경 기준표에서 다른 모델을 확정하면 같은 기준으로 검토한다. 모델을 바꾸기 전에 `ollama show <태그>`로 생각 모드 지원 여부를 확인하고, 4주차 예제로 `--think` 있을 때와 없을 때의 출력이 실제로 달라지는지 한 번 확인한다.

## 자료 작성 원칙

- `slides.md`에는 20분 × 3에 필요한 핵심 개념만 두고 긴 발화는 대본으로 분리한다.
- 예제는 uv 프로젝트 하나에 한 주제만 담고, 외부 다운로드 없이 실행되는 자체 샘플 데이터를 우선한다.
- `lab.md`에는 정답 전체 대신 완료 조건, 관찰 항목과 단계별 힌트를 둔다.
- 모든 실습은 정상 경로와 최소 한 개의 실패·경계 경로를 확인한다.
- GPU가 없거나 실패할 때의 CPU·소형 모델 대체 경로를 예제와 대본에 함께 둔다.
- 전역 `pip install`을 쓰지 않는다. 정확한 버전은 환경 기준표에서 확정하고 본문에 고정하지 않는다.
- 비밀정보는 `.env.example` 형식만 제공한다. 학생용 starter와 강의자용 해답을 분리한다.
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
