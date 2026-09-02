# 15주차 실습 — 발표하고, 검증받고, 회고하라

## 공통 규칙

- 완성 코드를 보기 전에 예상을 적는다.
- 명령은 현재 폴더를 확인한 뒤 실행한다.
- 각 교시에서 정상 경로와 실패·경계 경로를 최소 한 번씩 재현한다.
- 캡처보다 원인과 근거를 적은 짧은 문장이 더 중요한 증거다.
- 기본 문제 완료 후 확장 문제를 수행한다.
- 발표·검증은 릴리스 태그가 가리키는 기준본으로만 한다. 다른 팀이 발표하는 동안 자기 코드를 고치지 않는다.
- 실습 시간에 모델을 내려받지 않는다. 다른 팀 저장소에는 Issue 외의 쓰기(push)를 하지 않는다.

## 1교시 실습 — 최종 발표 라운드

### 상황

팀 저장소는 14주차에 `v0.1.0`으로 릴리스되었고, 다른 팀이 README만 보고 재현을 시도해 Issue를 남겼다. 이제 평가자와 청중 앞에서 팀당 시연 3분 + 질의 2분으로 "다른 사람이 재현·검증·기여할 수 있는 릴리스"임을 보여야 한다. 발표하지 않는 동안에는 평가자의 시선으로 다른 팀의 발표를 기록한다.

이어받는 것: 14주차 3교시의 시연 리허설 기록과 `demo_outline.md`, 릴리스 태그(결함을 고쳤다면 패치 태그).

### 시간 배분

| 단계 | 시간 | 활동 |
|---|---:|---|
| 준비·장비 점검 | 0–5분 | 발표 순서·기록 담당 확인, 발표 PC에서 태그·모델 캐시·fallback 자료 확인 |
| 발표 라운드 전반 | 5–15분 | 1·2번 팀: 팀당 시연 3분 + 질의 2분. 청중은 발표 기록표 작성 |
| 발표 라운드 후반 | 15–25분 | 3·4번 팀: 같은 규칙. 앞 팀이 답하지 못한 질문을 기록표에 옮김 |
| 증거 정리 | 25–30분 | 받은 질문·답하지 못한 질문·장애 기록, 2교시 검증 대상 팀의 URL·태그 확인 |

팀이 4팀을 넘으면 발표 라운드는 학교 시간표에 따라 확장하거나 별도 슬롯으로 나눈다. 시간표가 바뀌어도 팀당 5분과 기록 규칙은 같다.

### 준비

`examples/`를 개인 실습 폴더에 복사한다. 원본은 수정하지 않는다.

```powershell
New-Item -ItemType Directory week15-practice
Copy-Item -Recurse <교재 경로>\week15_final_presentation\examples\* .\week15-practice\
Set-Location week15-practice
```

발표 PC의 팀 저장소 clone본에서 기준본을 확인한다.

```powershell
git status                 # clean 이어야 한다
git describe --tags        # 발표 기준 태그
ollama list                # 시연 모델이 캐시되어 있는지
```

### 문제 1 · 발표 실행(발표 팀)

1. `demo_outline.md`의 표를 우리 팀 값으로 채우고, 시연 명령을 순서대로 한 파일에 적어 둔다.
2. 기준본에서 시작한다. `git status`가 clean이고 `git describe --tags`가 제출 태그인지 화면에 보인다.
3. 문제 → 시연 → 한계 → 다음 순서로 3분 안에 끝낸다. 시연 구간에서는 핵심 기능 1개를 **실제로 실행**하고, 오류 처리 1개(예: Ollama 연결 실패 메시지)를 보여 준다.
4. 질의 2분에는 질문을 다시 말하고 → 사실 → 이유 → 한계·다음 조치 순으로 답한다. 모르면 모른다고 말하고 확인 방법을 말한다.
5. 장애가 나면 `demo_outline.md`의 fallback대로 진행하고, 기록 담당이 무엇이 언제 실패했는지 적는다.

완료 조건:

- [ ] 기준본(태그) 확인 출력이 화면에 나왔다.
- [ ] 시연에 실제 실행과 한계 진술이 모두 있었다(기록 담당이 확인).
- [ ] 받은 질문과 답변, 답하지 못한 질문을 `presentation_log.md`에 적었다.

