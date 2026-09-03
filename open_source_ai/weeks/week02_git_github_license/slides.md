---
marp: true
theme: default
paginate: true
header: "오픈소스 AI 응용 · 2주차"
footer: "Git/GitHub 협업과 라이선스"
---

# 2주차
## Git/GitHub 협업과 라이선스

**60분 블록 × 3**<br>
매 블록 설명·시연 20분 + 직접 해결 실습 30분 + 휴식 10분

---

## 이번 주 세 블록

| 교시 | 설명·시연 20분 | 직접 해결 실습 30분 |
|---|---|---|
| 1교시 | 브랜치·원격·충돌 해결 | 원격 연결과 충돌 1회 해결 |
| 2교시 | GitHub 협업 흐름과 리뷰 | 짝 저장소에 제안하고 리뷰 받기 |
| 3교시 | 라이선스 읽기와 고르기 | 라이선스 판별과 LICENSE 추가 |

이번 주 질문: 내 변경을 다른 사람의 저장소에 **안전하게 제안**하고, 그 코드를 **어떤 조건으로** 쓰고 나눌 수 있는지 어떻게 판단하는가?

---

<!-- _class: lead -->

# 1교시 · 설명 20분
## 브랜치·원격·충돌 해결

---

## 0–3분 · 이어받는 것: 로컬에만 있는 기록

```text
1주차: git init → "Add environment report"   (내 PC 한 곳에만 있음)
2주차: 그 기록을 GitHub에 올리고, 갈라진 작업을 합친다
```

- 지금 저장소는 내 PC에만 있다. 디스크가 고장 나면 사라진다.
- 다른 사람이 볼 수도, 제안할 수도 없다.
- 오늘은 **원격**이라는 네 번째 장소가 생긴다.

**질문:** `git log`에는 기록이 있는데 GitHub에는 아직 없다. 어느 명령이 빠졌는가?

---

## 3–6분 · 세 영역 복습

```text
working tree ── git add ──▶ staging area ── git commit ──▶ repository(HEAD)
   수정 중                    다음 기록 후보                  확정 기록
```

- `git status`: 세 영역의 차이 요약
- `git diff`: working tree ↔ stage · `git diff --staged`: stage ↔ HEAD
- 한 commit = 한 의도. 메시지만 읽고 변화를 알 수 있어야 한다

**핵심:** commit은 로컬에서 끝난다. 원격은 별도의 명령으로만 바뀐다.

---

## 6–9분 · 원격: clone·push·pull·fetch

```text
로컬 main ── push ──▶ origin/main (GitHub)
로컬 main ◀─ pull ─── origin/main      (= fetch + merge)
          ◀─ fetch ── origin/main 참조만 갱신, 작업 파일은 그대로
```

```bash
git remote add origin (본인 저장소 HTTPS URL)
git push -u origin main
git branch -vv
```

- `clone`: 원격을 통째로 복사해 새 로컬을 만든다
- `-u`: 추적 관계를 기억해 이후 `git push`만으로 같은 곳에 보낸다

**질문:** `fetch` 뒤에 파일이 하나도 안 바뀌었다. 실패인가?

---

## 9–13분 · branch와 merge

```text
main:            A ── B ─────────── M   (merge commit, 부모 둘)
                       \           /
feature/readme:         C ── D ───┘
```

```bash
git switch -c feature/readme   # 만들고 이동
git switch main
git merge feature/readme
```

- branch = commit을 가리키는 **이름표**. 만드는 비용은 거의 0
- fast-forward: main이 뒤처지기만 했으면 이름표만 앞으로 옮긴다
- merge commit: 양쪽 다 진행했으면 부모가 둘인 commit을 만든다

---

## 13–16분 · 충돌은 선택 요청이다

```text
<<<<<<< HEAD
이 저장소는 오픈소스 AI 응용 수업의 실습 기록이다.
=======
이 저장소는 로컬 AI 도우미 프로젝트의 시작점이다.
>>>>>>> feature/readme
```

- 조건: 두 branch가 **같은 파일의 같은 줄**을 다르게 바꿨다
- Git은 어느 쪽이 옳은지 모른다. 사람이 결과 문장을 쓴다
- 절차: `git status` → 파일 열기 → 마커 제거·결과 작성 → `git add` → `git commit`
- 되돌리기: `git merge --abort`

