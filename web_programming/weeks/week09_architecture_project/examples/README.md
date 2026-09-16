# 9주차 예제 — 발표할 사이트와 README 1차판

7주차 `my-web`에서 이어지는 파일이다. 아래 파일은 해당 날짜 끝의 **`my-web` 전체 파일**이다.
8주차 `exam/` 폴더는 본시험 답안이라 예제에 싣지 않는다.
이번 주에는 HTML·CSS·JavaScript를 고치지 않는다. 늘어나는 것은 `README.md`와 `screenshots/` 폴더 두 가지다.
먼저 [따라하기](../walkthrough.md)를 순서대로 하고, 막히면 내 파일과 한 줄씩 비교한다.
`student01`은 연습용 아이디다. 본인 아이디로 바꿔 쓴다.

## 파일과 단계

| 예제 파일 | 따라하기 단계 | 내 `my-web` 폴더의 파일 |
|---|---|---|
| [day1/screenshots/home.png](day1/screenshots/home.png) · [day1/screenshots/guestbook.png](day1/screenshots/guestbook.png) | [5단계](../walkthrough.md#5-화면-두-장-캡처해-screenshots-폴더에-넣기) — 내 화면을 직접 찍어 넣는다 | `screenshots/home.png` · `screenshots/guestbook.png` |
| [day1/README.md](day1/README.md) | [6단계](../walkthrough.md#6-readme-1차판-쓰기) — 저장소 루트에 새로 만든다 | `README.md` |
| [day1/index.html](day1/index.html) · [day1/styles.css](day1/styles.css) · [day1/app.js](day1/app.js) | [3단계](../walkthrough.md#3-홈-화면-세-파일-확인하기) — 열어서 동작만 확인한다. 고치지 않는다 | `index.html` · `styles.css` · `app.js` |
| [day1/about.html](day1/about.html) · [day1/guestbook.html](day1/guestbook.html) · [day1/guestbook.js](day1/guestbook.js) | [4단계](../walkthrough.md#4-내-정보와-방명록-확인하기) — 열어서 동작만 확인한다 | `about.html` · `guestbook.html` · `guestbook.js` |
| [day2/](day2/)의 모든 파일 | day1과 같다. 2일차는 발표뿐이라 파일이 바뀌지 않는다 | 그대로 |

`day1/images/profile.png`와 `day2/images/profile.png`는 3주차에 넣은 그림 그대로다.
7주차에 GitHub 웹에서 만든 8줄짜리 `README.md`는 이번 주에 **지우고 1차판으로 다시 쓴다.**

## 1. 발표에서 보여 줄 화면

`day1/index.html`을 브라우저로 열고 **[인사 바꾸기]**를 한 번 누르면 아래와 같다. 이 화면이 캡처 1이다.

```text
student01의 웹 연습장
홈  내 정보  방명록
반갑습니다. 오늘도 좋은 하루 되세요.     ← 버튼을 눌러 바뀐 문장
[인사 바꾸기] [다크 모드]
클릭 1회                                 ← 눌러 본 것이 보인다
소개 · 프로필 그림 · 취미 세 줄
```

`day1/guestbook.html`에서 이름과 메시지를 넣고 **[남기기]**를 누르면 아래와 같다. 이 화면이 캡처 2다.

```text
방명록
한 줄 남기기 · 쓰는 순서 3줄
[이름] [이메일] [메시지] [남기기]
마지막으로 남긴 글
student01: 첫 방명록입니다.              ← 제출 뒤에 보이는 한 줄
```

- 두 캡처 모두 **동작한 뒤의 화면**이다. `클릭 0회`나 `아직 남긴 글이 없습니다.`인 채로 찍지 않는다.
- 이메일 칸은 비워 두어도 된다. 빈값 안내는 이름과 메시지 두 칸에만 있다.
- 새로고침하면 두 화면 모두 처음 상태로 돌아간다. 오늘 글은 화면에만 있기 때문이다.

## 2. README 1차판 5항목

`day1/README.md`가 1차판 예시다. 29줄이고 마크다운은 세 가지만 썼다.

```markdown
# my-web — student01의 웹 연습장

## 공개 주소

- [https://student01.github.io/my-web/](https://student01.github.io/my-web/)
```

| 항목 | 쓰는 것 | 점수 |
|---|---|---:|
| `# 제목` | 사이트 이름 한 줄 | 레포트 5점에 포함 |
| `## 공개 주소` | Pages 주소 링크 | 1 |
| `## 페이지` | 세 페이지와 한 줄 설명 | 1 |
| `## 기능` | 버튼과 폼, 두 줄 | 1 |
| `## 화면` | `screenshots/` 캡처 2장 링크 | 1 |
| `## 이번에 배운 것` | 3줄 | 1 |

- 같은 저장소 안의 파일은 소괄호에 `index.html`이나 `screenshots/home.png`처럼 **파일 이름만** 적는다.
- 굵게(`**`)나 이미지 문법(`![]()`)은 이번 주에 쓰지 않는다. 세 가지로 충분하다.
- 캡처를 링크로 걸면 GitHub에서 눌러 열 수 있다. 화면에 그림으로 띄우는 문법은 13주차에 쓴다.

## 3. 두 날의 파일 비교

| | 7주차 끝 | 9주차 1일차 끝 | 9주차 2일차 끝 |
|---|---|---|---|
| 세 페이지·CSS·JS | 있음 | 같음 (고치지 않음) | 같음 |
| `README.md` | GitHub 웹에서 만든 8줄 | **1차판 29줄** | 같음 |
| `screenshots/` | 없음 | **캡처 2장** | 같음 |

`day2/`는 `day1/`과 파일이 모두 같다. 2일차는 발표만 하므로 `my-web`에 바뀌는 파일이 없다.
13주차에 README를 최종판으로 다시 쓰고 캡처가 3장으로 늘어난다.

## 공식 참고 자료

- [README 정보 — GitHub Docs](https://docs.github.com/ko/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes)
- [기본 쓰기 및 서식 지정 구문 — GitHub Docs](https://docs.github.com/ko/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax)
- [리포지토리 내에서 분기 관리(브랜치 삭제) — GitHub Docs](https://docs.github.com/ko/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-and-deleting-branches-within-your-repository)
