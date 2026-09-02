# 11주차 — 데이터셋 구성과 모델 평가

## 이번 주 질문

> 내 데이터는 믿을 만하고 안전한가, 그리고 모델이 좋아졌다는 말을 무엇으로 증명하는가?

## 학습 목표

수업을 마치면 다음을 할 수 있다.

1. 원시 Q&A 데이터를 정규화·중복 제거·분할하는 파이프라인을 실행하고, 각 단계의 건수 변화를 보고서 파일로 설명한다.
2. 정규식으로 전화번호·이메일·주민등록번호 패턴을 검출해 마스킹하고, 오탐·미탐을 사람이 판단해 데이터 카드에 기록한다.
3. train/val/test 분리의 목적과 누수·벤치마크 오염을 구분하고, test split을 봉인해야 하는 이유를 설명한다.
4. 분류 지표(accuracy·precision·recall·F1)와 생성 지표(정확 일치·키워드 포함·유사도·형식 준수)가 각각 무엇을 재고 무엇을 놓치는지 예를 들어 설명한다.
5. 기준선 모델과 LoRA 모델을 같은 test split·같은 조건으로 정량 비교해 `outputs/eval-*.json`을 남긴다.
6. 모델 출력 20건을 3단계 루브릭으로 수동 채점하고 오류 유형을 붙인 뒤, 실패 사례 3개의 원인 가설과 개선안을 보고서로 쓴다.

## 누적 결과물

이번 주 실습은 12주차 **3차 종합과제**의 (a) "LoRA 실험 기록" 가운데 데이터 카드(`DATA_CARD.md`), 평가 결과(`outputs/eval-*.json`), 실패 분석(`FAILURE_ANALYSIS.md`)을 채운다. 10주차 `experiments/run-001.md`가 "학습했다"의 기록이라면 이번 주 산출물은 "좋아졌다"의 증거이고, 실패 분석의 「다음 실험」이 run-002의 출발점이 된다.

## 수업 흐름

| 블록 | 설명·시연 20분 | 직접 해결 실습 30분 | 핵심 증거 |
|---|---|---|---|
| 1교시 | 데이터 파이프라인과 데이터 카드 — 수집→정제→중복 제거→분할, train/val/test와 누수, 개인정보·저작권·편향 점검, 데이터 카드 항목 | 원시 데이터를 정제·마스킹·분할하기 — `clean.py`·`pii_check.py`·`split.py`로 `raw.jsonl` 48건을 처리하고 `DATA_CARD.md` 작성 | 정제 전후 건수(`clean_report.json`), PII 검출 목록(`pii_report.json`), `DATA_CARD.md` |
| 2교시 | 기준선과 지표 — 무엇으로 좋아졌다고 말하는가: 제로샷 기준선과 비교의 원칙, 분류·생성 지표, LLM-as-judge의 한계, 벤치마크 오염, 평가셋 봉인 | 기준선 vs LoRA 정량 비교 — `evaluate.py`로 샘플 예측을 채점해 지표를 익힌 뒤 10주차 기본 모델 vs 어댑터를 test 20문항으로 비교 | 비교표(`outputs/eval-*.json`), 자동 지표가 틀린 사례 1건 |
| 3교시 | 정성 평가와 실패 분석 — 오류 유형 분류표, 3단계 루브릭과 채점 일관성, 유해 출력·개인정보 유출 점검, 개선 루프, 3차 과제 준비 | 수동 채점과 실패 분석 보고 — 20개 출력을 루브릭으로 채점하고 `FAILURE_ANALYSIS.md`에 사례 3개와 다음 실험 작성 | 채점표(`outputs/scoring-*.md`), `FAILURE_ANALYSIS.md` |

각 블록은 설명·시연 20분, 실습 30분, 휴식 10분으로 운영한다. 분반 시간표에 따라 두 블록과 한 블록이 다른 날에 배치될 수 있으며, 블록 순서는 바꾸지 않는다.

## 준비물

- Git, VS Code, uv, PowerShell. 2교시 모델 모드는 NVIDIA GPU(기준 12 GB VRAM)에서 실행하며, GPU가 없으면 `--predictions` 모드와 `--device cpu --limit 5` 경로를 쓴다. 1·3교시는 GPU가 필요 없다.
- 수업 전 사전 캐시된 `HF_TEXT_MODEL`(교재 검증용 기본값 `Qwen/Qwen2.5-0.5B-Instruct`). 실습 시간에 모델을 내려받지 않는다.
- 10주차 산출물: `adapters/run-001/`(어댑터), `data/sample_sft.jsonl`(학습 데이터), `experiments/run-001.md`. 어댑터가 없어도 예제의 샘플 예측 파일로 2·3교시를 진행할 수 있다.
- 정확한 도구 버전은 [학기별 환경 기준표](../../../environment_baseline_template.md)에서 확정한다.
- 실제 이름, 학번, 전화번호, 이메일, 주민등록번호는 실습 데이터·데이터 카드·보고서에 넣지 않는다. 예제 데이터의 개인정보 패턴은 모두 가짜 값이다. 토큰은 `.env`에만 두고 `.env.example`만 커밋한다. 표시 이름은 `student01`, 팀명은 `team-a` 같은 수업용 값을 쓴다.

