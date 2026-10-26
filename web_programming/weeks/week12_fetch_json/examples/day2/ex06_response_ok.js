// ex06 response.ok: 파일이 없어도 서버는 답(404)을 보낸다. 그래서 읽기 전에 정상인지 response.ok 로 묻는다
// 처음에는 1번 줄이 켜져 있다. 1번을 주석으로, 2번을 주석 밖으로 바꿔 저장 → 새로고침한다.

const notice = document.querySelector('#notice');
const result = document.querySelector('#result');
const fileName = 'ex06_projects.json';      // 1. 있는 파일 → Status 200, ok 는 true
// const fileName = 'ex06_project.json';    // 2. s 가 빠진 이름(없는 파일) → Status 404, ok 는 false

async function loadProjects() {
    const response = await fetch(fileName);                       // ex02
    console.log(`${fileName} → status ${response.status}, ok ${response.ok}`);
    if (!response.ok) {                     // !response.ok 는 response.ok === false 와 같다
        notice.textContent = '프로젝트를 불러오지 못했습니다.';
        return;                             // 여기서 끝낸다(7주차 if 안의 return). 아래 json() 으로 가지 않는다
    }
    const projects = await response.json();
    notice.textContent = '';                // 정상이면 '불러오는 중' 을 지운다
    result.textContent = `${projects.length}개를 불러왔다`;
}

loadProjects();
