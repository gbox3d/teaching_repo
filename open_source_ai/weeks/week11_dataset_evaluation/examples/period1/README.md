# 11주차 1교시 · Needle 도구 호출

[실습지](../../lab.md)의 1교시를 따른다. 설명·시연 20분 뒤 실습 30분, 휴식 10분이다. 실행 위치는 이 폴더의 상위 `examples/`다. 교시마다 프로젝트나 자료를 복사하지 않는다.

읽을 코드: [ex01_needle](../src/ex01_needle/__init__.py) · [shared](../src/shared/__init__.py)

```powershell
uv run ex01
```

`complete()`의 `function_calls`를 Python에서 검증한다. `run()`으로 자동 실행하지 않는다. 문항마다 `reset()`한다.

시뮬레이터는 별도 터미널에서 켜 둔다. 입력의 기대 결과를 먼저 적고 실행한 뒤 TCP 연결을 유지한 상태에서 `GET /state`로 확인한다. 변경할 값은 소스의 상수에서 찾는다. 상세 시간표와 기록 항목은 실습지에 있다.
