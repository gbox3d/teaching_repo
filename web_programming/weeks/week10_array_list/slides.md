---
marp: true
theme: default
paginate: true
header: "웹프로그래밍 · 10주차"
footer: "Arrays · for · showList · splice"
---

# 배열 데이터를 목록으로 그리기

7·9주는 작성자·시각·본문을 최신순으로 표시했다.

10주 시작 파일은 `이름: 메시지`를 등록순으로 그린다. 첫 줄이 `items[0]`이다.

- 배열: push·length·인덱스
- 반복: 고전 for
- 화면: showList
- 삭제: splice(i, 1)

DOM만으로 삭제할 수도 있다. 이번 수업은 배열과 화면의 관계를 배우는 방식이다.

---

# 1일차 — 강의 60분·실습 30분

| 강의·시연 | 분 |
|---|---:|
| 준비 확인 | 5 |
| 배열·push·length | 20 |
| 인덱스·for | 20 |
| li·textContent·append | 10 |
| 실습 안내 | 5 |

필수 작성은 ex01 문자열 두 값과 ex02 시작 틀 다섯 줄이다.
파일·저장소는 수업 전에 준비하고 업로드는 수업 뒤에 한다.

---

## 배열·push·length — 5~25분

[ex01](examples/day1/ex01/index.html) · [코드](examples/day1/ex01/app.js)

```js
let items = [];
items.push('student01: 안녕하세요');
items.push('student02: 고맙습니다');
items.push('student03: 반갑습니다');
```

화면에서 length 3과 items[0]·items[2]를 확인한다.
items[3]은 없는 번호이므로 undefined다.
더하기로 값을 추가하고 초기화로 빈 배열을 비교한다.

출력 함수와 JSON.stringify는 제공 코드다.

---

## 고전 for — 25~45분

[ex02 완성](examples/day1/ex02/index.html) · [시작](examples/day1/ex02/start.html)

```js
for (let i = 0; i < items.length; i++) {
  const li = document.createElement('li');
  li.textContent = items[i];
  list.append(li);
}
```

시작 0 → length 전까지 → i를 1 증가한다.
배열이 0개면 반복 본문을 실행하지 않는다.
숫자 3으로 고정한 위 목록과 length를 쓰는 아래 목록을 비교한다.

---

## 요소 생성과 붙이기 — 45~55분

[ex03](examples/day1/ex03/index.html)

```js
const li2 = document.createElement('li');
li2.textContent = '2. 만들고 붙인 줄';
list.append(li2);
```

만들기만 한 li1은 처음 화면에 없다.
첫 요소 붙이기를 누르면 맨 뒤에 나타난다.
같은 li1을 다시 붙여도 복제되지 않고 총 세 줄을 유지한다.

---

## 배열과 DOM을 각각 갱신

[ex04](examples/day1/ex04/index.html), 강의자 시연

```js
items.push(text);
const li = document.createElement('li');
li.textContent = text;
list.append(li);
count.textContent = `${items.length}개`;
```

push만 생략하면 줄은 늘고 개수는 0이다.
append만 생략하면 개수만 늘고 줄은 없다.
이번 예제의 빈 문자열도 배열 값 하나다.

---

## 메모리·브라우저 저장·서버

| 위치 | 수업 | 새로고침 뒤 |
|---|---|---|
| JavaScript 배열 | 10주 | 초기 배열로 복귀 |
| localStorage | 11주 | 같은 출처의 값 유지 |
| 공용 서버 | 12~14주 | GET으로 다시 조회 |

11주 필수는 문자열·JSON·폼 저장이다. 전체 저장 방명록은 제공 시연본이다.
Supabase 서버 구축은 [별도 특강](../../specials/supabase_guestbook/README.md)이다.

---

## 1일차 필수 실습 — 30분

