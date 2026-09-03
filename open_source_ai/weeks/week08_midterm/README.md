# 8주차 — 수시평가와 2차 종합과제

## 이번 주 질문

> 1~7주의 내용을 혼자서 재현하고 설명할 수 있는가?

## 학습 목표

수업을 마치면 다음을 할 수 있다.

1. 실기평가 문제를 요구사항, 완료 조건, 검증 순서로 분해한다.
2. 깨진 uv 프로젝트를 오류 메시지 순서대로 복구하고 비밀 파일을 Git 추적에서 분리한다.
3. 라이선스·Git 상황 문제에 판단과 근거를 한 줄씩 붙여 답한다.
4. Ollama 클라이언트에 지정 기능을 추가하고 연결 실패와 모델 없음을 사람이 읽을 메시지로 구분한다.
5. pipeline 실행 결과의 label·score·device·경고 메시지를 근거를 들어 해석한다.
6. 2차 종합과제를 깨끗한 폴더에서 재현하고 제출 전 검사 목록을 통과한다.

## 누적 결과물

이번 주는 새 기능을 쌓는 주가 아니라 1~7주에 누적한 것을 혼자 재현하는 주다. 1·2교시의 공개 동형 모의 실기 A·B는 3교시 개인 실기평가의 연습이고, 5~7주 실습으로 만든 라이선스 분석표와 RAG 미니프로젝트는 **2차 종합과제**로 묶어 제출한다. 실기평가와 2차 과제에서 드러난 강점·약점은 9주차 팀 프로젝트 제안에서 역할을 나누는 근거가 된다.

## 수업 흐름

| 블록 | 설명·시연 20분 | 직접 해결 실습 30분 | 핵심 증거 |
|---|---|---|---|
| 1교시 | 실기평가 구조와 모의 문제 읽는 법 | 모의 실기 A 프로젝트 복구와 판별 문항 | 모의 A 완료 조건 체크, `answers_A.md`, 복구된 저장소의 `git ls-files` |
| 2교시 | 로컬 AI 실기 진단 포인트와 채점표 | 모의 실기 B 클라이언트 기능 추가와 결과 해석 | 모의 B 완료 조건 체크, `outputs/chat-*.json` 2개, `answers_B.md` |
| 3교시 | 실기평가 운영과 2차 과제 최종 점검 | 개인 실기평가와 대체 운영 | 제출 파일·commit id, `outputs/env-check.json`, 2차 과제 제출 전 검사 결과 |

각 블록은 설명·시연 20분, 실습 30분, 휴식 10분으로 운영한다. 분반 시간표에 따라 두 블록과 한 블록이 다른 날에 배치될 수 있으며, 블록 순서는 바꾸지 않는다. 3교시의 개인 실기평가는 기관 시간표에 따라 30분을 넘겨 확장될 수 있으며, 공개 자료에는 구조만 둔다.

## 준비물

- Git, VS Code, uv, Ollama, PowerShell. 1주차 `env_check.md`가 모두 통과한 PC.
- 사전 캐시된 기본 모델 `OLLAMA_MODEL`(교재 검증용 기본값 `qwen3:8b`, GPU 없는 PC는 `qwen3:0.6b`). 실습 중 모델을 내려받지 않는다.
- 4주차 1차 과제 저장소의 Ollama 클라이언트(예제 `ollama_client/`를 옮겨 넣은 `oss-tool`의 `chat`·`stream` 서브커맨드), 5주차 `model_cards.md`·`SOURCES.md`, 7주차 `mini_rag/`·`evalset.json`이 개인 저장소에 커밋되어 있다.
- 2주차 `license_matrix.md`와 `LICENSE`.
- 정확한 도구 버전은 [학기별 환경 기준표](../../../environment_baseline_template.md)에서 확정한다.
- 실제 이름, 학번, 전화번호, 비밀번호, 토큰은 실습 파일·답안·공개 저장소에 넣지 않는다. 표시 이름은 `student01`, 팀명은 `team-a` 같은 수업용 값을 쓴다.

## 자료 안내

