# 7주차 — 임베딩·검색·RAG 응용

## 이번 주 질문

> 모델이 모르는 내 문서를 근거로, 출처를 밝히며 답하게 하려면 무엇을 검색하고 무엇을 넣어야 하는가?

## 학습 목표

수업을 마치면 다음을 할 수 있다.

1. 문서를 chunk 크기·겹침·문장 경계 기준으로 분할하고, chunk 크기가 검색 결과에 미치는 영향을 관찰 결과로 설명한다.
2. sentence-transformers 또는 Ollama `/api/embed`로 청크를 임베딩해 numpy 인덱스를 만들고 코사인 유사도 top-k 검색을 수행한다.
3. 검색 결과를 system·context·question 구조의 프롬프트로 조립해 Ollama `/api/chat`으로 출처(`파일명#번호`)가 붙은 답을 생성한다.
4. 컨텍스트에 없는 질문에 "찾을 수 없다"로 답하는 경로와 `num_ctx`·top-k의 한계를 확인하고, 프롬프트 인젝션 위험을 설명한다.
5. 10문항 평가셋으로 retrieval hit rate와 출처 일치율을 측정하고 실패 사례의 원인을 chunk 경계·용어 불일치·top-k 부족으로 분류한다.
6. 2차 종합과제의 RAG 미니프로젝트 요건을 자기 저장소 기준으로 점검한다.

## 누적 결과물

이번 주 `mini_rag/` 파이프라인(chunk → embed → search → answer → eval)은 **2차 종합과제(8주차)** 의 RAG 미니프로젝트 골격이다. 과제에서는 문서를 자기 문서 10개 이상으로 바꾸고, 평가셋 10문항과 hit rate·실패 분석 2건을 붙여 제출한다. 6주차 임베딩·유사도 계산과 4주차 Ollama 클라이언트 패턴(환경변수 기본값, `think:false`, `outputs/` 기록)이 그대로 이어지며, 12주차 서비스화(3차 종합과제)의 교재 예제는 기본 모델만 호출하므로, 팀 프로젝트가 문서 검색을 쓰기로 했다면 이 파이프라인을 FastAPI `/chat` 뒤에 직접 붙여야 한다.

## 수업 흐름

