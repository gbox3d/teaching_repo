# 14주차 1교시: 소개 자료 검색과 대화

실행 위치는 이 폴더가 아니라 `examples/` 루트다. [공통 준비](../README.md#설치와-프로젝트-구조)에 따라 한 번 설치한 환경과 자료를 세 교시 동안 이어 쓴다.

읽을 파일은 [student_bot](../src/student_bot/__init__.py), [공용 대화 함수](../src/shared/__init__.py), [소개 자료](../src/shared/data/corpus.json)다. 학생 수정 파일은 `student_bot` 하나다.

```powershell
uv sync
uv run ex01
```

소개 자료에 있는 위치·상징물 질문을 입력한 뒤 자료에 없는 오늘 식단도 질문한다. 반환된 `answers`, `sources`, `abstain`을 읽고 문서의 ID와 대조한다. 빈 입력은 건너뛰며 `/bye` 또는 Ctrl+C로 종료한다. 이전 대화는 다음 요청에 포함되지 않는다.

30분 실습에서는 자료와 예상 답 확인, 두 질문 실행, 검색된 문서 확인, 설정값이나 프롬프트 한 부분 수정, 응답 비교 순서로 진행한다. `MODEL`, `OLLAMA_URL`, `TOP_K`는 파일 위쪽에 있다. 새 프로젝트 구조를 연습할 때는 별도 빈 위치에서 `uv init --package --python 3.12 --vcs none wku-bot`을 실행한다. 상세 활동과 제출 기준은 [실습지](../../lab.md)를 따른다.
