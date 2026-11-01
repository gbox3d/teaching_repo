# student01의 웹 연습장

웹프로그래밍 수업에서 한 주씩 늘려 가는 **자기소개 사이트**입니다.

## 공개 주소

- [https://student01.github.io/web-week09/](https://student01.github.io/web-week09/)

## 페이지

| 페이지 | 파일 | 내용 |
|---|---|---|
| 홈 | [index.html](index.html) | 인사말, 소개, 취미 목록 |
| 내 정보 | [about.html](about.html) | 아이디·이메일·관심 분야 표 |
| 방명록 | [guestbook.html](guestbook.html) | 이름·메시지 폼 |

![세 페이지가 메뉴로 서로 이어진 사이트 구조](images/site-map.svg)

## 기능

- 홈의 "인사 바꾸기"와 "다크 모드" 버튼을 누르면 문장과 배경색이 바뀌고 클릭 횟수가 1씩 오릅니다.
- 방명록에서 이름과 메시지를 적고 "남기기"를 누르면 아래에 한 줄로 보입니다. 빈칸이면 안내 문장이 나옵니다.

다크 모드 버튼은 `body` 에 class 하나를 붙였다 뗍니다.

```js
darkButton.addEventListener('click', function () {
  document.body.classList.toggle('dark');
  countUp();
});
```

## 화면

![인사 바꾸기를 누른 홈 화면](screenshots/home.png)

![글을 남긴 방명록 화면](screenshots/guestbook.png)

## 이번에 배운 것

- HTML 뼈대와 nav로 세 페이지를 이어 놓는 법
- CSS로 색·박스·flex·화면 폭에 따른 배치를 정하는 법
- 버튼 클릭과 폼 제출을 자바스크립트로 받아 화면을 바꾸는 법
