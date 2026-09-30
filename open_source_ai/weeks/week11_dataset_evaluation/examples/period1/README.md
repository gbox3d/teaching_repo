# 11주차 1교시 — 원시 데이터를 정제·마스킹·분할하기

[실습지 1교시](../../lab.md#1교시-실습--원시-데이터를-정제마스킹분할하기)에 대응하는 **누적 참조 구현**이다. 이전 교시 코드·입력은 이 폴더에 실제로 들어 있고, 이후 교시 실행 파일은 아직 없다. 모델·개인 실행 결과·어댑터는 포함하지 않는다.

## 시간과 파일 대응

| 시간 | 실습 단계 | 읽거나 실행할 파일 |
|---|---|---|
| 0–5분 | 원시 데이터·건수 예상 | `data/raw.jsonl` |
| 5–12분 | 정제·중복 임계값 | `clean.py` |
| 12–18분 | 개인정보 검출·마스킹 | `pii_check.py` |
| 18–24분 | split·seed·학습 데이터 겹침 | `split.py`, `data/week10_sample_sft.jsonl` |
| 24–30분 | 데이터 카드 7절 | `DATA_CARD_TEMPLATE.md` |

## 이전 산출물과 실행 위치

교재의 이 폴더 전체를 개인 `C:\classwork\week11\period1`에 복사한다. 다른 period의 가상환경을 복사하지 않고 이 폴더에서 `uv sync`한다. 패키지·모델은 수업 전에 준비한다.

10주차 학습 데이터를 이어받는다. 개인 학습본이 없을 때 실습지가 허용한 교재 데이터의 실제 사본을 `data/week10_sample_sft.jsonl`로 넣었다. 이 교시는 모델을 실행하지 않으며 의존성은 분할용 `datasets`다.

## 실행 순서

복사·`.env` 생성·이전 산출물 전달은 **새 실습 폴더에서 최초 1회만** 한다. 이미 작업 중이면 이 명령들을 생략하고 실행 위치 확인부터 이어간다. 기존 개인 코드·설정·결과를 덮어쓰지 않는다. 새 period의 누적 코드와 개인 변경은 비교하여 필요한 수정만 옮긴다.

```powershell
Set-Location C:\classwork\week11\period1
uv sync
uv run python clean.py
uv run python pii_check.py --action report
uv run python pii_check.py
uv run python split.py
uv run python split.py --seed 7 --out-dir outputs/split_seed7 --report outputs/split_report_seed7.json
uv run python split.py --against data/week10_sample_sft.jsonl
if (-not (Test-Path DATA_CARD.md)) { Copy-Item DATA_CARD_TEMPLATE.md DATA_CARD.md }
```

## 예상 출력과 완료 확인

기본 조건은 원시 48→정제 44건, PII 3건, train 20/val 4/test 20, leak_count 0이다. 조건을 바꾸면 자신의 출력으로 기록한다. `DATA_CARD.md`와 세 보고서를 다음 교시로 넘긴다.

## 대체 경로

GPU·모델·어댑터 없이 진행한다. 캐시된 패키지는 `uv sync --offline`으로 준비한다. 데이터 식별정보는 가짜 예시이며 실제 팀 데이터의 개인정보는 삭제한다.

옵션별 변형·실패 경로·확장은 실습지를 따른다. 모델 ID·revision·장치·조건을 기록하고 실행하지 않은 수치를 만들지 않는다. `.venv/`·`.env`·`outputs/`·가중치는 제외하고, 검증한 기록을 증거 폴더에 골라 보관한다. 현재 원본에는 lock이 없으며 학기 기준 확정 후 기준 PC에서 생성·검증해 배포한다.