### 문제 2 · 발표 기록(청중)

`presentation_log.md`에 팀마다 한 행씩 기록한다. 점수를 적지 않는다.

| 팀 | 문제 한 줄 | 실제로 실행된 것 | 한계로 말한 것 | 재현 절차 언급 | 질문·답변 요약 | 장애·시간 |
|---|---|---|---|---|---|---|
| team-b | | | | 예 / 아니오 | | |

1. 발표 시작 30초 안에 문제와 사용자가 이해되었는지 적는다.
2. "실제로 실행된 것"에는 화면에서 실행된 명령이나 UI 동작만 적는다. 말로만 한 설명은 적지 않는다.
3. 질의에서 `question_cards.md`의 어느 카드가 나왔는지와 답의 근거(파일·수치)가 있었는지 적는다.
4. 2교시에 검증할 팀의 저장소 URL과 태그를 발표 화면에서 받아 적는다.

완료 조건:

- [ ] 발표한 모든 팀에 대해 한 행씩 있다.
- [ ] 2교시 검증 대상 팀의 URL·태그를 적었다.

### 단계별 힌트

<details>
<summary>힌트 1 — 3분을 넘긴다</summary>

화면 이동을 줄인다. 저장소 열기·서버 켜기·모델 로드는 발표 전에 끝내고, 시연은 기능 1개만 한다. 평가 결과와 한계는 파일을 열어 수치 1개와 사례 1개만 가리킨다.
</details>

<details>
<summary>힌트 2 — 시연 중 Ollama 연결이 실패한다</summary>

`ollama serve`를 1회 재시작한다. 그래도 안 되면 사전 저장한 `outputs/` 결과로 같은 흐름을 설명한다. 이때 "연결 실패 시 우리 서비스가 돌려주는 메시지"를 보여 주면 오류 처리 시연이 된다.
</details>

<details>
<summary>힌트 3 — 질문에 답을 모른다</summary>

"지금 저장소에는 그 기록이 없다. 확인해서 Issue로 답하겠다"처럼 확인 방법을 말한다. 추측으로 채우지 않는다. 기록 담당이 그 질문을 `presentation_log.md`에 남긴다.
</details>

### 검증

- 정상: 3분 안에 실제 실행 결과가 화면에 나오고, 한계 한 문장이 말로 나왔다.
- 경계 또는 실패: 장애가 나면 fallback으로 넘어가 시간 안에 마쳤고, 장애 원인이 기록에 있다.
- 설명: "평가자가 이 발표에서 재현 가능하다고 믿을 근거는 무엇이었는가"를 한 문장으로 적었다.

### 확장 문제

1. 다른 팀 발표를 듣고 `question_cards.md`에 없는 질문 1개를 만들어 카드 형식으로 적는다.
2. 우리 팀 발표를 녹화했다면 3분 중 실제 실행 구간이 몇 초였는지 재고, 늘릴 방법을 한 문장으로 적는다.

## 2교시 실습 — 교차 재현 검증

### 상황

기말평가는 평가자가 제출된 릴리스를 깨끗한 PC에서 체크리스트대로 검증하는 방식이다. 같은 절차를 다른 팀 저장소에 먼저 적용해 본다. 처음 보는 사람처럼 README만 읽고 시작하고, 막히면 재시도 1회 뒤 기록한다.

이어받는 것: 1교시 `presentation_log.md`에 적은 검증 대상 팀의 저장소 URL과 태그, `release_verify/` 복사본.

### 시간 배분

| 단계 | 시간 | 활동 |
|---|---:|---|
| 문제·예상 | 0–4분 | 대상 팀 README만 읽고 예상 결과와 예상 실패 지점 적기 |
| clone·동기화·실행 | 4–14분 | `cross_review.ps1` 또는 수동 6단계, README 절차대로 핵심 기능 1개 실행 |
| 테스트·문서·비밀 검사 | 14–22분 | `uv run pytest -q`, `verify_release.py`, LICENSE ↔ `SOURCES.md` 대조 |
| 검증·기록 | 22–30분 | `reviewer_checklist.md` 채우기, 실패 분류, 릴리스 결함 Issue 1건 등록 |

### 준비

