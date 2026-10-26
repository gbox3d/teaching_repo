// ex05 try / catch: try 안에서 오류가 나면 페이지가 멈추지 않고 catch 로 넘어간다
// 서버 주소로 열면 1번(try 끝까지), 두 번 눌러 열면(file://) 2번(catch)이 화면에 보인다.

const notice = document.querySelector('#notice');

async function loadProjects() {
    try {
        const response = await fetch('ex05_projects.json');   // ex02. file:// 에서는 여기서 오류(ex03)
        const projects = await response.json();
        notice.textContent = `1. try: ${projects.length}개를 불러왔다`;   // 1. 오류가 없으면 try 끝까지
        console.log('1. try 를 끝까지 실행했다');
    } catch (error) {
        notice.textContent = '2. catch: 프로젝트를 불러오지 못했습니다.';   // 2. 오류가 나면 catch 로
        console.log('2. catch 가 받은 오류 :', error);
    }
}

loadProjects();
