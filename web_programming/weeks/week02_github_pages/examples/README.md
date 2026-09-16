# 2주차 예제 — GitHub에 올리는 세 파일과 소개 페이지

1주차 예제와 같은 구조의 작은 페이지다. 아래 파일은 해당 날짜의 **완성본**이다.
먼저 [따라하기](../walkthrough.md)를 순서대로 하고, 막히면 내 파일과 한 줄씩 비교한다.
`student01`은 연습용 아이디다. 본인 아이디로 바꿔 쓴다.

## 파일과 단계

| 예제 파일 | 따라하기 단계 | 내 `my-web` 폴더의 파일 |
|---|---|---|
| [day1/index.html](day1/index.html) | [2단계](../walkthrough.md#2-세-파일-만들기)에서 `<h1>내 첫 페이지</h1>`로 만들고, [8단계](../walkthrough.md#8-제목-한-줄-고치고-push-하기)에서 이 파일과 같아진다 | `index.html` |
| [day1/styles.css](day1/styles.css) | [2단계](../walkthrough.md#2-세-파일-만들기) | `styles.css` |
| [day1/app.js](day1/app.js) | [2단계](../walkthrough.md#2-세-파일-만들기) | `app.js` |
| [day2/about.html](day2/about.html) | [12단계](../walkthrough.md#12-abouthtml-추가하고-링크-넣기) — about 브랜치에서 새로 만든다 | `about.html` |
| [day2/index.html](day2/index.html) | [12단계](../walkthrough.md#12-abouthtml-추가하고-링크-넣기) — day1에 링크 한 줄이 추가된다 | `index.html` |
| [day2/styles.css](day2/styles.css) · [day2/app.js](day2/app.js) | day1과 같다. 2일차에는 고치지 않는다 | `styles.css` · `app.js` |

## 1. 1일차 완성 — 내 첫 GitHub 페이지

`day1/` 세 파일을 `my-web` 폴더에 두고 `index.html`을 브라우저로 열면 카드 한 장이 보인다.

```text
Week 02 · GitHub Pages
내 첫 GitHub 페이지
내 컴퓨터에서 만든 페이지를 GitHub에 올려 공개합니다.
[방문 버튼] 클릭 횟수: 0
```

- `index.html`: 제목 `<h1>`, 문장 `<p>`, 버튼과 `<p id="status">`. `styles.css`와 `app.js`를 연결한다.
- `styles.css`: 카드 모양과 버튼 색. 1주차 예제를 조금 줄인 것이다.
- `app.js`: 버튼을 누를 때마다 `클릭 횟수`를 1씩 올린다. 1주차와 같다.

GitHub Pages로 공개하면 같은 화면이 `https://student01.github.io/my-web/`에서 열린다.

## 2. 2일차 완성 — 소개 페이지

`day2/`는 day1에 `about.html`이 추가되고, `index.html`에 링크 한 줄이 늘어난 것이다.

```html
<p><a href="about.html">소개 페이지 보기</a></p>
```

- `about.html`은 `styles.css`만 연결하고 `app.js`는 연결하지 않는다. 버튼이 없기 때문이다.
- `<a href="index.html">`로 첫 페이지로 돌아간다. 두 파일이 같은 폴더에 있으므로 파일 이름만 적는다.
- 공개 주소는 `https://student01.github.io/my-web/about.html`이다.

```text
Week 02 · about 브랜치
소개
student01의 웹프로그래밍 연습 페이지입니다.
첫 페이지로 돌아가기
```

## 3. 브랜치와 파일

| 브랜치 | 있는 파일 |
|---|---|
| `main` (merge 전) | index.html · styles.css · app.js |
| `about` | index.html(링크 추가) · about.html · styles.css · app.js |
| `main` (merge 후) | about과 같다 |

`git switch main`을 하면 폴더에서 `about.html`이 사라지고, `git merge about` 뒤에 돌아온다.
파일이 지워진 것이 아니라 about 브랜치의 commit에 들어 있는 것이다.

## 공식 참고 자료

- [GitHub Pages 사이트 만들기 — GitHub Docs](https://docs.github.com/ko/pages/getting-started-with-github-pages/creating-a-github-pages-site)
- [리포지토리의 브랜치 보기 — GitHub Docs](https://docs.github.com/ko/repositories/configuring-branches-and-merges-in-your-repository/managing-branches-in-your-repository/viewing-branches-in-your-repository)
