# 12주차 2교시 — 스트리밍 채팅 UI

[해당 실습 단계·문제·완료 조건](../../lab.md#2교시-실습--스트리밍-채팅-ui-연결) · [교시별 색인](../README.md)

1교시 API에 SSE와 Gradio UI를 추가한 **누적 참조 구현**이다. 1교시 학생 과제 GET /models의 답은 포함하지 않았다. 개인 1교시 구현은 실습지 전환 절에 따라 옮긴다. Docker는 3교시 자료다.

## 시간별 파일 대응

| 실습 시간 | 단계 | 이 폴더의 파일·경로 | 확인할 증거 |
|---|---|---|---|
| 0–4분 | 시간 예상 | `app/main.py`, `ui/gradio_app.py` | 첫 글자·전체 시간 예상 |
| 4–10분 | SSE 원문 | `smoke_test.py --show-events` | delta·done, first_chunk_ms·total_ms |
| 10–18분 | UI 두 모드 | `ui/gradio_app.py` | once/stream 비교표 |
| 18–25분 | Stop·오류 | `ui/gradio_app.py`의 `ERROR_HINTS` | 중단·연결 실패·502 문구 |
| 25–30분 | 검증·기록 | `outputs/ui-turns.jsonl` | 시간 및 error:true 2건 |

파일명이 짧게 적힌 경우 바로 앞 열의 같은 하위 폴더를 기준으로 읽는다. 시간과 완료 조건은 연결된 실습지를 따른다.

## 실행 위치와 명령

이 `period2/` 폴더를 개인 실습 공간에 **처음 한 번 폴더째** 복사하고 그 안에서 실행한다. 숨김 파일도 포함한다. 이미 개인 교시 폴더가 있으면 다시 복사하지 않고 이어 한다. `.env`와 작성한 기록도 새 양식으로 덮어쓰지 않는다. 실제 준비 명령은 위 실습지 링크를 따른다. Python 명령은 `pyproject.toml` 옆에서 실행한다. `uv.lock`·`.venv/`는 배포하지 않았으므로 최초 `uv sync`로 개인 환경을 만든다.

```powershell
uv sync
uv run uvicorn app.main:app --port 8000 --reload
# 다른 터미널도 이 폴더에서
uv run python smoke_test.py --show-events --max-tokens 300
uv run python ui/gradio_app.py --no-stream
# UI를 Ctrl+C로 종료한 뒤
uv run python ui/gradio_app.py
```

## 기본 실행과 실습 후 검증

API는 8000, UI는 7860에서 열린다. SSE에 delta·done 이벤트가 보이고, 두 UI 모드의 first_ms·total_ms가 outputs/ui-turns.jsonl에 기록된다. ERROR_HINTS는 실습 문제 2에서 자기 팀 사용자에 맞게 고친다.

## 이전 산출물과 다음 단계

1교시의 실패 예상표·outputs와 직접 만든 GET /models를 이어받는다. 이전 서버는 Ctrl+C로 종료하고 이 교시 폴더에서 새로 실행한다.

## 대체 경로

모델이 없으면 다운로드하지 않고 앱 서버 중단·없는 Ollama 포트의 UI 오류를 기록한다. 정상 스트리밍 비교는 캐시 모델이 있는 PC에서 마무리한다.
