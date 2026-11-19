[실습 페이지](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week06_dom_events)

# 6주차 실습: 클릭 횟수와 다크 모드

각 차시의 강의·시연 60분 뒤 학생 실습 30분을 진행한다. 파일과 저장소는 수업 전에 준비하고 업로드는 수업 뒤에 한다. 완성 예제 여섯 개의 모든 비교를 직접 수정하는 활동은 선택이다.

## 1일차

| 실습 시간 | 필수 활동 |
|---|---|
| 0~5분 | 개인 ex03의 index.html에서 btn·count ID와 app.js 선택자 대조 |
| 5~20분 | app.start.js에서 준비한 app.js에 아래 여섯 줄 작성 |
| 20~30분 | 세 번 클릭해 3회, 새로고침해 0회 확인. Console 오류와 Elements의 글자 확인 |

시작 파일은 [ex03/app.start.js](examples/day1/ex03/app.start.js)다. 제공된 `const btn` 아래에 다음 여섯 줄을 작성한다. 안쪽 두 줄은 들여쓴다.

```js
const countBox = document.querySelector('#count');
let count = 0;
btn.addEventListener('click', function () {
  count = count + 1;
  countBox.textContent = `클릭 ${count}회`;
});
```

`count`는 리스너 밖에서 한 번 0으로 만든다. 이벤트가 발생할 때마다 1을 더하고 화면에 쓴다. 새로고침하면 스크립트를 다시 실행하므로 0회다. 별도 초기화 버튼은 만들지 않는다.

강의자는 완성 [app.js](examples/day1/ex03/app.js)의 inside와 count 로그를 비교한다. 학생은 이 비교 코드까지 다시 작성하지 않는다. ex01의 잘못된 ID, ex02의 리스너 밖 대입도 강의자 오류 시연이며 확인 뒤 원본으로 복구한다.

## 2일차

| 실습 시간 | 필수 활동 |
|---|---|
| 0~5분 | 개인 홈 styles.css의 다크 배경·글자색 두 값 변경 |
| 5~15분 | 제공 app.js의 TODO 세 곳에 toggle과 countUp 호출 연결 |
| 15~25분 | 인사·다크·인사 순서로 클릭, 375/1280px와 새로고침 확인 |
| 25~30분 | 다크 모드와 클릭 1회 이상이 보이는 캡처 한 장 |

개인 홈은 [web-week06/app.start.js](examples/day2/web-week06/app.start.js)를 수업 전에 app.js로 준비한 사본이다. HTML·요소 선택·greet·hello·countUp과 리스너 틀은 제공되므로 지우지 않는다. 기존 개인 소개·취미·이미지도 유지한다.

CSS의 `body.dark, body.dark .card`에서 배경을 `#222222`에서 `#202938`, 글자를 `#eeeeee`에서 `#f5f7ff`로 바꿔 본다. 제목·메뉴의 `#a7c5ff`, 푸터의 `#c8d4eb` 규칙은 제공한다. h1·h2·nav a·footer에는 밝은 모드의 별도 color가 있어 body의 color만으로 덮어쓰이지 않는다. 어두운 모드용 선택자를 함께 확인한다.

인사 버튼 리스너에는 다음 한 줄을 넣는다.

```js
countUp();
```

다크 버튼 리스너에는 다음 두 줄을 넣는다.

```js
document.body.classList.toggle('dark');
countUp();
```

인사·다크·인사 순서로 누르면 클릭 3회이며 인사 문장이 바뀌고 어두운 화면이 된다. 다크 버튼을 다시 누르면 4회와 밝은 화면이다. 새로고침하면 0회·밝은 화면·초기 인사다. 다시 다크 버튼을 눌러 캡처한다. 375px에서 메뉴가 세로이고 두 폭에서 버튼·제목·메뉴·푸터를 읽을 수 있는지 확인한다.

## 막혔을 때

| 증상 | 확인과 복구 |
|---|---|
| textContent 또는 addEventListener에서 null 오류 | HTML ID와 querySelector 철자, script의 defer 확인 |
| 횟수가 항상 1회 | let count를 리스너 밖에 두었는지 확인 |
| 횟수가 안 늘지만 오류가 없음 | TODO가 남았거나 countUp;에서 호출 괄호가 빠졌는지 확인 |
| Assignment to constant variable | 누적 변수 count는 let으로 선언 |
| class는 붙는데 색이 그대로 | CSS 연결과 body.dark 규칙, 파일 저장 확인 |
| 카드·제목·메뉴·푸터만 밝은 모드 색 | 해당 요소의 body.dark 선택자 확인 |
| 초기화하면 횟수·다크 모드가 사라짐 | 정상이다. 이번 주에는 저장하지 않는다 |
| Pages 반영 지연 | 로컬 캡처와 Commits 기록으로 확인, 수업 뒤 재확인 |

## 수업 뒤 업로드

사전에 준비한 개인 저장소 web-week06에서 다음 명령을 실행한다. 저장소와 remote 설정은 [2주차 안내](../week02_github_pages/lab.md)를 따른다.

```bash
git add .
git commit -m "6주차 DOM과 이벤트"
git push
```

공개 주소 `https://student01.github.io/web-week06/`에서 다시 확인한다. 수업 중 제출은 주소창이 보이는 로컬 또는 파일 화면 한 장이다. 공개 파일과 캡처에는 별칭·가상 이메일을 사용한다. 공용 PC의 로그인 자격 증명은 수업 뒤 정리한다.

## 선택 연습

ex01~ex06 README의 비교를 한 곳씩 수정하고 복구한다. ex03의 count를 함수 안으로 옮기거나 ex06의 countUp 호출 괄호를 빼서 차이를 비교할 수 있다. 추가 메뉴 접기나 다크 모드 저장은 필수 실습과 평가에 넣지 않는다.