- [PT 원고](slides.md): 세 번의 20분 설명·시연용 Marp 자료
- [실습지](lab.md): 1·2·3교시 문제, 힌트, 검증, 확장
- [실행 예제](examples/README.md): 공개 동형 모의 실기 starter(깨진 프로젝트, 클라이언트 시작 코드, 해석용 샘플), 2차 과제 제출 전 검사 스크립트
- 강의 대본: 강의자 별도 관리(비공개)
- [수시 실기평가 구조](exam_structure.md): 평가 범위, 권장 운영, 패킷 구성, 공정성 경계
- [수시 실기평가 채점표](exam_rubric.md): 100점 상대 배점과 수준별 판단
- [2차 종합과제 안내](assignment_brief.md): 목적, 필수 산출물, 제출 형식, 제출 전 검사
- [2차 종합과제 채점표](assignment_rubric.md): 100점 상대 배점과 감점 원칙

## 권장 진행 방식

1. 모의 실기는 타이머를 켜고 30분을 지킨다. 못 끝낸 항목은 증상·관찰·시도를 적고 넘어간다.
2. 코드를 만지기 전에 요구사항을 완료 조건 체크 항목으로 옮기고 검증 명령을 정한다.
3. 오류는 첫 줄부터 읽고 한 번에 한 곳만 고친 뒤 다시 실행한다.
4. 판별 문항은 "판단 + 근거 + 출처" 세 줄 이내로 답한다. 빈칸 대신 "확인할 문서"를 적는다.
5. 2차 과제는 새 폴더에 clone해 README의 명령만으로 재현한 뒤 제출한다.

## 완료 기준

- [ ] 모의 A의 `uv run python report.py`가 `outputs/report.json`을 만들고 `git ls-files`에 `.env`가 없다.
- [ ] 모의 A의 라이선스 3문항·Git 1문항에 판단과 근거를 적었다.
- [ ] 모의 B의 `--system` 옵션이 동작하고 `outputs/chat-*.json`에 `tokens_per_sec`가 기록된다.
- [ ] 모의 B에서 연결 실패와 모델 없음이 서로 다른 메시지로 처리된다.
- [ ] pipeline 결과 해석 3문항에 판단과 근거를 적었다.
- [ ] 개인 실기(또는 대체 운영)에서 시작 전 `outputs/env-check.json`을 만들고 `git status`가 clean인 상태로 시작했다.
- [ ] 제출 파일과 commit id를 기록하고 제출물을 다시 열어 확인했다.
- [ ] 2차 종합과제를 깨끗한 폴더에서 README만으로 재현했다.

## 제출 증거

1. 2차 종합과제: 저장소 URL + 최종 commit id + README 재현 절차([assignment_brief.md](assignment_brief.md) 기준). 배점·마감은 학교 운영 문서가 정한다.
2. 개인 실기평가: 비공개 패킷이 지정한 파일 + 마지막 commit id + 짧은 설명(무엇을·왜). 제출 경로는 시험 공지를 따른다.
3. 개인 저장소에 누적: `answers_A.md`, `answers_B.md`, 모의 A 복구 저장소, 모의 B `outputs/chat-*.json` 2개.

터미널 출력에는 사용자 홈 경로가 포함될 수 있다. 제출 전에 개인 식별 정보가 없는지 확인한다.

## 다음 주 연결

9주차 `week09_project_governance`에서는 2~3인 팀을 꾸려 오픈소스 AI 프로젝트 제안서를 쓰고 팀 저장소를 만든다. 이번 주 실기와 2차 과제에서 확인한 각자의 강점(재현성·API·라이선스 분석·평가)을 팀 역할 분담의 근거로 가져간다. 다음 수업 전에 GitHub 계정과 2차 과제 저장소가 팀원에게 보이는지 확인한다.

## 참고 자료

- [Git `rm` 공식 문서](https://git-scm.com/docs/git-rm)
- [GitHub Docs — 저장소에서 민감한 데이터 제거](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository)
- [uv 프로젝트 개념](https://docs.astral.sh/uv/concepts/projects/)
- [Ollama API 레퍼런스](https://github.com/ollama/ollama/blob/main/docs/api.md)
- [Transformers pipelines 문서](https://huggingface.co/docs/transformers/main_classes/pipelines)
- [SPDX 라이선스 목록](https://spdx.org/licenses/)
