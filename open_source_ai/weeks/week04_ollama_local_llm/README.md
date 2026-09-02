# 4주차 — Ollama와 로컬 LLM

## 이번 주 질문

> 내 PC의 GPU에서 언어 모델이 실제로 어떻게 실행되고, 내 프로그램은 그것과 어떻게 대화하는가?

## 학습 목표

수업을 마치면 다음을 할 수 있다.

1. 가중치·토크나이저·컨텍스트로 이루어진 LLM 실행 구조를 설명하고, 파라미터 수와 양자화 단계로 VRAM 사용량을 어림한다.
2. `ollama list/show/run/ps`로 캐시된 모델의 파라미터 수, 양자화, 컨텍스트 길이, 메모리 사용량, tokens/s를 실측해 기록한다.
3. `/api/chat`을 비스트리밍과 스트리밍(NDJSON)으로 호출하고 `eval_count`·`eval_duration` 같은 응답 메타를 읽는다.
4. `temperature`·`num_ctx`·`num_predict`·`seed` 옵션과 `think` 옵션이 답에 미치는 영향을 같은 프롬프트로 비교한다.
5. 연결 실패와 모델 없음을 사람이 읽을 메시지와 0이 아닌 종료 코드로 처리한다.
6. Modelfile로 시스템 프롬프트가 들어간 커스텀 모델을 만들고 변경 전후를 같은 질문으로 비교한다.

## 누적 결과물

이번 주는 1장(1~4주)을 마무리하는 **1차 종합과제** 주차다. 2주차의 협업 저장소와 3주차의 uv 프로젝트·설정 로더 위에, 이번 주의 Ollama 클라이언트(`chat`·`stream`), 모델 비교 보고서(`model_report.md`), 커스텀 모델 `Modelfile`이 얹혀 1차 과제 저장소가 완성된다. 예제의 `chat.py`·`stream.py`는 참조 구현이며, 과제에서는 3주차 `oss-tool` CLI의 `chat`·`stream` 서브커맨드로 옮겨 넣는다. 5~7주차의 RAG 답변기는 이 클라이언트를 그대로 재사용한다.

## 수업 흐름

| 블록 | 설명·시연 20분 | 직접 해결 실습 30분 | 핵심 증거 |
|---|---|---|---|
| 1교시 | 모델은 어떻게 실행되는가 — 가중치·토크나이저·컨텍스트, 양자화(FP16→Q4)와 용량·품질 트레이드오프, 파라미터 수→VRAM 계산, Ollama 구조(서버·CLI·라이브러리·Modelfile)와 캐시 위치 | 모델 두 개를 실행하고 측정하기 — `ollama run`·`/set verbose`·`ollama show`·`ollama ps`로 기본 모델과 소형 모델을 실측하고 같은 질문 3개의 답 차이를 기록 | `model_report.md`(모델 2개: 파라미터·양자화·파일 크기·메모리·tokens/s·답 차이) |
| 2교시 | REST API로 대화하기 — `/api/generate`와 `/api/chat`의 차이, 메시지 역할, 스트리밍(NDJSON)과 비스트리밍, options(`temperature`·`num_ctx`·`num_predict`), 응답 메타, `think` 옵션, 오류 처리 | REST API로 대화하고 실패를 다루기 — `chat.py`·`stream.py` 실행과 메타 읽기, 연결 실패·모델 없음 재현, `--seed` 추가 후 temperature 0과 1 비교 | `outputs/chat-*.json`·`outputs/stream-*.json`, 실패 메시지 2건, 비교 문단 |
| 3교시 | Modelfile과 시스템 프롬프트, 1차 종합과제 — FROM·SYSTEM·PARAMETER·TEMPLATE, `ollama create`, 시스템 프롬프트 설계, 프롬프트와 파인튜닝의 경계, 1차 과제 안내 | 수업 도우미 모델 만들기와 과제 점검 — Modelfile로 커스텀 모델 생성, `chat.py --model`로 전후 비교, SYSTEM 한 줄 변경 후 재비교, 과제 체크리스트 점검 | `ollama list` 출력, 전후 비교표, 과제 체크리스트 점검 결과 |

각 블록은 설명·시연 20분, 실습 30분, 휴식 10분으로 운영한다. 분반 시간표에 따라 두 블록과 한 블록이 다른 날에 배치될 수 있으며, 블록 순서는 바꾸지 않는다.

## 준비물

- Ollama가 설치되어 있고 서버가 켜져 있다(`ollama list`가 오류 없이 출력된다).
- 기본 생성 모델과 CPU 대체 소형 모델이 **수업 전에 캐시**되어 있다. 교재 검증용 기본값은 `qwen3:4b`와 `qwen3:0.6b`이며, 실습 중 `ollama pull`을 실행하지 않는다.
- uv, Git, VS Code, PowerShell. 예제의 의존성(`httpx`, `python-dotenv`)은 수업 전 `uv sync`로 한 번 받아 둔다.
- 3주차에서 만든 개인 저장소의 `oss_tool` 프로젝트와 `config.py`(`OLLAMA_HOST`·`OLLAMA_MODEL` 기본값).
- 1주차 `env_check.md`의 GPU 이름·VRAM 값(보고서에 옮겨 적는다).
- 정확한 도구 버전, 모델 ID·양자화·용량은 [학기별 환경 기준표](../../../environment_baseline_template.md)에서 확정한다.
- 실제 토큰, 비밀번호, 개인정보를 `.env`·산출물·공개 저장소에 넣지 않는다. 표시 이름은 `student01`, 팀명은 `team-a` 같은 수업용 값을 쓴다.