```powershell
Set-Location .\week15-practice\release_verify
Copy-Item .env.example .env
uv sync
.\cross_review.ps1 -RepoUrl <대상 팀 저장소 URL> -Team team-b -Tag v0.1.0
```

스크립트가 clone → 태그 checkout → `uv sync --frozen` → pytest → `verify_release.py`를 실행하고 `outputs\cross-review-team-b-<시각>.log`를 남긴다. 실패한 단계에서 멈추지 않고 끝까지 기록하므로 로그를 위에서부터 읽는다. 네트워크가 없으면 `-RepoUrl`에 로컬 경로를 준다.

### 문제 1 · 체크리스트 검증

`reviewer_checklist.md`를 `review-team-b.md`로 복사해 채운다.

1. 0단계: 저장소 URL·태그·commit id를 적는다. `git -C .\review\team-b describe --tags --exact-match`로 태그가 HEAD를 가리키는지 본다.
2. 1~2단계: 로그에서 clone과 `uv sync --frozen` 결과를 옮겨 적는다. sync가 실패했으면 메시지 첫 줄로 lock 불일치(릴리스 결함)인지 네트워크·캐시(환경)인지 판단한다.
3. 3단계: `.\review\team-b`로 이동해 README 재현 절차대로 핵심 기능 1개를 직접 실행한다. README의 예시 출력과 형태가 같은지 적는다. 모델이 없으면 내려받지 않고 "환경"으로 기록한다.
4. 4~7단계: pytest 결과, `outputs\verify-team-b-<시각>.md`의 FAIL·WARN 항목을 옮겨 적고, WARN은 파일을 직접 열어 통과/실패를 판단한다. LICENSE와 `SOURCES.md`의 모델·데이터 라이선스가 호환되는지 한 문장으로 적는다.
5. 8~9단계: 평가 결과 파일의 수치가 README·발표와 같은지, `git -C .\review\team-b shortlog -sn --no-merges`에 팀원 전원이 있는지 적는다.

완료 조건:

- [ ] 0~9단계 모두에 통과/실패/해당 없음과 근거가 있다.
- [ ] 실패마다 환경 문제 / 릴리스 결함 / 설계 한계 분류가 있다.
- [ ] "README만으로 10분 안에 실행할 수 있는가"에 예/아니오와 이유가 있다.

### 문제 2 · 재현 실패 보고

1. 릴리스 결함으로 분류한 실패 중 가장 먼저 막힌 것 1개를 고른다. 결함이 없으면 WARN 항목 중 문서 보완이 필요한 것 1개를 고른다.
2. `reviewer_checklist.md`의 Issue 양식대로 대상 팀 저장소에 Issue를 등록한다. 제목은 `[재현] <단계 번호> <한 줄 증상>`.
3. 환경·재현 절차·기대·실제(출력 첫 3줄)·분류를 채운다. 추측·비난·점수 표현을 넣지 않는다.
4. Issue URL을 `review-team-b.md` 종합 절에 적는다.

완료 조건:

- [ ] Issue에 재현 절차와 실제 출력이 있어 대상 팀이 그대로 따라 할 수 있다.
- [ ] 환경 문제를 릴리스 결함으로 보고하지 않았다.

### 단계별 힌트

<details>
<summary>힌트 1 — `uv sync --frozen`이 실패한다</summary>

메시지에 `uv.lock`이 없다거나 `pyproject.toml`과 맞지 않는다는 내용이 있으면 릴리스 결함이다. 패키지 다운로드 실패·프록시·타임아웃이면 환경 문제다. `--frozen`을 빼고 성공하는지는 참고만 하고, 기록에는 "`--frozen` 실패"로 남긴다.
</details>

<details>
<summary>힌트 2 — 모델이 없어 실행이 안 된다</summary>

실습 시간에 내려받지 않는다. `ollama list`로 캐시된 모델을 보고, 대상 팀 README가 CPU 대체(`qwen3:0.6b` 등)를 허용하면 `OLLAMA_MODEL`만 바꿔 실행한다. 허용하지 않으면 "환경 문제, README에 모델 ID·용량 명시 여부: 예/아니오"로 기록한다.
</details>

<details>
<summary>힌트 3 — `tests/`가 없거나 pytest가 실패한다</summary>