## 자료 안내

- [PT 원고](slides.md): 세 번의 20분 설명·시연용 Marp 자료
- [실습지](lab.md): 1·2·3교시 문제, 힌트, 검증, 확장
- [실행 예제](examples/README.md): `eval_lab/` uv 프로젝트 — 정제·개인정보 검출·분할·지표·평가·채점표 스크립트, 자체 작성 원시 데이터 48건, 샘플 예측 파일, 데이터 카드·실패 분석·채점표 양식
- 강의 대본: 강의자 별도 관리(비공개)

## 권장 진행 방식

1. 스크립트를 실행하기 전에 "몇 건이 지워질까", "어느 모델이 몇 점일까"를 먼저 적고 실행 결과와 비교한다.
2. 원본 `examples/eval_lab/`은 그대로 두고 개인 실습 폴더에 복사해 실행한다.
3. 매 단계의 보고서 JSON(`clean_report`, `pii_report`, `split_report`, `eval-*`)을 지우지 않는다. 데이터 카드와 실패 분석의 숫자는 전부 이 파일들에서 옮겨 적는다.
4. 자동 지표는 "무엇을 놓치는가"를 함께 적을 때만 증거가 된다. 숫자 하나마다 반례 문항 하나를 찾는다.
5. 기본 문제를 마친 뒤에만 확장 문제(패턴 추가, system 프롬프트 변경, Ollama 모델 비교)를 수행한다.

## 완료 기준

- [ ] `clean.py` 실행 후 원시 48건에서 제거된 4건의 id와 사유(정확 중복·근사 중복·빈 값)를 적고, 임계값을 바꿨을 때의 차이를 한 문장으로 적었다.
- [ ] `pii_check.py --action report`의 검출 3건에 대해 오탐 여부를 판단하고 조치(mask/drop)를 데이터 카드에 기록했다.
- [ ] `split.py` 결과 train/val/test 건수와 `leak_count` 0을 확인하고, seed를 바꾸면 test id가 달라지는 것과 10주차 학습 데이터와 겹치는 문항을 기록했다.
- [ ] `DATA_CARD.md`의 7개 절을 보고서 JSON의 값으로 채웠다.
- [ ] `evaluate.py --predictions`로 샘플 예측 2개를 채점하고, 형식은 통과했지만 내용이 틀린 문항 1개를 찾아 이유를 적었다.
- [ ] 기준선과 LoRA(어댑터가 없으면 기준선만)를 test split로 실제 생성·채점해 `outputs/eval-*.json`을 남겼다.
- [ ] 20개 출력을 3단계 루브릭으로 채점하고 짝과 5건의 일치율을 적었다.
- [ ] `FAILURE_ANALYSIS.md`에 서로 다른 유형의 사례 3개(증상·원인 가설·근거·개선안·검증 방법)와 "하나만 바꾸는" 다음 실험을 적었다.

## 제출 증거

이번 주는 별도 제출물이 없다. 아래 증거를 개인 저장소에 누적한다.

1. `evidence/week11/clean_report.json`, `pii_report.json`, `split_report.json`(`outputs/`는 `.gitignore`에 있으므로 증거 폴더로 복사한다)
2. `DATA_CARD.md`
3. `evidence/week11/eval-*.json` 2개(예측 모드 1건 + 모델 모드 1건)와 비교표(겹침 문항 제외 전후)
4. `evidence/week11/scoring-*.md`: 수동 채점 완료본(점수·오류 유형·메모·일치율)
5. `FAILURE_ANALYSIS.md`
6. `git log --oneline -3`: 보고서·카드·분석 파일만 커밋했음을 보이는 이력(`outputs/`·`adapters/`는 `.gitignore`)

터미널 출력과 JSON에는 사용자 홈 경로가 포함될 수 있다. 기록 전에 개인 식별 정보가 없는지 확인한다.

## 다음 주 연결

12주차 `week12_ai_service_deploy`에서 평가를 통과한 모델(또는 기본 모델)을 FastAPI 앱 서버와 Gradio UI로 감싸 다른 사람이 쓸 수 있는 서비스로 만든다. 이번 주 `DATA_CARD.md`·`eval-*.json`·`FAILURE_ANALYSIS.md`가 3차 종합과제 (a)의 내용이며, 실패 분석의 「다음 실험」은 run-002로 이어져 12주차 3교시의 과제 점검에서 함께 확인한다.

## 참고 자료

- [Datasets 문서 — Process(`train_test_split`)](https://huggingface.co/docs/datasets/process)
- [Hugging Face Hub 문서 — Dataset Cards](https://huggingface.co/docs/hub/datasets-cards)
- [Hugging Face Evaluate 문서](https://huggingface.co/docs/evaluate/)
- [scikit-learn 문서 — Metrics and scoring](https://scikit-learn.org/stable/modules/model_evaluation.html)
- [PEFT 문서 — LoRA](https://huggingface.co/docs/peft/package_reference/lora)
- [Transformers 문서 — Generation](https://huggingface.co/docs/transformers/main_classes/text_generation)
