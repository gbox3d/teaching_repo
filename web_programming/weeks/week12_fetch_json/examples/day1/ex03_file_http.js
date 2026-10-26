// ex03 file:// 과 http://: 같은 코드도 두 번 눌러 연 페이지(file://)에서는 fetch 가 막힌다
// 서버 주소(http://localhost:8000/ex/)로 한 번, 탐색기에서 index.html 을 두 번 눌러(file:///…) 한 번 열고 화면과 Console 을 비교한다.

const result = document.querySelector('#result');
result.textContent = '1. 불러오는 중 — 이 글자가 그대로면 2번(fetch 줄)에서 멈춘 것이다';   // 1. 어느 주소로 열어도 실행된다

async function loadProjects() {
    const response = await fetch('ex03_projects.json');      // 2. file:// 에서는 여기서 멈추고 빨간 줄이 뜬다
    const projects = await response.json();
    result.textContent = `3. ${projects.length}개를 불러왔다`;  // 3. 서버 주소에서만 여기까지 온다
}

loadProjects();
