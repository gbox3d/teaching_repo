# 7주차 2교시 — 출처 있는 답 생성과 거부 경로

**역할: 2교시 출처 있는 답 생성 참조 구현과 인덱스 재생성 코드.** [실습지의 2교시](../../lab.md#2교시-실습--출처-있는-답-생성과-거부-경로)를 순서대로 진행할 때 여는 폴더다. 완성된 답안 문서를 제공하지 않으며 측정값·비교·판정은 직접 기록한다.

이 폴더는 다른 `period`나 통합 예제 폴더를 import하지 않는 독립 uv 프로젝트다. 앞 교시에 필요한 공개 코드는 중복 포함하고, 뒤 교시에 처음 쓰는 실행 파일은 넣지 않았다.

## 실습 단계와 파일 대응

| 실습지 단계 | 이번에 여는 파일 | 남기는 증거 |
|---|---|---|
| 준비, 독립 인덱스 재생성 | `docs/`, `chunk.py`, `embed.py`, `ragcore.py` | 이 폴더의 `outputs/index.*` |
| 문제 1, 출처·프롬프트·메타 | `rag_answer.py`, `search.py` | 정상 `outputs/rag-*.json` 2건 |
| 문제 2, 거부·검색 없음·num_ctx | `rag_answer.py`의 비교 옵션 | `rag_note.md`·거부/경계 JSON |

`pyproject.toml`은 이 교시까지의 의존성, `.gitignore`는 환경·캐시·비밀·산출물 제외 규칙이다. 설정을 읽는 교시는 `.env.example`도 포함한다. 전체 파일은 이 폴더에서 확인한다.

## 실행 위치와 수업 전 준비

새 복사본을 만들 때만 복사한다. 이미 진행 중인 폴더·기록을 템플릿으로 덮어쓰지 않는다.

```powershell
$src = "<교재 저장소>\open_source_ai\weeks\week07_embeddings_rag\examples"
$dst = "$HOME\osa-practice\week07"
New-Item -ItemType Directory -Force $dst | Out-Null
if (-not (Test-Path "$dst\period2")) { Copy-Item -Recurse "$src\period2" "$dst\period2" }
Set-Location "$dst\period2"
if (-not (Test-Path .env)) { Copy-Item .env.example .env }
uv sync                    # 수업 전에 설치·캐시한다
```

이 교시 폴더만 복사해도 시작할 수 있다. 실습 30분을 시작하기 전에 아래 준비 명령으로 **이 폴더의** 인덱스를 만든다. 앞 교시의 `outputs/`를 가져오거나 다른 폴더를 import하지 않는다. 문서를 수정했다면 그 내용을 이 폴더의 `docs/`에도 반영한 뒤 다시 만든다.

```powershell
uv run python chunk.py --size 300 --overlap 50
uv run python embed.py --chunks outputs/chunks-300.json
```

Python 명령은 현재 `period2` 폴더에서 `uv run`으로 실행한다. activate는 필요 없다. 현재 교재에는 기준 PC에서 확정한 lock이 없으므로 첫 `uv sync`가 lock을 만든다. 검증·커밋된 lock을 배포받은 경우에만 `uv sync --locked`, `uv run --locked ...`로 재현을 확인한다. 설치·업데이트는 [공통 uv 가이드](../../../../uv_guide.md)를 따른다.

## 설명·시연 20분

[이 주차 슬라이드](../../slides.md)의 2교시 구간과 같다.

| 시간 | 설명·시연 |
|---|---|
| 0–3분 | 이어받는 것: 검색 결과는 답이 아니다 |
| 3–6분 | 프롬프트 구조: system · context · question |
| 6–9분 | 출처 표시: 파일명#번호 |
| 9–12분 | 컨텍스트 길이: num_ctx와 top-k |
| 12–15분 | "자료에 없으면 찾을 수 없다"와 인젝션 |
| 15–17분 | 시연: 정상 · 거부 · 비교 |
| 17–20분 | 실습 인계 |

## 직접 해결 실습 30분

다음 표는 [실습지](../../lab.md#2교시-실습--출처-있는-답-생성과-거부-경로)의 시간 배분을 그대로 따른다. 이후 휴식 10분이다.

| 단계 | 시간 | 활동 |
|---|---:|---|
| 문제·예상 | 0–5분 | 서버·모델 확인, 질의 2개의 인용 청크와 자료 밖 질문의 결과 예상 |
| 출처 있는 답 | 5–13분 | `rag_answer.py` 질의 A·B, `cited`·`cited_in_retrieved` 확인, `--show-prompt` |
| 거부·비교 | 13–21분 | 자료 밖 질문 → `refused` 확인, `--no-context`와 비교 |
| num_ctx 경계 | 21–25분 | `--num-ctx 256`으로 `prompt_eval_count`와 답 변화 관찰 |
| 검증·기록 | 25–30분 | `rag_note.md` 완성, `outputs/rag-*.json` 3건 확인 |

## 실습에서 실행할 명령

아래는 실행 순서의 핵심 명령이다. 전체 질문·반복 조건·실패 기록·완료 조건은 실습지 문제 1·2를 따른다.

```powershell
uv run python rag_answer.py --query "uv.lock은 왜 커밋하는가" --top-k 3
uv run python rag_answer.py --query "Apache-2.0 라이선스가 MIT와 다른 점은?" --top-k 3
uv run python rag_answer.py --query "uv.lock은 왜 커밋하는가" --show-prompt
uv run python rag_answer.py --query "LoRA의 rank는 무엇인가" --top-k 3
uv run python rag_answer.py --query "LoRA의 rank는 무엇인가" --no-context
uv run python rag_answer.py --query "uv.lock은 왜 커밋하는가" --top-k 3 --num-ctx 256
```

## 예상 결과와 완료 확인

두 정상 답의 cited·cited_in_retrieved, 자료 밖 질문의 refused, 검색 제거·컨텍스트 축소 결과를 남긴다. 거부·출처 규칙을 지키지 않은 경우도 실제 관찰로 기록한다.

`outputs/`는 각 교시 폴더 안에 생성된다. 비교 기록 문서는 실습지처럼 주차 실습 폴더(현재 폴더의 상위)에 작성한다. 필요한 증거만 `evidence/`에 골라 옮기고 `.env`, `.venv/`, 모델 캐시와 `outputs/` 전체를 Git에 넣지 않는다.

## 바꿔 보기

실습지 문제 2대로 `--no-context`와 `--num-ctx 256`을 각각 비교한다. top-k 변경과 프롬프트 인젝션은 기본 실습 후 확장 문제로 진행한다.

## CPU·네트워크 대체 경로

임베딩은 CPU 또는 로컬 Ollama 백엔드로 가능하다. 생성은 켜진 로컬 Ollama와 캐시된 소형 모델(`OLLAMA_MODEL=qwen3:0.6b`)로 진행한다. 네트워크가 없으면 캐시만 사용한다. 모델이 없으면 다운로드 대신 준비 상태를 확인한다.
