# 5주차 — Hugging Face Hub와 공개 자원 분석

## 이번 주 질문

> 공개된 모델과 데이터가 정말 내 프로젝트에 쓸 수 있는 것인지 어떤 문서와 정보로 판단하는가?

## 학습 목표

수업을 마치면 다음을 할 수 있다.

1. Hub 저장소(models·datasets·spaces)의 구조와 모델 카드의 항목(용도·학습 데이터·평가·한계·편향·라이선스)을 읽고 사용 가능 여부를 근거와 함께 판정한다.
2. `huggingface_hub`로 모델 정보·카드·캐시를 조회해 모델 ID와 revision(commit hash), 캐시 위치(`HF_HOME`)를 기록한다.
3. Transformers `pipeline`으로 분류·생성 태스크를 모델·revision·device를 명시해 실행하고 CPU와 GPU(또는 Apple `mps`)의 로드·추론 시간을 비교한다.
4. `datasets`로 로컬 파일과 Hub 데이터셋을 같은 API로 열어 필드 구조·건수·샘플을 기록하고 스트리밍으로 큰 데이터의 앞부분만 살펴본다.
5. Dataset Card와 데이터 라이선스(CC 계열·연구 전용)에서 상업 이용·재배포·개인정보 위험을 판단한다.
6. 사용한 모델·데이터의 출처를 `SOURCES.md` 한 표(이름·revision·라이선스·용도·변경 내용)로 남긴다.
7. `uv init --package --python 3.12`로 배포 표준 구조의 프로젝트를 만들고, 예제가 함께 쓰는 설정·데이터를 `src/shared/` 공용 패키지로 가져다 쓰는 구조를 설명한다.

## 누적 결과물

이번 주의 `model_cards.md`와 `SOURCES.md`는 8주차 2차 종합과제 「라이선스 분석 보고」의 첫 행들이 된다. 2교시에서 기록한 모델 ID와 commit hash는 6·7주차의 임베딩·RAG 답변기가 쓰는 모델 고정값이 되고, 3교시의 `datasets` 사용법은 10주차 LoRA 학습 데이터 준비에서 그대로 쓴다.

## 수업 흐름

| 블록 | 설명·시연 20분 | 직접 해결 실습 30분 | 핵심 증거 |
|---|---|---|---|
| 1교시 | Hub 구조와 모델 카드 — 저장소 구조, 카드 읽는 순서(라이선스·용도·학습 데이터·평가·한계), 카드 YAML, gated 모델, revision(commit hash) 고정, 캐시 구조와 용량 | `uv init --package --python 3.12`로 프로젝트 만들기, `uv run ex01`(Hub 정보)·`ex02`(카드)·`ex03`(캐시)로 지정 모델 3개 분석 | `model_cards.md` |
| 2교시 | Transformers pipeline 첫 추론 — pipeline이 감추는 세 단계, task와 모델 명시, 한국어 모델 고르기, device·dtype, messages로 생성, 공용 패키지 `src/shared/` | `uv run ex04`(분류)·`ex05`(생성)를 자동 장치와 CPU에서 실행, revision 고정 후 재실행, 잘못된 revision 재현 | `pipeline_report.md` |
| 3교시 | datasets와 출처 기록 — 로컬 파일도 같은 API, features·filter, 스트리밍, Dataset Card, 데이터 라이선스(CC 계열)와 개인정보 위험, `SOURCES.md` | `uv run ex06`(로컬 데이터)·`ex07`(Hub 스트리밍)으로 구조·라이선스 기록, `SOURCES.md`에 모델 2개 + 데이터 1개 | `SOURCES.md` |

각 블록은 설명·시연 20분, 실습 30분, 휴식 10분으로 운영한다. 분반 시간표에 따라 두 블록과 한 블록이 다른 날에 배치될 수 있으며, 블록 순서는 바꾸지 않는다.

## 준비물

