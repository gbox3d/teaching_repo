# 10주차 따라하기

[실습 시간표](lab.md)에 맞춰 필수 부분만 작성한다. 일곱 비교 예제 전체를 새로 만드는 과제가 아니다.

## 수업 전 준비

[10주 제공 폴더](examples/day2/web-week10/) 전체를 새 `web-week10`으로 복사한다. 9주에 수정한 홈·내 정보가 있으면 그 HTML·`app.js`·`styles.css`·이미지를 새 폴더로 옮긴다. 방명록 HTML과 JS는 10주 제공 파일을 사용한다. 9주 타임라인은 최신 글을 먼저 보여 줬다. 이번 시작 파일은 문자열을 등록순으로 표시해 첫 줄부터 배열 인덱스를 대조할 수 있다.

저장소 루트에서 Node.js 24로 실행한다.

```powershell
node web_programming/tools/static-server/server.mjs web_programming/weeks/week10_array_list/examples 8000
```

## 1일차

1. `http://localhost:8000/day1/ex01/`에서 배열 3개와 인덱스 값을 확인한다. app.js의 첫째·셋째 push 문자열을 바꾼다. 더하기는 뒤에 추가하고 초기화는 빈 배열로 바꾼다.
2. `http://localhost:8000/day1/ex02/start.html`을 연다. app.start.js의 TODO 다섯 줄을 다음으로 채운다.

```js
  for (let i = 0; i < items.length; i++) {
    const li = document.createElement('li');
    li.textContent = items[i];
    list.append(li);
  }
```

3. 저장·새로고침한다. 처음 네 값이면 위 목록은 세 줄, 아래 목록은 네 줄이다. `items.push('student04');`를 주석 처리하고 배열을 0·1·3개로 바꾼다. 아래 목록과 배열 개수가 항상 같아야 한다. 위 목록은 비교를 위해 숫자 3을 고정한 코드다.
4. 완료한 다섯 줄을 ex02의 app.js와 비교한다. `i++`는 매 반복 뒤 i를 1 더한다. `items.length`는 개수이므로 마지막 유효 번호는 length−1이다.

ex03은 만들기·글자 넣기·붙이기의 차이를 보여 준다. ex04는 데이터 배열과 DOM을 따로 바꾸므로 둘 중 한 줄을 빠뜨렸을 때 어긋나는 시연이다. 추가 수정은 선택이다.

## 2일차

`http://localhost:8000/day2/web-week10/guestbook.start.html`을 연다. DOM 선택·빈 배열·showList·이벤트·빈칸 안내·시작 호출은 이미 있다.

### 등록 두 줄

`guestbook.start.js` submit 안 TODO 아래 세 줄을 지운다.

```js
  const li = document.createElement('li');
  li.textContent = `${name}: ${message}`;
  list.append(li);
```

같은 자리에 두 줄을 쓴다.

```js
  items.push(`${name}: ${message}`);
  showList();
```

기존 세 줄을 함께 남기면 showList가 그린 뒤 같은 글을 한 번 더 붙인다. `form.reset()`과 `nameInput.focus()`는 유지한다.

### 삭제 두 줄

삭제 버튼의 click 함수 안 TODO 두 줄을 다음으로 바꾼다.

```js
      items.splice(i, 1);
      showList();
```

첫 인자는 0부터 시작하는 위치, 둘째 인자는 삭제할 개수다. showList가 목록을 다시 만들 때 삭제 버튼도 새 인덱스 i를 사용한다. 버튼 생성과 W3.CSS 클래스는 제공 코드다.

### 완성 확인

세 글을 등록하고 가운데 글을 삭제한다. 2개와 첫째·셋째 글이 남는다. 모두 삭제하면 0개와 빈 안내가 보인다. 다시 세 글을 등록해 가운데를 삭제하고 캡처한다. 완성한 시작 JS를 `guestbook.js`로 복사한 뒤 일반 `guestbook.html`에서도 확인한다.

공백 검사는 JavaScript, 잘못된 이메일 형식은 브라우저 기본 검사다. 이메일은 저장하지 않는다. 새로고침하면 `items = []`부터 다시 실행하므로 글은 사라진다.

## 제공 함수

showList의 흐름은 목록 비우기 → for로 글·버튼 생성 → 개수 표시 → 빈 상태 표시다. `innerHTML`은 빈 문자열로 비울 때만 사용하며 입력은 textContent에 넣는다. 개수와 빈 안내는 for 뒤에서 실행하므로 배열이 0개여도 갱신된다.

[완성 HTML](examples/day2/web-week10/guestbook.html) · [완성 JS](examples/day2/web-week10/guestbook.js) · [시작 JS](examples/day2/web-week10/guestbook.start.js)

## 수업 뒤 업로드

이번 주 폴더에서 기존 Git 절차로 commit·push한다. Pages 배포가 완료되면 공개 주소에서 등록·삭제를 다시 확인한다. localhost 캡처는 수업 내 결과로 인정한다. 공개 페이지를 새로 열면 배열도 새로 생기므로 캡처할 글을 다시 입력한다.