[실습지](lab.md#1일차) · [따라하기](walkthrough.md#1일차)

1. ex01 push 문자열 두 값 변경: 5분
2. ex02 app.start.js의 for·본문 다섯 줄: 15분
3. push 줄을 주석 처리하고 배열 0·1·3개 비교: 10분

아래 목록과 배열 개수가 일치하면 완료다.
위 목록은 숫자 3으로 반복하므로 항상 세 줄이다.
ex03·04 코드 변경은 선택이다.

---

# 2일차 — 강의 60분·실습 30분

| 강의·시연 | 분 |
|---|---:|
| 준비 확인 | 5 |
| showList | 15 |
| 비우고 그리기 | 15 |
| 삭제 버튼 틀 | 15 |
| 폼 인계 | 5 |
| 실습 안내 | 5 |

필수 작성은 제공 시작 틀의 등록 두 줄·삭제 두 줄이다.

---

## showList — 5~20분

[ex06](examples/day2/ex06/index.html)

```text
목록 비우기
  → 배열 길이만큼 li 생성·append
  → 배열 개수 표시
  → 0개이면 빈 안내
```

열 때 한 번, 배열을 바꾼 뒤 한 번 호출한다.
개수와 빈 안내는 for 밖에 둔다.
배열이 비어도 0개를 표시해야 하기 때문이다.

---

## 비우고 그리기 — 20~35분

[ex05](examples/day2/ex05/index.html)

```js
list.innerHTML = '';
for (let i = 0; i < items.length; i++) {
  const li = document.createElement('li');
  li.textContent = items[i];
  list.append(li);
}
```

1번 버튼은 3→6→9줄, 2번 버튼은 반복해도 3줄이다.
입력은 textContent에 넣고 innerHTML은 비우기에만 사용한다.

---

## 삭제 버튼 틀 — 35~50분

[ex07](examples/day2/ex07/index.html)

```js
removeButton.addEventListener('click', function () {
  items.splice(i, 1);
  showList();
});
```

버튼 생성·스타일·이벤트 틀은 제공한다.
학생은 배열에서 하나를 빼고 다시 그리는 두 줄을 작성한다.
다시 그리면 각 버튼이 새 위치 i를 사용한다.
가운데 삭제 뒤 첫째·셋째 글과 2개가 남아야 한다.

---

## 폼 인계 — 50~55분

[방명록 시작](examples/day2/web-week10/guestbook.start.html)

10주 시작 JS의 submit에서 li를 붙이는 세 줄을 다음 두 줄로 교체한다.

```js
items.push(`${name}: ${message}`);
showList();
```

HTML·폼 검증·showList·시작 호출은 제공 코드다.
기존 append 세 줄을 남기면 같은 글을 한 번 더 붙인다.
이메일은 브라우저 기본 형식 검사만 하고 배열에 저장하지 않는다.

---

## 2일차 필수 실습 — 30분

[실습지](lab.md#2일차) · [따라하기](walkthrough.md#2일차)

1. 등록 세 줄을 두 줄로 교체: 10분
2. 삭제 TODO 두 줄 완성: 8분
3. 3개 등록 → 가운데 삭제 → 전부 삭제: 7분
4. 다시 3개 등록·가운데 삭제 후 캡처: 5분

완료한 guestbook.start.js를 guestbook.js에 복사하여 일반 페이지도 확인한다.
ex05~07의 추가 변형은 선택이다.

---

## 제출과 동작 확인

localhost 주소창·남은 두 글·삭제 버튼·2개가 보이는 캡처 한 장.

- 빈 이름·메시지 차단, 잘못된 이메일 형식 차단
- 태그 모양 문자열은 텍스트로 표시
- 375px·1280px에서 긴 글과 버튼 확인
- 새로고침하면 빈 배열·0개

수업 뒤 commit·push와 Pages 확인을 한다. 배포 지연으로 수업 내 캡처를 미루지 않는다.

---

## 다음 주와 선택 보강

11주에는 객체 필드를 읽고 문자열→JSON→폼 저장·불러오기를 실습한다.
전체 저장 방명록은 제공 시연본이며 학생 필수 구현과 구분한다.
localhost에서도 저장·복원을 확인하고 캡처할 수 있다.

[배열 심화](../../specials/array_advanced/README.md)의 forEach·filter·map·reduce는 별도 보강 수업이다.
SPA 직접 전환은 14주 이후 선택 특강이다.
