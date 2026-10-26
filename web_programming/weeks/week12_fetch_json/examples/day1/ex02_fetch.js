// ex02 fetch 로 JSON 파일 읽기: 파일을 요청해 응답을 받고(await fetch), 응답의 글자를 배열로 바꾼다(await response.json())
// 서버 주소(http://localhost:8000/ex/)에서 연다. 화면, Console 1·2번, F12 › Network 의 ex02_projects.json 줄을 본다.

const result = document.querySelector('#result');

async function loadProjects() {                              // async 를 붙인 함수 안에서만 await 를 쓸 수 있다
    const response = await fetch('ex02_projects.json');      // 1. 이 파일을 요청하고 응답이 올 때까지 기다린다
    console.log('1. response :', response);
    const projects = await response.json();                  // 2. 응답의 글자를 배열로 바꾼다. 여기서도 기다린다
    console.log('2. projects :', projects);
    result.textContent = `2. ${projects.length}개를 불러왔다 — 첫 제목은 ${projects[0].title}`;
}

loadProjects();                                              // 만든 함수는 불러야 실행된다(5주차 ex08)
