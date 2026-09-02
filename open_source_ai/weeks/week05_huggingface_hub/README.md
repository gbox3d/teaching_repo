# 5주차 — Hugging Face Hub와 공개 자원 분석

## 이번 주 질문

> 공개된 모델과 데이터가 정말 내 프로젝트에 쓸 수 있는 것인지 어떤 문서와 정보로 판단하는가?

## 학습 목표

수업을 마치면 다음을 할 수 있다.

1. Hub 저장소(models·datasets·spaces)의 구조와 모델 카드의 항목(용도·학습 데이터·평가·한계·편향·라이선스)을 읽고 사용 가능 여부를 근거와 함께 판정한다.
2. 모델 ID와 revision(commit hash), 캐시 위치(`HF_HOME`)와 구조(blobs·refs·snapshots), 오프라인 모드로 재현 가능한 모델 참조를 기록한다.
3. Transformers `pipeline`으로 분류·생성 태스크를 모델·revision·device를 명시해 실행하고 CPU와 GPU의 로드·추론 시간을 비교한다.
4. `datasets`로 로컬 파일과 Hub 데이터셋을 같은 API로 열어 필드 구조·건수·샘플을 기록하고 스트리밍으로 큰 데이터의 앞부분만 살펴본다.
5. Dataset Card와 데이터 라이선스(CC 계열·연구 전용)에서 상업 이용·재배포·개인정보 위험을 판단한다.
6. 사용한 모델·데이터의 출처를 `SOURCES.md` 한 표(이름·revision·라이선스·용도·변경 내용)로 남긴다.

## 누적 결과물

이번 주의 `model_cards.md`와 `SOURCES.md`는 8주차 2차 종합과제 「라이선스 분석 보고」의 첫 행들이 된다. 2교시에서 기록한 모델 ID와 commit hash는 6·7주차의 임베딩·RAG 답변기가 쓰는 모델 고정값이 되고, 3교시의 `datasets` 사용법은 10주차 LoRA 학습 데이터 준비에서 그대로 쓴다.

## 수업 흐름

| 블록 | 설명·시연 20분 | 직접 해결 실습 30분 | 핵심 증거 |
|---|---|---|---|
| 1교시 | Hub 구조와 모델 카드 — models·datasets·spaces 저장소 구조, 모델 카드 읽는 순서(라이선스·용도·학습 데이터·평가·한계), 카드 메타데이터(YAML), gated 모델과 토큰, revision(commit hash) 고정, 캐시 구조(`HF_HOME`, blobs·refs·snapshots)·용량 계산·오프라인 모드 | 모델 카드 분석표와 캐시 보고 — 지정 모델 3개(`Qwen/Qwen2.5-0.5B-Instruct`, `intfloat/multilingual-e5-small`, 라이선스 제한이 있는 모델 1개)의 라이선스·SPDX·의도된 용도·금지 용도·학습 데이터 공개 여부·한계를 `model_cards.md`에 채우고, `cache_report.py`로 캐시 용량과 commit hash를 확인 | `model_cards.md`, `cache_report.py` 출력 요약 |
| 2교시 | Transformers pipeline 첫 추론 — pipeline이 감추는 세 단계, task 종류와 모델 명시, 한국어 모델 고르기, `device`·`device_map`·dtype, chat template로 생성 모델 호출, 경고 메시지 읽기와 시간 측정 원칙 | pipeline으로 분류와 생성 실행하기 — `pipeline_demo.py`로 감성 분류(소형 다국어 모델)와 텍스트 생성(`HF_TEXT_MODEL`)을 CPU와 GPU에서 실행, revision을 commit hash로 고정해 재실행, 실패 경로 재현, 시간 비교표 작성 | 두 태스크 출력 JSON, CPU/GPU 시간 비교표(`pipeline_report.md`) |
| 3교시 | datasets와 출처 기록 — `load_dataset`·split·features, 로컬 파일도 같은 API, 스트리밍, Dataset Card 읽기, 데이터 라이선스(CC 계열·연구 전용)와 개인정보·저작권 위험, `SOURCES.md` 출처 기록표 | 데이터셋 살펴보기와 출처 기록표 — `dataset_peek.py`로 자체 샘플 데이터의 필드 구조·건수·샘플 5개 기록, 공개 데이터셋 1개의 Dataset Card 분석, `SOURCES.md`에 모델 2개 + 데이터 1개 기록 | `SOURCES.md`, 데이터 구조 기록 |

각 블록은 설명·시연 20분, 실습 30분, 휴식 10분으로 운영한다. 분반 시간표에 따라 두 블록과 한 블록이 다른 날에 배치될 수 있으며, 블록 순서는 바꾸지 않는다.

## 준비물

