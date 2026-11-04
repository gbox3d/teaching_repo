# 6주차 1교시 — 임베딩과 신화 검색

[실습지](../../lab.md)의 1교시를 따른다. 실행 위치는 이 폴더가 아니라 복사한 `examples` 프로젝트 루트다.

읽을 코드: [ex01_embed](../src/ex01_embed/__init__.py) · [ex02_search](../src/ex02_search/__init__.py) · [shared](../src/shared/__init__.py) · 자료 [myths.md](../src/shared/data/myths.md)

```powershell
uv run ex01
uv run ex02
```

`ex01`은 문장 하나가 숫자 1024개가 되는 것을 보여 주고, 입력한 문장과 기준 문장 다섯 개의 유사도를 큰 순서로 출력한다. `ex02`는 신화 50편을 벡터로 저장한 뒤 질문과 가까운 글 `TOP_K`편을 점수와 함께 보여 준다. 빈 줄은 건너뛰고 `/bye`로 종료한다. 예상 → 실행 → 값 하나 수정 → 비교 → 기록 순서로 진행하며 실습 시간은 30분이다. 세부 시간표·입력 예시·완료 기준은 실습지에 있다.
