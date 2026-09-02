# 10주차 — PEFT/LoRA 경량 파인튜닝

## 이번 주 질문

> 12 GB GPU로 소형 모델의 말투·형식을 바꾸는 학습을 몇 분 안에 재현 가능하게 수행하려면 무엇을 고정하고 무엇을 기록해야 하는가?

## 학습 목표

수업을 마치면 다음을 할 수 있다.

1. 전이학습, 전체 파인튜닝, PEFT의 차이를 학습 파라미터 수와 메모리로 설명한다.
2. LoRA의 rank, alpha, target modules가 학습 파라미터 비율에 미치는 영향을 표로 계산한다.
3. instruction/output 데이터를 chat template로 감싸고 라벨 마스킹이 적용된 학습 입력을 확인한다.
4. `transformers.Trainer`와 `peft`로 소형 모델의 LoRA 어댑터를 seed를 고정해 학습하고 loss를 기록한다.
5. 같은 프롬프트·같은 조건으로 기본 모델과 어댑터 적용 모델의 출력을 비교한다.
6. 재현에 필요한 항목만 담은 실험 기록(`experiments/run-001.md`)을 작성한다.

## 누적 결과물

이번 주 실습은 12주차 **3차 종합과제**(PEFT/LoRA 실험 기록·AI 서비스 베타)의 첫 실험 기록 `experiments/run-001.md`를 만든다. 9주차 팀 제안서에서 고른 모델 후보 중 하나에 LoRA를 붙여 학습 파라미터·VRAM·loss·전후 출력을 남기며, 11주차에서 이 데이터와 모델을 정제·평가하고 12주차에서 서비스로 감싼다.

## 수업 흐름

| 블록 | 설명·시연 20분 | 직접 해결 실습 30분 | 핵심 증거 |
|---|---|---|---|
| 1교시 | 전체를 다시 배우지 않고 일부만 바꾸기 — 전이학습·전체 파인튜닝·PEFT 비교, LoRA 직관(ΔW = BA, r, alpha, target modules), 학습 메모리 네 덩어리, 12 GB 현실, 프롬프트 vs LoRA 선택 기준 | 어댑터 붙이고 학습 파라미터 세기 — `lora_setup.py`로 `HF_TEXT_MODEL`에 LoRA 적용, r을 4·8·16으로 바꿔 학습 파라미터 비율표와 VRAM 예측표 작성 | 학습 파라미터 비율표, VRAM 예측표(`outputs/setup-*.md`) |
| 2교시 | 데이터가 모델에 들어가는 길: 템플릿·마스킹·Trainer — SFT 데이터 형식, chat template, 라벨 마스킹, `Trainer` 구조, 핵심 하이퍼파라미터, seed 고정 | 수업 도우미 말투로 LoRA 학습하기 — `train_lora.py --inspect`로 마스킹 확인 후 `data/sample_sft.jsonl`로 학습, step별 loss 기록, `adapters/run-001/` 저장 | loss 로그(`outputs/train-run-001.json`), 어댑터 폴더 |
| 3교시 | 어댑터를 저장·비교·기록하기 — 어댑터 저장·로드·병합, 공정한 전후 비교 설계, 실험 기록 양식, 실패 기록, GGUF·Ollama 가져오기(확장) | 전후 비교와 실험 기록 run-001 — `compare.py`로 기본 vs 어댑터 출력 5개 나란히, `EXPERIMENT_TEMPLATE.md`로 `experiments/run-001.md` 작성 | 전후 비교표(`outputs/compare-run-001.md`), `experiments/run-001.md` |

각 블록은 설명·시연 20분, 실습 30분, 휴식 10분으로 운영한다. 분반 시간표에 따라 두 블록과 한 블록이 다른 날에 배치될 수 있으며, 블록 순서는 바꾸지 않는다.

## 준비물

- Git, VS Code, uv, PowerShell. GPU 실습은 NVIDIA GPU(기준 12 GB VRAM), GPU가 없으면 CPU 대체 경로(`--device cpu --max-steps 5`)를 쓴다.
- 수업 전 사전 캐시된 `HF_TEXT_MODEL`(기본값 `Qwen/Qwen2.5-0.5B-Instruct`). 실습 시간에 모델을 내려받지 않는다.
- 5주차 `SOURCES.md`와 9주차 팀 제안서(모델 후보·라이선스 표). 실험 기록의 「고정한 것」 표에 옮겨 적는다.
- 정확한 도구 버전은 [학기별 환경 기준표](../../../environment_baseline_template.md)에서 확정한다.
- 실제 이름, 학번, 비밀번호, Hugging Face 토큰은 실습 파일과 공개 저장소에 넣지 않는다. 토큰은 `.env`에만 두고 `.env.example`만 커밋한다. 학습 데이터에도 실제 인물·기관 정보를 넣지 않는다.