**핵심:** 충돌은 오류가 아니라 **결정을 요청하는 상태**다.

---

## 16–18분 · 커밋 메시지 규약

```text
Add run instructions to README

New members could not find how to start the tool.
Related to #3
```

- 제목: 명령형 동사로 시작, 50자 안팎, 마침표 없음
- 제목과 본문 사이 빈 줄 하나
- 본문: 무엇이 아니라 **왜**. 관련 Issue 번호
- 나쁜 예: `update`, `fix`, `final2`

**질문:** `git log --oneline`만 읽고 각 commit이 사용자에게 준 변화를 말할 수 있는가?

---

## 18–20분 · 실습 인계

[1교시 실습 — 원격 연결과 충돌 1회 해결](lab.md#1교시-실습--원격-연결과-충돌-1회-해결)

완료 조건:

1. `git branch -vv`에서 `main`이 `origin/main`을 추적하고 같은 commit이다
2. 같은 줄 충돌을 한 번 재현하고, 마커 없는 결과 문장으로 merge commit을 만들었다
3. `git log --graph --oneline --all`에 두 갈래와 합류점이 보인다

실습 30분 뒤 휴식 10분. 휴식 후 2교시.

---

<!-- _class: lead -->

# 2교시 · 설명 20분
## GitHub 협업 흐름과 리뷰

---

## 0–3분 · 이어받는 것: 내 저장소에서 남의 저장소로

- 1교시: **내** 저장소 안에서 branch를 합쳤다
- 2교시: **쓰기 권한이 없는** 남의 저장소에 변경을 제안한다
- 도구: Fork, Issue, Pull Request, Review — 모두 GitHub 기능이며 Git 자체에는 없다
- 오늘 실습은 2인 1조. 서로의 저장소에 제안하고 서로 리뷰한다

**질문:** push 권한이 없는 저장소에 `git push`하면 무슨 일이 생기는가?

---

## 3–7분 · 협업 흐름 6단계

```text
Fork ──▶ Issue ──▶ Branch ──▶ Pull Request ──▶ Review ──▶ Merge
내 복사본  제안·합의   작업선      변경 요청        검토·수정    반영
```

| 단계 | 어디서 | 누가 |
|---|---|---|
| Fork · Branch · push | 내 계정, 내 PC | 제안자 |
| Issue · PR | 원본 저장소 | 제안자 |
| Review · Merge | 원본 저장소 | 관리자(저장소 주인) |

**핵심:** 제안자는 원본을 직접 건드리지 않는다. 관리자가 Merge 버튼을 누른다.

---

## 7–10분 · Issue: 코드보다 제안이 먼저

- Issue = "이 변경을 해도 되는가"를 코드를 쓰기 **전에** 묻는 곳
- 좋은 Issue: 현재 상황 → 제안 → 기대 효과 → 대안
- 관리자가 "좋다"고 답하면 그때 branch를 만든다
- 거절되어도 잃는 것이 없다. 아직 코드를 쓰지 않았기 때문이다
- PR 본문의 `Closes #12`는 merge 시 Issue를 자동으로 닫는다

**질문:** Issue 없이 큰 PR을 보냈다가 거절당하면 무엇을 잃는가?

---

## 10–13분 · 작은 PR과 PR 설명 양식

| 항목 | 내용 |
|---|---|
| 관련 Issue | `Closes #12` |
| 변경 내용 | 무엇을 바꿨는가(파일·동작) |
| 변경 이유 | 왜 필요한가 |
| 확인 방법 | 리뷰어가 그대로 실행할 명령 |
| 체크리스트 | 의도 하나, 비밀 없음, 실행 확인, 출처 기록 |

- PR 하나 = 의도 하나. 리뷰어가 **10분 안에 읽는 크기**
- **Draft PR**: 아직 merge 대상이 아니다. 방향을 먼저 묻고 싶을 때 연다

---

## 13–16분 · 리뷰 예절: 코드에 대해, 사람이 아니라

- 대상은 코드와 근거: "이 줄은 현재 폴더를 확인하지 않는다" (O) / "왜 이렇게 했어요?" (X)
- 요청은 구체적으로: 무엇을, 왜, 어떻게 바꾸면 되는지
- 질문형으로 열어 둔다: "이 명령이 Windows에서도 같은가?"
- 좋은 점도 한 줄 적는다
- 제안자는 방어하지 않고 **수정 commit으로 답한다**
- Approve · Comment · Request changes 중 하나를 근거와 함께

**핵심:** 리뷰는 판정이 아니라 **함께 고치는 대화**다.

---

## 16–18분 · 템플릿이 하는 일

```text
.github/
├─ PULL_REQUEST_TEMPLATE.md     # PR을 열 때 본문에 자동 삽입
└─ ISSUE_TEMPLATE/
   └─ proposal.md               # Issue를 만들 때 선택지로 표시
CONTRIBUTING.md                  # 기여 절차·규칙 안내
```

- 원본 저장소의 **기본 branch**에 있어야 적용된다
- 양식이 있으면 리뷰어가 물어야 할 질문이 줄어든다
- `examples/pr_template/`을 그대로 복사해 시작한다

**질문:** 템플릿을 fork에만 넣으면 원본으로 보내는 PR에 적용되는가?

---

## 18–20분 · 실습 인계

[2교시 실습 — 짝 저장소에 제안하고 리뷰 받기](lab.md#2교시-실습--짝-저장소에-제안하고-리뷰-받기)

완료 조건:

1. 짝 저장소에 Issue 1개와 템플릿을 채운 PR 1개를 올렸다(URL)
2. 짝의 PR에 줄 단위 리뷰 코멘트 1개 이상과 수정 요청을 남겼다(URL)
3. 수정 commit이 push되고 PR이 merge되었다

실습 30분 뒤 휴식 10분. 휴식 후 3교시.

---

<!-- _class: lead -->

# 3교시 · 설명 20분
## 라이선스 읽기와 고르기

---

## 0–3분 · 저작권이 먼저, 라이선스는 허락

```text
코드를 쓰는 순간 저작권 발생 (등록 불필요)
        ▼
기본값: 모든 권리 보유 → 남은 복제·수정·재배포 불가
        ▼
LICENSE 파일 = 저작권자가 조건을 붙여서 주는 허락
```

- GitHub에 공개되어 있어도 **LICENSE가 없으면 허락이 없는 것**이다
- 2교시에 merge된 짝의 코드도 라이선스가 없으면 조건을 말할 수 없다

**질문:** 별이 1만 개인 저장소에 LICENSE가 없다. 내 프로젝트에 넣어도 되는가?

---

## 3–6분 · permissive: MIT·Apache-2.0·BSD

| 라이선스 | SPDX ID | 지켜야 할 것 |
|---|---|---|
| MIT | `MIT` | 저작권·허가 고지 유지 |
| BSD 3-Clause | `BSD-3-Clause` | 고지 유지, 이름을 홍보에 쓰지 않음 |
| Apache 2.0 | `Apache-2.0` | 고지, NOTICE 유지, 변경 표시, 특허 허가 |

- 공통: 상업적 이용 가능, 비공개 수정 가능, 재배포 시 고지만 유지
- "허용적" = 결과물의 라이선스를 강제하지 않는다
- 이 수업의 개인 저장소 기본 선택: **MIT 또는 Apache-2.0**

**질문:** MIT 라이브러리를 유료 앱에 넣어 소스를 공개하지 않고 팔 수 있는가?

---

## 6–9분 · copyleft: GPL·LGPL·AGPL

| 라이선스 | SPDX ID | 소스 공개 의무가 생기는 때 |
|---|---|---|
| GPL 3.0 | `GPL-3.0-only` | 결합한 프로그램을 **배포**할 때, 전체 |
| LGPL 3.0 | `LGPL-3.0-only` | 라이브러리 수정분만(동적 링크한 앱은 자유) |
| AGPL 3.0 | `AGPL-3.0-only` | 배포 없이 **네트워크 서비스**로 제공해도 |

- "같은 자유를 다음 사람에게도" — 결과물도 같은 라이선스
- 내부에서만 쓰고 배포하지 않으면 의무가 생기지 않는다(AGPL은 예외)

**핵심:** 의무를 발생시키는 사건이 배포인지, 서비스 제공인지 구분한다.

---

## 9–12분 · 특허 조항과 호환성 방향

```text
permissive ──▶ copyleft    : 가능 (MIT 코드를 GPL 프로젝트에)
copyleft   ──▶ permissive  : 불가 (결과물이 GPL이 된다)
Apache-2.0 ──▶ GPL-3.0     : 가능
Apache-2.0 ──▶ GPL-2.0     : 불가
```

- Apache-2.0: 기여자의 **특허 사용 허가** 포함, 특허 소송을 걸면 허가 종료
- MIT·BSD: 특허 언급 없음 → 기업 프로젝트가 Apache-2.0을 고르는 이유
- 호환성 = 합쳐서 배포할 때 두 조건을 **동시에** 지킬 수 있는가

**질문:** MIT 코드와 GPL-3.0 코드를 합친 프로그램을 MIT로 배포할 수 있는가?

---

## 12–15분 · 모델 라이선스: 오픈 웨이트 ≠ 오픈소스

| 모델 계열 | 라이선스 | 성격 |
|---|---|---|
| Qwen (대부분의 크기) | Apache-2.0 | OSI 승인, 조건 적음 |
| Llama | Llama Community License | 사용 정책, 표기, 대규모 사용자 별도 허가 |
| Gemma | Gemma Terms of Use | 금지 용도 정책 포함 |
| RAIL 계열(OpenRAIL-M) | 사용 제한 조항 | 용도 제한 = OSI 정의 밖 |

- OSI 오픈소스 AI 정의: 용도 제한 없이 사용·연구·수정·공유 + 데이터 정보·코드·가중치
- "가중치를 내려받을 수 있다"와 "무엇이든 해도 된다"는 다른 말이다
- 같은 계열 안에서도 크기별로 다를 수 있다 → **모델 카드에서 매번 확인**

---

## 15–18분 · 데이터 라이선스와 "라이선스 없음"

| 표시 | SPDX ID | 학습·재배포 조건 |
|---|---|---|
| CC0 | `CC0-1.0` | 조건 없음(출처 기록은 습관) |
| CC BY | `CC-BY-4.0` | 출처 표기 |
| CC BY-SA | `CC-BY-SA-4.0` | 출처 표기 + 파생물 동일 조건 |
| CC BY-NC | `CC-BY-NC-4.0` | 비상업만 |
| 없음 · "연구 전용" | — | 사용 불가, 또는 저작권자에게 문의 |

- 학습 데이터의 조건은 **모델과 서비스까지 따라온다**
- 코드·모델·데이터 세 종류를 한 표에 적는다 → `license_matrix.md`
- SPDX 목록에 없는 라이선스(Llama·Gemma 약관)는 `LicenseRef-이름`으로 적는다

**핵심:** 라이선스 없음 = 사용 불가. 판단이 서지 않으면 쓰지 않는다.

---

## 18–20분 · 실습 인계

[3교시 실습 — 라이선스 판별과 LICENSE 추가](lab.md#3교시-실습--라이선스-판별과-license-추가)

완료 조건:

1. `license_cards_answers.md` 10문항에 판단(가능·조건부·불가)과 근거를 적었다
2. 개인 저장소에 `LICENSE`(MIT 또는 Apache-2.0)와 선택 이유 1문장이 commit·push되었다
3. `license_matrix.md`에 코드·모델·데이터 항목 5개 이상을 SPDX ID와 출처 URL로 채웠다

실습 30분 뒤 휴식 10분. 다음 주는 `week03_reproducible_python`.

---

## 이번 주 정리

```text
1교시: 로컬 commit → push → branch → merge → 충돌은 선택 요청
2교시: Fork → Issue → Branch → PR → Review → Merge
3교시: 저작권 → 라이선스(허락) → permissive / copyleft → 모델·데이터까지
```

공통점은 하나다. **권한이 없는 곳에는 제안으로, 허락이 없는 코드는 쓰지 않는다.**

다음 주 `week03_reproducible_python`: 이 저장소를 uv 기반 재현 가능한 Python 프로젝트로 바꾼다.