## 자료 안내

- [PT 원고](slides.md): 세 번의 20분 설명·시연용 Marp 자료
- [실습지](lab.md): 1·2·3교시 문제, 힌트, 검증, 확장
- [실행 예제](examples/README.md): `ollama_client/` uv 프로젝트(`config.py`·`chat.py`·`stream.py`·`Modelfile`), 모델 보고서 양식, 측정 기록 스크립트
- [따라하기 절차](walkthrough.md): 시연·실습을 단계대로 재현하는 절차서
- 강의 대본: 강의자 별도 관리(비공개)
- [1차 종합과제 안내](assignment_brief.md) · [1차 종합과제 루브릭](assignment_rubric.md)

## 권장 진행 방식

1. 실습 문제의 완료 조건을 먼저 읽고, 명령을 실행하기 전에 숫자(파일 크기·메모리·tokens/s)와 메시지를 예상해 적는다.
2. 모든 측정은 같은 질문 3개로 한다. 질문을 바꾸면 비교가 아니다.
3. 예제는 원본을 두고 개인 실습 폴더에 복사해 변형한다. 실패 경로(서버 없음·모델 없음)는 반드시 한 번씩 재현한다.
4. 응답 메타는 화면 값을 믿지 말고 JSON에서 직접 찾아 손으로 계산해 본다.
5. 3교시가 끝나면 1차 과제 체크리스트에서 비어 있는 항목을 적고, 다음 수업 전까지 채울 계획을 정한다.

## 완료 기준

- [ ] `ollama show`·`ollama list`에서 기본 모델의 파라미터 수, 양자화, 컨텍스트 길이, 파일 크기를 옮겨 적었다.
- [ ] `/set verbose`의 eval rate와 `ollama ps`의 SIZE·PROCESSOR를 모델 2개에 대해 기록했다.
- [ ] 같은 질문 3개에 대한 두 모델의 답 차이를 `model_report.md`에 한 문장씩 적었다.
- [ ] `chat.py`가 남긴 JSON에서 `eval_count`·`eval_duration`으로 tokens/s를 직접 계산해 화면 값과 비교했다.
- [ ] `stream.py`에서 첫 조각까지의 시간과 조각 수를 기록하고, 메타가 마지막 줄에만 있음을 확인했다.
- [ ] 연결 실패·모델 없음 두 경우에 사람이 읽을 메시지와 0이 아닌 종료 코드를 확인했다.
- [ ] `--seed`를 추가한 뒤 temperature 0과 1의 답 차이를 한 문단으로 적었다.
- [ ] 커스텀 모델을 `ollama create`로 만들고 기준 모델·커스텀·SYSTEM 변경 후 답을 비교표로 남겼다.

## 제출 증거

이번 주는 1차 종합과제 주차다. 아래 증거를 개인 저장소에 누적하고, 과제 제출은 [1차 종합과제 안내](assignment_brief.md)를 따른다.

1. `model_report.md`(모델 2개 비교 + 커스텀 모델 전후 비교표)
2. `evidence/`에 복사한 `outputs/chat-*.json`·`outputs/stream-*.json` 2~3개
3. 연결 실패·모델 없음 메시지와 종료 코드를 적은 텍스트
4. temperature 0과 1 비교 문단(seed 값 포함)
5. `Modelfile`과 `ollama list` 출력
6. 1차 과제 체크리스트 점검 결과(비어 있는 항목과 계획)

터미널 출력에는 사용자 홈 경로가 포함될 수 있다. 제출 전에 개인 식별 정보와 토큰이 없는지 확인한다.

## 다음 주 연결

5주차 `week05_huggingface_hub`에서는 Ollama 라이브러리 밖의 Hugging Face Hub에서 모델과 데이터를 찾고, 모델 카드와 라이선스를 읽어 "정말 내 프로젝트에 쓸 수 있는 것인지"를 판단한다. 이번 주의 `OLLAMA_MODEL`처럼 모델 ID를 환경변수로 관리하는 습관이 `HF_TEXT_MODEL`·`HF_EMBED_MODEL`로 이어진다. 1차 종합과제는 안내서의 제출 형식대로 저장소 URL과 최종 commit id를 준비한다.

## 참고 자료

- [Ollama 공식 문서](https://docs.ollama.com/)
- [Ollama API 레퍼런스](https://github.com/ollama/ollama/blob/main/docs/api.md)
- [Ollama Modelfile 문서](https://github.com/ollama/ollama/blob/main/docs/modelfile.md)
- [uv 공식 문서](https://docs.astral.sh/uv/)
- [GitHub Docs — Pull requests](https://docs.github.com/en/pull-requests)
