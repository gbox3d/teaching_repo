# mock_exam — 공개 동형 모의 실기

1·2교시 모의 실기의 시작 자료다. 실제 실기 패킷이 아니며 정답은 들어 있지 않다. 상위 [examples/README.md](../README.md)에 실행 방법과 관찰 지점이 있다.

| 경로 | 쓰는 교시 | 내용 |
|---|---|---|
| `tasks_A.md` | 1교시 | 문제 A-1(프로젝트 복구), A-2(라이선스 3문항), A-3(Git 상황), `answers_A.md` 양식 |
| `make_broken_repo.ps1` | 1교시 | `broken_project/` 복사 + `.env` 커밋 이력 생성 |
| `broken_project/` | 1교시 | 복구 대상(원본에서 실행하지 않는다) |
| `tasks_B.md` | 2교시 | 문제 B-1(기능 추가), B-2(pipeline 해석 3문항), `answers_B.md` 양식 |
| `client_starter/` | 2·3교시 | 최소 Ollama 클라이언트 + `check_env.py` |
| `fixtures/pipeline_output.json` | 2교시 | 해석용 자체 작성 샘플 |

시간 배분과 완료 조건은 [lab.md](../../lab.md)를 따른다.
