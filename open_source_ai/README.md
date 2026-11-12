# 오픈소스 AI 응용 공용 교재

## 목차

- [범위](#범위)
- [진입점](#진입점)
- [수업 시간 구조](#수업-시간-구조)
- [학교 적용](#학교-적용)
- [환경 원칙](#환경-원칙)

## 범위

오픈소스 생태계와 Git·GitHub 협업, 라이선스, 재현 가능한 Python 환경(uv), Ollama 로컬 LLM,
LangChain, 임베딩·RAG, PEFT/LoRA 경량 파인튜닝, Streamlit 앱,
초소형 모델의 시뮬레이터 제어·학습, 챗봇 성능 평가와 개발 보고서까지 연결하는 15주 오픈소스 AI 응용 교재다.

## 진입점

- 15주 교재 색인: [`weeks/README.md`](weeks/README.md)
- 선택 특강: [Hugging Face Hub와 공개 자원 분석](specials/huggingface_hub/README.md)
- 선택 특강: [PyTorch 텐서·저장·회귀 모델](specials/pytorch_basics/README.md)
- 선택 자료: [프로젝트 운영·서비스 배포·CI의 이전 강의](specials/project_delivery/README.md)
- 시뮬레이터 제어·학습: [10주차 시작](weeks/week10_simulator_control/README.md), [공용 제어 도구](../tools/bleuno-control/README.md)
- 제작 계획과 품질 검수 기준: [`materials_plan.md`](materials_plan.md)
- 기말 챗봇 과제와 공개 평가: [14주차 안내](weeks/week14_chatbot_project/README.md)
- 과목별 설치 프로그램: [`ta_setup_guide.md`](ta_setup_guide.md)
- uv 설치·갱신·Python 환경·`uv run` 실습: [`uv_guide.md`](uv_guide.md)
- GitHub 소스 배포와 `.gitignore` 주의사항: [`github_distribution.md`](github_distribution.md)
- 실습실 PC 의 GitHub 로그인 정리(공통 도구): [`../tools/github-classroom-pc-reset/`](../tools/github-classroom-pc-reset/README.md)
- 공통 설치 프로그램: [`../ta_lab_setup_guide.md`](../ta_lab_setup_guide.md)
- 환경 기준표: [`../environment_baseline_template.md`](../environment_baseline_template.md)

## 수업 시간 구조

- 한 주는 **60분 블록 3개**(1·2·3교시)이며, 각 블록은 설명·시연 20분 + 직접 해결 실습 30분 + 휴식 10분이다.
- 분반 시간표에 따라 블록이 `2 + 1` 또는 `1 + 2`로 이틀에 나뉜다. 자료는 일차가 아니라 교시(블록) 단위로 쓴다.
- 종합과제는 4·8·12·15주차에만 있고, 나머지 주차의 실습 결과는 다음 종합과제의 재료로 누적한다.

## 학교 적용

- 학교명·분반·실제 배점·시험·마감·LMS 정보는 학교 폴더에서 관리한다.
- 학교별 표지와 일정은 배포본에서 적용하고 공용 원고에 직접 넣지 않는다.
- 루브릭의 배점은 100점 상대 배점이며, 실제 성적 비율은 학교 운영 문서가 정한다.
- 강의 대본과 실습 해답은 강의자가 별도 관리한다(비공개).

## 환경 원칙

- Python 패키지는 `uv` 기반 격리환경과 lock 파일로 재현한다.
- Python·학습 도구·모델·GPU 조건은 환경 기준표에서 확정한다. 주차별 상수와 lock 파일, [검증용 기본값](weeks/README.md#교재-검증용-기본값)을 함께 확인한다.
- 모델 다운로드 크기와 캐시 위치를 먼저 계산하고, 수업 직전 여러 PC에서 동시에 내려받지 않는다.
- GPU 실패 때 사용할 CPU 또는 소형 모델 대체 경로를 함께 검증한다.
- 예제의 `uv.lock`은 환경 기준표 확정 후 기준 PC에서 생성해 커밋한다.
