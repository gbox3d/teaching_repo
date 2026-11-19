# Streamlit으로 로컬 AI 앱 만들기 · 3교시

[실습지](../../lab.md)의 3교시를 따른다. 실행은 `pyproject.toml`이 있는 프로젝트 루트에서 한다.

```powershell
uv run streamlit run src/ex03_rag/app.py
```

내 문서에 질문하는 앱을 실습하고 입력·결과·값을 바꾼 비교를 기록한다. 실습 30분 뒤 휴식 10분이다.

본문이 비거나 공백뿐이면 경고를 표시하고 assistant 기록에 넣지 않는다. 답변 본문이 없는 상황과, 본문은 있지만 문서의 근거와 맞지 않는 상황을 구분해 기록한다.