## 자료 안내

- [PT 원고](slides.md): 세 번의 20분 설명·시연용 Marp 자료
- [실습지](lab.md): 1·2·3교시 문제, 힌트, 검증, 확장
- [실행 예제](examples/README.md): `lora_lab/` uv 프로젝트 — LoRA 설정·학습·비교·병합 스크립트, 자체 작성 SFT 데이터, 실험 기록 양식
- [따라하기 절차](walkthrough.md): 시연·실습을 단계대로 재현하는 절차서
- 강의 대본: 강의자 별도 관리(비공개)

## 권장 진행 방식

1. 스크립트를 실행하기 전에 학습 파라미터 비율, loss 변화, 전후 출력 차이를 먼저 예상해 적는다.
2. 원본 `examples/lora_lab/`은 그대로 두고 개인 실습 폴더에 복사해 실행한다.
3. 매 실행의 `outputs/` 기록을 지우지 않고 run 이름을 바꿔 쌓는다. 실패한 실행도 기록에 남긴다.
4. 조건을 한 번에 하나만 바꾼다(rank, learning rate, epoch 중 하나).
5. 기본 문제를 마친 뒤에만 확장 문제(병합, rank 비교, 데이터 추가)를 수행한다.

## 완료 기준

- [ ] `lora_setup.py` 결과로 r=4·8·16의 학습 파라미터 비율표와 VRAM 예측표를 만들었다.
- [ ] `train_lora.py --inspect` 출력에서 프롬프트 구간이 가려지고 답변만 학습 대상으로 남는 것을 확인했다.
- [ ] `adapters/run-001/`에 `adapter_config.json`, `adapter_model.safetensors`, `run_config.json`이 있다.
- [ ] `outputs/train-run-001.json`의 loss가 처음보다 마지막에 낮고, 최대 VRAM 실측값을 1교시 예측과 비교했다.
- [ ] `compare.py`로 같은 프롬프트 5개의 기본 vs 어댑터 출력을 나란히 기록하고 형식 준수 수를 세었다.
- [ ] `experiments/run-001.md`의 「고정한 것」「설정」「결과」「샘플 출력」「관찰과 실패」「다음 실험」을 채웠다.
- [ ] 개인 저장소에 어댑터 가중치가 아니라 기록(`experiments/run-001.md`와 `outputs/` 기록 사본)만 커밋했다.

## 제출 증거

이번 주는 별도 제출물이 없다. 아래 증거를 개인 저장소에 누적한다.

1. `experiments/run-001/setup-*.md`: rank별 학습 파라미터 비율표와 VRAM 예측표(`outputs/`에서 복사)
2. `experiments/run-001/train-run-001.json`: 설정, loss 이력, 시간, 최대 VRAM(`outputs/`에서 복사)
3. `experiments/run-001/compare-run-001.md`: 프롬프트 5개의 전후 출력과 형식 준수 수(`outputs/`에서 복사)
4. `experiments/run-001.md`: 실험 기록(3차 종합과제의 첫 실험)
5. `git log --oneline -3`: 기록 파일만 커밋했음을 보이는 이력(실습 폴더의 `adapters/`·`models/`·`outputs/`는 `.gitignore`, 기록은 개인 저장소 `experiments/`로 복사해 커밋)

터미널 출력에는 사용자 홈 경로가 포함될 수 있다. 기록 전에 개인 식별 정보가 없는지 확인한다.

## 다음 주 연결

11주차 `week11_dataset_evaluation`에서 이번 주 학습 데이터(`sample_sft.jsonl`과 팀 데이터)를 정제·중복 제거·분할하고 개인정보를 점검한 뒤, 기본 모델과 LoRA 모델을 test split로 정량·정성 평가한다. 이번 주 `run-001.md`가 그 비교의 기준선이 되므로 seed, 모델 ID, 데이터 버전을 빠짐없이 적어 둔다.

## 참고 자료

- [PEFT 문서 — LoRA](https://huggingface.co/docs/peft/package_reference/lora)
- [Transformers 문서 — Trainer](https://huggingface.co/docs/transformers/main_classes/trainer)
- [Transformers 문서 — Chat Templates](https://huggingface.co/docs/transformers/chat_templating)
- [PyTorch 문서 — Automatic Mixed Precision](https://docs.pytorch.org/docs/stable/amp.html)
- [safetensors 문서](https://huggingface.co/docs/safetensors/)
- [Ollama 문서 — 모델 가져오기](https://docs.ollama.com/import)
