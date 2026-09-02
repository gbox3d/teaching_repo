# 모델 보고서 — 4주차

- 작성자: `student01`
- 측정 PC: GPU 이름 · VRAM (1주차 `env_check.md`에서 복사)
- 서버 주소·기본 모델: `OLLAMA_HOST` · `OLLAMA_MODEL` 값 (환경변수로 관리하며 실제 값을 여기에 적는다)

## 1. 측정 대상

| 항목 | 모델 A(기본) | 모델 B(소형) |
|---|---|---|
| 이름:태그 | | |
| 파라미터 수 (`ollama show` → parameters) | | |
| 양자화 (`ollama show` → quantization) | | |
| 컨텍스트 길이 (`ollama show` → context length) | | |
| 파일 크기 (`ollama list` → SIZE) | | |
| 메모리 크기 (`ollama ps` → SIZE) | | |
| PROCESSOR (`ollama ps` → 예: `100% GPU`) | | |
| eval rate 평균 tokens/s (`/set verbose`, 질문 3개 평균) | | |
| 첫 응답 load duration | | |

## 2. 같은 질문 3개

측정에 쓰는 질문은 바꾸지 않는다. 바꾸면 비교가 아니다.

- Q1: `uv가 무엇인지 두 문장으로 설명해 줘.`
- Q2: `MIT 라이선스와 GPL의 차이를 표로 정리해 줘.`
- Q3: `다음 JSON을 고쳐 줘: {"name": "student01", "week": 4,}`

| 질문 | 모델 A 답 요약 (길이·형식·정확성) | 모델 B 답 요약 | 차이 한 문장 |
|---|---|---|---|
| Q1 | | | |
| Q2 | | | |
| Q3 | | | |

## 3. 계산과 실측

- 모델 A: 파라미터 수 × 파라미터당 바이트(양자화 기준) = 예상 가중치 크기 ____ GB. 실제 파일 크기 ____ GB. 차이의 이유: ____
- `ollama list`의 SIZE와 `ollama ps`의 SIZE가 다른 이유: ____
- 모델 B가 모델 A보다 tokens/s가 ____배 빠르다/느리다. 이유: ____

## 4. 결론

- 팀 도우미의 기본 모델로 ____ 를 고른다. 이유 두 가지: ____ / ____
- GPU가 없는 팀원의 대체 모델: ____ (품질에서 잃는 것: ____)

## 5. 커스텀 모델 전후 비교 (3교시에 채운다)

| 질문 | 기준 모델 | 커스텀 v1 (Modelfile SYSTEM) | 커스텀 v2 (SYSTEM 한 줄 변경: ____) | 관찰 |
|---|---|---|---|---|
| Q1 | | | | |
| Q2 | | | | |
| Q3 | | | | |

- 요청의 `--system`과 Modelfile의 SYSTEM이 둘 다 있을 때 관찰한 것: ____
