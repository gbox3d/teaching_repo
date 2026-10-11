// ex01 JSON 글자 규칙: 이름과 문자열 값은 큰따옴표("), 마지막 항목 뒤에는 쉼표가 없다
// 11주차 JSON.parse 로 글자를 배열로 바꿔 본다. 규칙을 지킨 글자만 바뀐다. 화면과 Console 을 본다.

const result = document.querySelector('#result');

// 1. 큰따옴표 — 11주차 Application 탭에서 본 글자와 같은 모양이다
const text1 = `[{"title": "자기소개 페이지"}, {"title": "방명록"}]`;
const projects1 = JSON.parse(text1);
console.log('1. 큰따옴표 :', projects1);
result.textContent = `1. ${projects1.length}개 — 첫 제목은 ${projects1[0].title}`;

// 2. 작은따옴표 — 아래 세 줄의 // 를 지우면 빨간 줄이 뜬다. JSON 에는 작은따옴표가 없다
// const text2 = `[{'title': '자기소개 페이지'}, {'title': '방명록'}]`;
// const projects2 = JSON.parse(text2);
// console.log('2. 작은따옴표 :', projects2);

// 3. 마지막 쉼표 — 아래 세 줄의 // 를 지우면 빨간 줄이 뜬다
// const text3 = `[{"title": "자기소개 페이지"}, {"title": "방명록"},]`;
// const projects3 = JSON.parse(text3);
// console.log('3. 마지막 쉼표 :', projects3);

// 바깥의 ` ` 는 JS 의 글자 표시(5주차 템플릿 문자열)다. 그 안쪽이 JSON 글자다.
// JSON 파일(ex02 의 ex02_projects.json)에는 바깥 ` ` 없이 안쪽 글자만 적는다.
