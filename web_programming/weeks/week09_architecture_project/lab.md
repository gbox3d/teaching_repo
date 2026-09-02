# 9주차 실습 — 설계에서 walking skeleton까지

## 1일차 60분 — 문제·데이터·상태 설계

### 문제

14주차까지 완성할 개인 프로젝트의 핵심 흐름을 한 페이지 설계로 만든다. 기능을 많이 적는 대신, 사용자·데이터·권한·실패를 검증 가능한 문장으로 연결한다.

### 시간 상자

| 시간 | 활동 | 산출물 |
|---:|---|---|
| 0–8분 | 문제/사용자/Must | 각 한 문장 |
| 8–20분 | 사용자 이야기 | 정상 2 + 경계 1 |
| 20–32분 | entity와 관계 | field/owner 표 |
| 32–43분 | 실행 위치 결정 | architecture diagram |
| 43–53분 | 여섯 UI 상태 | 조건/표시/회복/검증 |
| 53–60분 | 동료 설명·수정 | 결정 1개 개선 |

### 필수 산출물

#### 1. 문제 문장

```text
[핵심 사용자]가 [상황]에서 [문제]를 해결하도록 [핵심 행동]을 제공한다.
```

#### 2. 사용자 이야기와 acceptance scenario

```text
사용자로서 [목적]을 위해 [행동]하고 싶다.
Given [상태], When [행동], Then [관찰 결과].
```

정상 둘, validation/unauthorized/empty 중 하나를 포함한다.

#### 3. 데이터 표

| entity | 핵심 field | owner | 읽기 | 쓰기 | 관계 |
|---|---|---|---|---|---|
| 예: Post | id, title, body | user | 공개 | owner | Comment |

#### 4. architecture diagram

GitHub Pages browser, static asset, Supabase, 선택적 server를 실제 사용 여부에 맞게 그린다. 화살표에는 `Post[]`, session 같은 데이터 이름을 쓴다.

#### 5. 상태표

loading, empty, validation, unauthorized, not-found, network error의 발생 조건·화면·회복 행동·검증 방법을 모두 적는다.

### 단계별 힌트

**힌트 1:** 화면이 아니라 사용자 행동 하나로 범위를 줄인다. “게시판”보다 “내 글 한 개를 작성하고 다시 수정한다”가 검증 가능하다.

**힌트 2:** field마다 공개돼도 되는지 묻는다. password, secret, 관리자 메모는 public entity에 두지 않는다.

**힌트 3:** 선택적 server가 없다면 diagram에서 제거한다. 장래 기능을 위해 빈 상자를 남기지 않는다.

### 검증

- [ ] Must가 한 학기 남은 기간에 구현 가능한가?
- [ ] 모든 변경 가능한 핵심 row에 owner가 정의됐는가?
- [ ] 관계 기능 하나가 두 entity의 key로 설명되는가?
- [ ] public과 secret 경계가 diagram에 표시됐는가?
- [ ] 여섯 상태에 서로 다른 회복 행동이 있는가?
- [ ] 동료가 1분 안에 핵심 흐름을 다시 설명할 수 있는가?

## 2일차 60분 — 실행 가능한 walking skeleton

### 문제

[project starter](examples/project-starter/)를 복사해 자신의 핵심 entity 모양으로 바꾸고, mock data를 읽어 loading·success·empty·error를 표시한다. 다음 주 data source를 Supabase로 교체할 수 있도록 UI에서 저장 위치를 분리한다.

### 시간 상자

| 시간 | 활동 | 검증 |
|---:|---|---|
| 0–8분 | starter 복사·첫 commit | 로컬 실행 |
| 8–20분 | mock entity/contract | JSON과 함수 반환 |
| 20–35분 | 핵심 목록 render | loading/success |
| 35–44분 | empty/error | fixture·없는 경로 |
| 44–52분 | architecture 문서 동기화 | 코드 파일과 화살표 |
| 52–60분 | Pages/발표 리허설 | URL·3분 |

### 필수 요구사항

- `data-source.js`만 데이터 위치와 fetch를 안다.
- UI가 받는 entity의 field와 의미를 문서에 적는다.
- 사용자 문자열은 `textContent`로 출력한다.
- loading·success·empty·error 중 현재 상태 하나만 보인다.
- mock JSON을 빈 배열로 바꿔 empty를 재현한다.
- 잘못된 URL로 error를 재현하고 원인을 Console에 남긴다.
- 자신의 architecture 문서가 실제 파일/요청 방향과 일치한다.
- 공개 URL 또는 재현 가능한 로컬 실행 명령을 제공한다.

### 단계별 힌트

**힌트 1:** 먼저 mock JSON field를 자신의 entity에 맞게 바꾸고 `listItems()`의 반환 예를 문서에 붙인다.

**힌트 2:** `main.js`에는 source URL 대신 `listItems()` 호출만 남긴다.

**힌트 3:** data source 교체 가능성은 interface를 하나 더 만드는 것이 아니라, UI가 fetch 세부사항을 import하지 않는 것으로 충분하다.

### 검증

- [ ] Network에서 HTML → JS modules → JSON 요청을 추적했다.
- [ ] JSON 2행과 화면 2개가 id를 유지한다.
- [ ] 빈 배열에서 이전 카드가 남지 않는다.
- [ ] 404 뒤 재시도 가능한 화면이 남는다.
- [ ] 새 탭에서 공개 URL을 열어 상대 경로를 확인했다.
- [ ] secret/service-role/password 문자열이 저장소에 없다.

## 제출

[1차 과제 안내](project_brief.md)와 [rubric](rubric.md)에 따라 발표 자료와 보고서를 제출한다.

## 확장 주제

1. static JSON과 Supabase를 같은 data contract로 전환하는 adapter 비교
2. Mermaid diagram에 정상·오류 응답을 나눈 sequence diagram 추가
3. optimistic UI가 필요한 동작과 rollback 설계
4. 이미지 저작권·출처·대체 텍스트를 asset inventory에 기록
5. Deno/Edge Function이 필요한 secret 또는 계산 경계 제안