`tests/`가 없으면 4단계는 "실패 — 테스트 없음"이고 릴리스 결함이다. 실패한 테스트가 README나 Issue에 "알려진 실패"로 적혀 있으면 통과 조건부로 적고, 적혀 있지 않으면 결함이다.
</details>

### 검증

- 정상: clone → `uv sync --frozen` → 실행 → pytest가 개입 없이 통과하고 `verify_release.py`에 FAIL이 없다.
- 경계 또는 실패: 한 단계 이상 실패했고, 로그 첫 줄로 원인을 분류했으며 릴리스 결함만 Issue로 갔다.
- 설명: "이 저장소에서 가장 먼저 고쳐야 할 것과 그 이유"를 한 문장으로 적었다.

### 확장 문제

1. `checks.py`의 `README_SECTIONS`에 "GPU 없는 대체 경로" 패턴을 추가하고 대상 저장소를 다시 검사한다.
2. 대상 팀 README의 재현 절차를 새 폴더에서 처음부터 다시 따라 하며 걸린 시간을 재고, 10분을 넘긴 단계를 적는다.

## 3교시 실습 — 회고와 최종 제출 점검

### 상황

발표와 교차 검증이 끝났다. 우리 팀도 다른 팀의 검증 Issue를 받았다. 이제 동료에게 실행 가능한 피드백을 전달하고, 학기 동안의 작업을 근거와 함께 회고하고, 4차 종합과제 제출 정보를 확정한다. 릴리스 뒤에 고친 것이 있다면 패치 태그로 기준본을 다시 찍는다.

이어받는 것: 2교시 `review-<팀>.md`와 등록한 Issue, 우리 팀이 받은 Issue, `presentation_log.md`.

### 시간 배분

| 단계 | 시간 | 활동 |
|---|---:|---|
| 동료 피드백 | 0–8분 | `peer_feedback_form.md` 작성 → 대상 팀 Issue 또는 Discussion에 전달 |
| 개인 회고 | 8–18분 | `retrospective_template.md`를 근거와 함께 채우기 |
| 제출 점검 | 18–26분 | `submission_checklist.md` 확인, 자기 저장소에 `verify_release.py` 실행, 태그·commit id 확인 |
| 검증·기록 | 26–30분 | `submission.md` 작성, 개인 저장소에 증거 commit |

### 준비

```powershell
Set-Location .\week15-practice
Copy-Item .\peer_feedback_form.md .\peer_feedback-team-b.md
Copy-Item .\retrospective_template.md .\retrospective.md
Copy-Item .\submission_checklist.md .\submission.md
```

팀 저장소 clone본에서:

```powershell
git fetch --tags
git describe --tags --exact-match     # 기준본 태그
git shortlog -sn --no-merges          # 팀원별 commit 수
```

### 문제 1 · 동료 피드백과 개인 회고

1. `peer_feedback-team-b.md`의 3절을 채운다. 좋았던 점 1, 재현 실패 1, 제안 1, 질문 1. 각 칸에 파일·명령·수치가 하나 이상 들어간다.
2. 대상 팀 저장소 Issue(또는 Discussion)에 남기고 URL을 적는다. 재현 실패는 2교시 Issue에 이미 있으면 링크만 단다.
3. `retrospective.md`의 1~3절을 채운다. 항목마다 근거(commit·Issue·PR·실험 기록)를 붙인다. 근거를 못 찾는 항목은 지운다.
4. 4절에 `git shortlog` 결과와 자기 commit·Issue·PR·Review 대표 URL을 적는다.
5. 5~7절(AI 도구 회고, 받은 피드백 반영 결정, 이후에 할 일 3개)을 채운다.

완료 조건:

- [ ] 피드백 4칸 모두에 구체적 근거가 있고 대상 팀에 전달한 URL이 있다.
- [ ] 회고 1~3절의 모든 항목에 근거가 붙어 있다.
- [ ] 이후에 할 일 3개가 기여 지속·포트폴리오·라이선스 유지에 하나씩 대응한다.

### 문제 2 · 최종 제출 점검

1. 팀 저장소에서 `verify_release.py`를 실행한다.

   ```powershell
   Set-Location .\release_verify
   uv run python verify_release.py --repo <팀 저장소 경로> --team team-a --check-ollama
   ```