| 블록 | 설명·시연 20분 | 직접 해결 실습 30분 | 핵심 증거 |
|---|---|---|---|
| 1교시 | 임베딩으로 문서를 찾는다: 왜 RAG인가(환각·최신성·출처·비용), 임베딩과 의미 유사도, 문서 분할(크기·겹침·경계), 코사인 top-k 검색, 벡터 DB 없이 numpy로 충분한 규모 | 문서를 나누고 임베딩으로 찾기: `chunk.py` → `embed.py` → `search.py` 질의 2개 top-3, chunk 크기 300자와 150자 비교 | `search_note.md`(질의 2개 top-3 표, chunk 크기 비교 문장), `outputs/search-*.json` |
| 2교시 | 검색 결과를 출처 있는 답으로: system·context·question 프롬프트 구조, 출처 표시(파일명#번호), `num_ctx`와 top-k의 한계, "자료에 없으면 찾을 수 없다" 지시, 프롬프트 인젝션 주의 | 출처 있는 답 생성과 거부 경로: `rag_answer.py`로 출처 있는 답 2건, 컨텍스트 밖 질문의 거부 확인, `--no-context`·`--num-ctx` 비교 | `rag_note.md`(답 2건과 인용 확인, 거부 결과, 비교 문장), `outputs/rag-*.json` 3건 이상 |
| 3교시 | 평가셋으로 품질을 잰다: 검색 실패 유형(chunk 경계·용어 불일치·top-k 부족), 환각 점검(답이 컨텍스트에 근거하는가), 소형 평가셋과 hit rate, **2차 종합과제 안내** | 평가셋으로 품질 재기와 실패 분석: `eval.py`로 top-k·chunk 크기별 hit rate 측정, 실패 사례 2개 원인 분석, 2차 과제 체크리스트 점검 | `eval_note.md`(평가 결과표, 실패 분석 2건, 과제 점검표), `outputs/eval-*.md` |

각 블록은 설명·시연 20분, 실습 30분, 휴식 10분으로 운영한다. 분반 시간표에 따라 두 블록과 한 블록이 다른 날에 배치될 수 있으며, 블록 순서는 바꾸지 않는다.

## 준비물

- Git, VS Code, uv, Ollama, PowerShell. NVIDIA GPU가 있으면 `nvidia-smi`가 동작해야 한다(없어도 CPU 경로로 진행한다).
- 사전 캐시된 모델: 임베딩용 `HF_EMBED_MODEL`(교재 검증용 기본값 `intfloat/multilingual-e5-small`, 6주차와 같은 모델), 생성용 `OLLAMA_MODEL`(기본값 `qwen3:8b`, GPU 없는 PC는 `qwen3:0.6b`). `--backend ollama` 대체 경로를 쓰려면 `OLLAMA_EMBED_MODEL`(기본값 `bge-m3`)도 캐시한다. 실습 시간에 내려받지 않는다.
- `examples/mini_rag`를 개인 저장소에 복사한 폴더에서 `uv sync`를 수업 전에 마쳐 둔다(첫 sync는 torch 설치로 오래 걸린다).
- 4주차 산출물 `ollama_client/`의 `.env` 패턴, 6주차 `pretrained_embed.py`의 유사도 행렬 결과. 이번 주 파일은 같은 개인 저장소에 누적한다.
- 정확한 도구 버전, 모델 ID·revision·용량은 [학기별 환경 기준표](../../../environment_baseline_template.md)에서 확정한다.
- 실제 이름, 학번, 토큰, 비밀번호를 실습 파일·문서(`docs/`)·평가셋·공개 저장소에 넣지 않는다. `.env`는 커밋하지 않고 `.env.example`만 둔다. 표시 이름은 `student01`, 팀명은 `team-a` 같은 수업용 값을 쓴다.

## 자료 안내

- [PT 원고](slides.md): 세 번의 20분 설명·시연용 Marp 자료
- [실습지](lab.md): 1·2·3교시 문제, 힌트, 검증, 확장
- [실행 예제](examples/README.md): `mini_rag/` uv 프로젝트 — 수업용 한국어 문서 6개, 분할·임베딩·검색·답 생성·평가 스크립트, 평가셋 10문항
- [따라하기 절차](walkthrough.md): 시연·실습을 `할 일 → 예상 결과 → 확인` 순으로 재현하는 절차서
- 강의 대본: 강의자 별도 관리(비공개)
- [2차 종합과제 안내](../week08_midterm/assignment_brief.md)와 [채점표](../week08_midterm/assignment_rubric.md): 8주차 폴더에 있다. 3교시에 미리 읽고 점검한다.

## 권장 진행 방식

1. 스크립트를 실행하기 전에 "어느 파일의 어느 문장이 1위로 나올지"를 먼저 예상해 적는다.
2. 옵션(`--size`, `--top-k`, `--num-ctx`)은 한 번에 하나만 바꾸고, 바꾸기 전 결과와 나란히 기록한다.
3. 답이 그럴듯해 보여도 `cited`·`cited_in_retrieved`·`refused` 필드로 근거를 확인한다. 인용이 검색 결과 밖이면 환각으로 본다.
4. GPU가 없거나 임베딩 모델 로드가 실패하면 `--device cpu` 또는 `--backend ollama`로 같은 절차를 진행하고, 어느 경로였는지 기록에 남긴다.
5. 기본 문제를 마친 뒤에만 확장 문제를 한다. `outputs/`는 커밋하지 않고 증거로 남길 파일만 `evidence/week07/`에 복사한다.

## 완료 기준

- [ ] `chunk.py`를 300자와 150자로 실행해 청크 수·평균 글자 수를 표로 만들었다.
- [ ] `embed.py`로 인덱스 2개(`index`, `index-150`)를 만들고 백엔드·모델·장치·인코딩 시간을 기록했다.
- [ ] 같은 질의 2개의 top-3가 chunk 크기에 따라 어떻게 달라지는지 한 문장씩 적었다.
- [ ] `rag_answer.py`의 답 2건에 `[출처: 파일명#번호]`가 붙어 있고 인용이 검색 결과 안에 있음을 확인했다.
- [ ] 컨텍스트 밖 질문에 "제공된 자료에서 찾을 수 없습니다"가 나왔고, `--no-context`와의 차이를 적었다.
- [ ] `eval.py`로 hit rate를 top-k 3·top-k 1·150자 인덱스 세 조건에서 측정해 표로 만들었다.
- [ ] 실패 문항 2개(없으면 순위가 가장 낮은 2개)의 원인을 chunk 경계·용어 불일치·top-k 부족 중 하나로 분류하고 근거를 적었다.
- [ ] 2차 종합과제 안내의 "제출 전 검사"를 자기 저장소 기준으로 표시하고 비어 있는 항목을 적었다. 기록에 토큰·개인정보가 없다.

## 제출 증거

이번 주는 별도 제출물이 없다. 아래 증거를 개인 저장소에 누적한다. `outputs/`는 `.gitignore`에 들어 있으므로 남길 파일은 `evidence/week07/`로 복사해 커밋한다.

1. `search_note.md`: 청크 수 표, 질의 2개 × chunk 크기 2개의 top-3 표, chunk 크기 비교 문장
2. `rag_note.md`: 출처 있는 답 2건(질문·답·인용·`cited_in_retrieved`), 컨텍스트 밖 질문 결과, `--no-context`·`--num-ctx` 비교 문장
3. `eval_note.md`: 세 조건의 hit rate 표, 실패 사례 2건(증상·원인 유형·근거·개선안), 2차 과제 점검표
4. `evidence/week07/`: `search-*.json` 1건, `rag-*.json` 2건(정상·거부), `eval-*.md` 1건
5. `git log --oneline -3` 결과(이번 주 commit 3개 이상)

## 다음 주 연결

8주차 `week08_midterm`은 1~7주 내용을 혼자 재현하는 수시 실기평가와 2차 종합과제 제출 주다. 이번 주 `mini_rag/`와 `evalset.json`은 과제의 RAG 미니프로젝트로 확장되므로, 수업 전에 [2차 종합과제 안내](../week08_midterm/assignment_brief.md)의 필수 산출물 목록을 읽고 자기 문서 10개를 어떤 라이선스 조건으로 모을지 정해 둔다. 실기평가 범위에는 이번 주의 `/api/embed`·`/api/chat` 호출과 출처 표시도 포함된다.

## 참고 자료

- [Sentence Transformers 문서](https://sbert.net/)
- [Transformers 문서](https://huggingface.co/docs/transformers/)
- [Ollama API 레퍼런스](https://github.com/ollama/ollama/blob/main/docs/api.md)
- [Ollama 문서](https://docs.ollama.com/)
- [OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
