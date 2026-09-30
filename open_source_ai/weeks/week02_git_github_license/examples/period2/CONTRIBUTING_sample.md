# 기여 안내 (CONTRIBUTING 예시)

이 문서는 개인·팀 저장소에 넣을 `CONTRIBUTING.md`의 예시다. 저장소 이름과 branch 규칙을 자기 프로젝트에 맞게 고쳐 쓴다. 9주차 팀 저장소 템플릿에서 다시 사용한다.

## 시작 전에

- 변경을 제안하려면 코드를 쓰기 전에 **Issue를 먼저 연다**. "제안(proposal)" 템플릿을 사용한다.
- 관리자가 Issue에 답하면 그때 branch를 만든다. 답이 없으면 하루 뒤 Issue에 한 줄 더 남긴다.
- 오타·링크 수정처럼 한 줄짜리 변경은 Issue 없이 PR을 바로 열어도 된다.

## 작업 흐름

1. 저장소를 fork하고 fork를 clone한다.
2. `main`에서 새 branch를 만든다. 이름은 `종류/주제` 형식이다.
   - `feature/run-guide` — 기능·문서 추가
   - `fix/readme-typo` — 잘못된 것 수정
   - `docs/license-matrix` — 문서만 변경
3. 작은 단위로 commit하고 fork에 push한다.
4. 원본 저장소의 `main`을 base로 Pull Request를 연다. PR 템플릿의 모든 항목을 채운다.

## 커밋 메시지

```text
Add run instructions to README

New members could not find how to start the tool.
Related to #3
```

- 제목은 명령형 동사로 시작하고 50자 안팎, 마침표 없음.
- 제목과 본문 사이에 빈 줄 하나.
- 본문에는 무엇이 아니라 **왜**를 쓴다. 관련 Issue 번호를 적는다.
- `update`, `fix`, `final` 같은 제목은 받지 않는다.

## Pull Request 규칙

- PR 하나에 의도 하나. 리뷰어가 10분 안에 읽을 수 있는 크기(대략 200줄 이하)로 나눈다.
- 방향을 먼저 묻고 싶으면 **Draft PR**로 연다. Draft는 merge 대상이 아니다.
- PR 본문의 `Closes #번호`로 Issue를 연결한다.
- 리뷰 요청을 받으면 반박 대신 **수정 commit**으로 답한다. 동의하지 않으면 근거를 코멘트로 적는다.
- 비밀번호·토큰·개인정보가 들어간 PR은 즉시 닫고, 이미 push된 값은 무효화(회전)한다.

## 리뷰

- 리뷰는 코드와 근거에 대해 한다. 사람에 대해 하지 않는다.
- 요청은 "무엇을, 왜, 어떻게"가 있게 쓴다. 예: "이 명령은 현재 폴더를 확인하지 않는다. 앞에 `git status` 한 줄을 넣으면 실습자가 위치를 놓치지 않는다."
- 좋은 점도 한 줄 적는다.
- Approve, Comment, Request changes 중 하나를 근거와 함께 남긴다.
- 관리자는 영업일 기준 2일 안에 첫 응답을 목표로 한다(수업 중에는 같은 교시 안).

## 기여물의 라이선스

이 저장소에 PR로 보낸 기여물은 저장소의 `LICENSE`와 같은 조건으로 배포된다는 데 동의한 것으로 본다. 다른 사람의 코드·모델·데이터를 가져올 때는 라이선스와 출처를 PR 본문과 `license_matrix.md`에 적는다. 라이선스가 없는 자료는 가져오지 않는다.

## 행동 강령

참여자는 서로를 존중한다. 팀 저장소에서는 Contributor Covenant를 행동 강령으로 채택한다(9주차에서 다룬다).

## 문의

질문은 Issue로 남긴다. 이메일·전화번호 같은 개인 연락처는 이 문서에 적지 않는다.