2. FAIL 항목을 고치거나(문서·`.gitignore`·태그), 고칠 수 없으면 이유를 `submission.md`에 적는다. 비밀 패턴 FAIL이 실제 값이면 즉시 제거하고 토큰을 회전한다.
3. 릴리스 뒤 고친 commit이 있으면 CHANGELOG에 적고 패치 태그를 찍는다.

   ```powershell
   git tag -a v0.1.1 -m "Fix reproduction issues found in cross review"
   git push origin v0.1.1
   ```

4. `submission.md`의 체크리스트를 위에서부터 확인하고, 제출 정보 양식에 저장소 URL·태그·commit id·재현 절차·팀원별 기여 URL·시연 영상 위치·받은 Issue 처리를 적는다.
5. 개인 저장소에 `presentation_log.md`, `review-team-b.md`, `peer_feedback-team-b.md`, `retrospective.md`, `submission.md`를 commit한다.

완료 조건:

- [ ] `verify_release.py` 결과에 FAIL이 없거나 남은 FAIL의 이유가 `submission.md`에 있다.
- [ ] 제출 정보 양식의 commit id가 `git describe --tags --exact-match`의 태그가 가리키는 commit과 같다.
- [ ] 팀원 전원의 기여 URL이 있다.

### 단계별 힌트

<details>
<summary>힌트 1 — 태그가 HEAD를 가리키지 않는다(WARN)</summary>

릴리스 뒤에 commit이 더 있다는 뜻이다. 그 commit이 제출본에 들어가야 하면 CHANGELOG를 갱신하고 패치 태그를 찍는다. 들어가면 안 되면 제출 commit id를 태그의 commit으로 적고 그 뒤 commit은 다음 버전으로 남긴다.
</details>

<details>
<summary>힌트 2 — 비밀 패턴이 자리표시자에 걸린다</summary>

`.env.example`의 값은 비워 둔다(`HF_TOKEN=`). 문서 예시라면 `hf_xxxx`처럼 패턴에 안 걸리는 짧은 표기로 바꾼다. 실제 값이면 파일에서 지우는 것으로 끝나지 않는다. 이력에 남으므로 토큰을 회전하고 그 사실을 기록한다.
</details>

<details>
<summary>힌트 3 — 회고에 쓸 근거를 못 찾는다</summary>

`git log --author=<표시 이름> --oneline`, 저장소 Issues·Pull requests 탭의 본인 필터, `experiments/run-*.md`, `outputs/eval-*.json`을 본다. 근거가 없는 항목은 "근거 없음 — 다음에는 기록하겠다"로 다음에 다르게 할 것 절에 옮긴다.
</details>

### 검증

- 정상: `verify_release.py` FAIL 0, 태그가 HEAD를 가리키고, `submission.md`의 commit id와 일치한다.
- 경계 또는 실패: FAIL 또는 WARN이 남았지만 각각에 사람이 판단한 이유가 적혀 있다.
- 설명: "우리 릴리스에서 처음 보는 사람이 가장 먼저 막힐 곳과 그것을 README 어디에 적었는가"를 한 문장으로 적었다.

### 확장 문제

1. 다른 팀에서 받은 Issue 하나를 실제로 고쳐 PR → 리뷰 → merge → 패치 태그까지 진행하고 CHANGELOG에 적는다.
2. `retrospective.md`의 "이후에 할 일" 중 하나를 Issue로 만들어 마일스톤과 담당을 지정한다.

## 제출 체크

- `presentation_log.md`: 다른 팀 발표 기록(팀마다 한 행)
- `review-<팀>.md`: 교차 재현 검증 체크리스트 0~9단계, 실패 분류, Issue URL, `outputs/verify-<팀>-*.md` 경로
- `peer_feedback-<팀>.md`: 동료 피드백 4칸과 전달 URL
- `retrospective.md`: 근거 있는 회고와 이후에 할 일 3개
- `submission.md`: 체크리스트 확인 결과와 제출 정보 양식(저장소 URL·태그·commit id·재현 절차·팀원별 기여 URL)
- 선택: 확장 문제 결과(패치 태그, Issue URL)
