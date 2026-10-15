# 5주차 예제 — 교시별 폴더

이번 주는 Hugging Face의 공식 라이브러리를 **가져다 쓰는** 주다. Hub 조회는 `huggingface_hub`, 추론은 `transformers`의 `pipeline`, 데이터는 `datasets`가 맡는다. 예제 하나는 개념 하나이고 15~40줄이다.

| 교시 | 폴더 | 하는 일 | 명령 |
|---|---|---|---|
| 1교시 | [period1](period1/README.md) | Hub 정보·모델 카드 읽기, 캐시 보기 | `uv run ex01`, `ex02`, `ex03` |
| 2교시 | [period2](period2/README.md) | pipeline으로 분류·생성 | `uv run ex04`, `ex05` |
| 3교시 | [period3](period3/README.md) | 로컬·Hub 데이터셋 살펴보기 | `uv run ex06`, `ex07` |

양식: [모델 카드 분석표](model_cards_template.md)(1교시), [출처 기록표](SOURCES_template.md)(3교시).

## 공통 구조 — 배포 표준

- 교시 폴더 하나가 uv 프로젝트 하나다. `.python-version`(3.12), `pyproject.toml`, `src/`로 되어 있다.
- 예제 하나가 `src/exNN/__init__.py` 패키지 하나이고 `def main()`이 진입점이다. `pyproject.toml`의 `[project.scripts]`가 `exNN` 명령을 등록하고 `[build-system]`(`uv_build`)이 설치한다.
- 여러 예제가 함께 쓰는 설정·데이터는 `src/shared/` 공용 패키지에 두고 `from shared import ...`로 가져다 쓴다. 코드가 읽는 데이터 파일도 `src/shared/data/`에 둔다.
- 예제 폴더에서 `uv sync` 한 번, 그다음 `uv run exNN`으로 실행한다. 대화형 예제는 빈 줄을 건너뛰고 `/bye`로 끝난다.

## 수업 전 준비 (강의자·조교)

모델·데이터는 수업 전에 받아 둔다. 별도 스크립트 없이 `huggingface_hub`에 들어 있는 `hf` 명령을 쓴다.

```powershell
Set-Location period2
uv sync
uv run hf download Qwen/Qwen2.5-0.5B-Instruct
uv run hf download lxyuan/distilbert-base-multilingual-cased-sentiments-student
uv run hf cache ls
```

`hf download 모델 --revision <commit hash>`로 받으면 그 버전으로 고정된다. 캐시 위치를 바꾸려면 PowerShell에서 `$env:HF_HOME = "D:\hf-cache"`처럼 정한 뒤 받는다.