- Git, VS Code, uv, PowerShell. 브라우저에서 `huggingface.co`의 모델·데이터 카드 페이지를 열 수 있어야 한다(카드 열람은 계정 없이 가능하다).
- 사전 캐시된 모델: 생성용 `HF_TEXT_MODEL`(교재 검증용 기본값 `Qwen/Qwen2.5-0.5B-Instruct`)과 분류용 `HF_CLS_MODEL`(기본값은 [실행 예제](examples/README.md)의 기본값 표 참고). 실습 시간에 새로 내려받지 않는다.
- `examples/hf_explore`를 개인 저장소에 복사한 폴더에서 `uv sync`를 수업 전에 마쳐 둔다(첫 sync는 torch 설치로 오래 걸린다).
- 4주차 산출물: 개인 저장소와 `.env`·`config.py` 패턴. 이번 주 파일은 같은 저장소에 누적한다.
- 정확한 도구 버전, 모델 ID·revision·용량은 [학기별 환경 기준표](../../../environment_baseline_template.md)에서 확정한다.
- Hugging Face 토큰, 비밀번호, 실명, 학번을 실습 파일과 공개 저장소에 넣지 않는다. gated 모델의 파일 다운로드는 이번 주 실습 범위 밖이며, 토큰을 쓰더라도 `.env`에만 둔다. 표시 이름은 `student01`, 팀명은 `team-a` 같은 수업용 값을 쓴다.

## 자료 안내

- [PT 원고](slides.md): 세 번의 20분 설명·시연용 Marp 자료
- [실습지](lab.md): 1·2·3교시 문제, 힌트, 검증, 확장
- [실행 예제](examples/README.md): `hf_explore/` uv 프로젝트(`cache_report.py`·`pipeline_demo.py`·`dataset_peek.py`·자체 샘플 데이터), 모델 카드 분석표·출처 기록표 템플릿
- 강의 대본: 강의자 별도 관리(비공개)

## 권장 진행 방식

1. 카드를 열기 전에 라이선스·용량·한국어 지원을 먼저 예상하고, 카드에서 근거 문장을 찾아 예상과 비교한다.
2. 모델을 부를 때는 항상 `model=`·`revision=`·`device=`를 쓰고, 출력 JSON의 commit hash를 기록 문서에 옮겨 적는다.
3. 시간 측정은 워밍업 뒤 두 번째 호출을 기준으로 하고, 장치·dtype·토큰 수 같은 조건을 함께 적는다.
4. 데이터는 전체를 열기 전에 5개만 보고 구조와 라이선스를 판단한다.
5. 실패 메시지는 첫 줄만 옮겨 적고 "무엇을 확인해야 하는가"를 한 문장으로 덧붙인다.

## 완료 기준

- [ ] 모델 3개의 라이선스·SPDX 식별자·의도된 용도·금지 용도·학습 데이터 공개 여부·한계를 `model_cards.md`에 채우고 판정 근거를 적었다.
- [ ] `cache_report.py` 출력에서 캐시 위치·총 용량·저장소별 commit hash를 확인하고 암산 용량과 실제 용량의 차이를 설명했다.
- [ ] `pipeline_demo.py`로 분류 5문장과 생성 1건을 실행해 `outputs/pipeline-*.json`을 얻었다.
- [ ] CPU와 GPU(GPU가 없으면 CPU 두 번)의 로드·워밍업·추론 시간을 표로 비교하고 차이의 이유를 적었다.
- [ ] 잘못된 revision 또는 오프라인 상태의 실패 메시지를 재현하고 한 줄로 요약했다.
- [ ] `dataset_peek.py`로 로컬 샘플의 필드 구조·건수·샘플 5개를 기록하고 스트리밍과의 차이를 확인했다.
- [ ] 공개 데이터셋 1개의 Dataset Card에서 라이선스·수집 방법·개인정보 항목을 찾았다.
- [ ] `SOURCES.md`에 모델 2개와 데이터 1개를 revision·라이선스·용도와 함께 적고 commit했다.

## 제출 증거

이번 주는 별도 제출물이 없다. 아래 증거를 개인 저장소에 누적한다.

1. `model_cards.md`: 예상표, 분석표, 판정, 캐시 보고 요약
2. `pipeline_report.md`: 분류·생성 출력 요약, CPU/GPU 시간 비교표, 실패 메시지 요약
3. `SOURCES.md`: 모델 2개 + 데이터 1개
4. `git log --oneline -3` 결과(이번 주 commit 3개)

`outputs/` 폴더는 `.gitignore`로 제외되므로 필요한 값은 Markdown 문서에 옮겨 적는다. 터미널 출력과 캐시 경로에는 사용자 홈 경로가 포함될 수 있으니 기록 전에 개인 식별 정보가 없는지 확인한다.

## 다음 주 연결

6주차 `week06_pytorch_models`에서는 이번 주 `pipeline` 한 줄 안쪽으로 들어간다. 토크나이저가 만든 텐서가 GPU로 옮겨져 어떻게 계산되는지, 학습 루프가 무엇을 반복하는지를 PyTorch로 직접 다룬다. 이번 주 `SOURCES.md`에 적은 모델 ID와 commit hash를 그대로 쓴다.

## 참고 자료

- [Hugging Face Hub 문서](https://huggingface.co/docs/hub/)
- [Model Cards](https://huggingface.co/docs/hub/model-cards)
- [Dataset Cards](https://huggingface.co/docs/hub/datasets-cards)
- [Transformers Pipelines](https://huggingface.co/docs/transformers/main_classes/pipelines)
- [Datasets 문서](https://huggingface.co/docs/datasets/)
- [huggingface_hub 캐시 관리](https://huggingface.co/docs/huggingface_hub/guides/manage-cache)