- Git, VS Code, uv, PowerShell. 브라우저에서 `huggingface.co`의 모델·데이터 카드 페이지를 열 수 있어야 한다(카드 열람은 계정 없이 가능하다).
- 수업 전에 받아 둔 모델: 생성용 `Qwen/Qwen2.5-0.5B-Instruct`, 분류용 `lxyuan/distilbert-base-multilingual-cased-sentiments-student`. [수업 전 준비](examples/README.md#수업-전-준비-강의자조교)의 `hf download`로 받는다. 실습 시간에 새로 내려받지 않는다.
- 교시 폴더마다 `uv sync`를 수업 전에 마쳐 둔다(1교시는 `huggingface_hub`만, 2교시는 torch·transformers, 3교시는 datasets). 예제 폴더에는 `.python-version`(3.12)이 있다.
- 1교시 Hub 조회와 3교시 `ex07` 스트리밍은 인터넷이 필요하다.
- Hugging Face 토큰은 이번 주에 필요 없다. gated 모델은 카드만 읽는다. 표시 이름은 `student01`, 팀명은 `team-a` 같은 수업용 값을 쓴다.

## 자료 안내

- [PT 원고](slides.md): 세 번의 20분 설명·시연용 Marp 자료
- [실습지](lab.md): 1·2·3교시 문제, 힌트, 확장
- [실행 예제](examples/README.md): `period1`(`ex01`~`ex03`) → `period2`(`ex04`·`ex05`, `src/shared/`) → `period3`(`ex06`·`ex07`, `src/shared/data/`)
- 강의 대본: 강의자 별도 관리(비공개)

## 권장 진행 방식

1. 카드를 열기 전에 라이선스·용량·한국어 지원을 먼저 예상하고, 카드에서 근거 절을 찾아 예상과 비교한다.
2. 모델은 항상 `model=`·`revision=`·`device=`를 적어 부른다. 이 값은 `src/shared/__init__.py` 한곳에 둔다.
3. 시간은 두 번째 실행을 기준으로 잰다. 첫 실행에는 다운로드·파일 확인이 섞인다.
4. 데이터는 전체를 열기 전에 앞 몇 행만 보고 구조와 라이선스를 판단한다.
5. 오류는 Traceback 맨 아래 줄을 옮겨 적고 "무엇을 확인해야 하는가"를 한 문장으로 덧붙인다.

## 완료 기준

- [ ] `uv init --package --python 3.12`로 만든 프로젝트와 교재 예제 폴더의 구조가 같은지 확인했다.
- [ ] 모델 3개의 라이선스·SPDX 식별자·의도된 용도·금지 용도·학습 데이터 공개 여부·한계를 `model_cards.md`에 채우고 판정 근거를 적었다.
- [ ] `ex01`의 commit과 `ex03`의 캐시 commit을 대조했다.
- [ ] `ex04`를 자동 장치와 CPU에서 실행해 시간을 비교하고, 한국어·영어 문장의 결과 차이를 설명했다.
- [ ] `ex05`를 revision 고정 전후로 실행하고 잘못된 revision의 오류를 기록했다.
- [ ] `ex06`·`ex07`로 로컬·Hub 데이터의 구조와 카드 라이선스를 기록했다.
- [ ] `SOURCES.md`에 모델 2개와 데이터 1개를 commit hash·SPDX·용도와 함께 적고 commit했다.

## 제출 증거

이번 주는 별도 제출물이 없다. 아래 증거를 개인 저장소에 누적한다.

1. `model_cards.md`: 예상표, 분석표, 판정, Hub 정보와 캐시 보고
2. `pipeline_report.md`: 분류·생성 결과, 시간 비교표, revision 고정·실패 결과
3. `SOURCES.md`: 모델 2개 + 데이터 1개
4. `git log --oneline -3` 결과(이번 주 commit 3개)

터미널 출력과 캐시 경로에는 사용자 홈 경로가 포함될 수 있으니 기록 전에 개인 식별 정보가 없는지 확인한다.

## 다음 주 연결

6주차 `week06_pytorch_models`에서는 이번 주 `pipeline` 한 줄 안쪽으로 들어간다. 토크나이저가 만든 텐서가 GPU로 옮겨져 어떻게 계산되는지, 학습 루프가 무엇을 반복하는지를 PyTorch로 직접 다룬다. 이번 주 `SOURCES.md`에 적은 모델 ID와 commit hash를 그대로 쓴다.

## 참고 자료

- [Hugging Face Hub 문서](https://huggingface.co/docs/hub/)
- [Model Cards](https://huggingface.co/docs/hub/model-cards)
- [Dataset Cards](https://huggingface.co/docs/hub/datasets-cards)
- [Transformers Pipelines](https://huggingface.co/docs/transformers/main_classes/pipelines)
- [Datasets 문서](https://huggingface.co/docs/datasets/)
- [hf 명령 사용법](https://huggingface.co/docs/huggingface_hub/guides/cli)
- [huggingface_hub 캐시 관리](https://huggingface.co/docs/huggingface_hub/guides/manage-cache)
