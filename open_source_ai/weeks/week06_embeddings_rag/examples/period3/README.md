# 6주차 3교시 — 평가셋으로 검색·답변 점검하기

1교시와 같은 **프로젝트 루트**에서 계속한다. `outputs/index.*`와 `outputs/index-150.*`를 다시 복사하거나 생성할 필요가 없다.

[ex05_eval](../src/ex05_eval/__init__.py)은 루트 [evalset.json](../evalset.json)의 질문을 공용 검색 함수에 보낸다. `--generate`를 지정하면 2교시와 같은 답변 함수를 사용한다.

```powershell
uv run ex05 --top-k 3
uv run ex05 --top-k 1
uv run ex05 --index outputs/index-150 --top-k 3
uv run ex05 --ids q05,q10 --generate
```

앞의 세 명령은 검색만 평가한다. 마지막 명령은 Ollama로 두 문항의 답을 생성해 키워드·출처 일치도 확인한다. 결과는 `outputs/eval-*.json`과 `outputs/eval-*.md`에 저장한다.

실패한 질문을 직접 다시 확인하려면 `uv run ex03 --top-k 5`로 질문을 입력한다. 한 조건만 바꾸어 비교하고 원인과 관찰 결과를 `eval_note.md`에 기록한다.

실습 문제·시간표·완료 조건은 [3교시 실습지](../../lab.md#3교시-실습--평가셋으로-품질-재기와-실패-분석)를 따른다.
