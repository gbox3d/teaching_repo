# 3교시 — 로컬·Hub 데이터셋 살펴보기

`datasets`의 `load_dataset`은 내 파일과 Hub 데이터셋을 같은 방법으로 연다. 카드는 `huggingface_hub`의 `DatasetCard`로 읽는다.

```powershell
uv sync
uv run ex06
```

| 명령 | 배우는 것 | 해 보기 |
|---|---|---|
| `uv run ex06` | `load_dataset("json", data_files=...)`로 필드·건수·자료형 보기, `filter`로 찾기 | `찾기>`에 `uv`, `라이선스` 입력 |
| `uv run ex07` | `streaming=True`로 앞 3행만 받기, `DatasetCard`의 license | 빈 줄(`klue/klue ynat`), `klue/klue`(구성 빠짐), `HuggingFaceH4/no_robots` 입력 |

## 공용 패키지와 데이터 — `src/shared/`

```text
src/shared/__init__.py        데이터 경로·Hub 데이터셋 ID
src/shared/data/sample_qa.jsonl   수업용 Q&A 12건
src/shared/data/README.md         그 데이터의 Dataset Card
```

코드가 읽는 데이터는 코드와 함께 패키지 안에 둔다. `Path(__file__).parent / "data"`는 "이 코드 파일이 있는 폴더의 data"라서 어느 폴더에서 실행해도 같은 파일을 찾는다.

## 안 될 때

- `오류: Config name is missing. Please pick one among ...`: 구성이 여러 개인 데이터셋이다. 목록의 이름 하나를 띄어 쓴다(예: `klue/klue ynat`).
- `오류: 401 Client Error`: 없는 데이터셋 ID다(비공개일 수 있어 401로 답한다).
- `ex07`은 네트워크가 필요하다. 막혀 있으면 `ex06`과 카드 읽기만 한다.
