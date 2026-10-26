// ex04 카드 만들기: 배열의 항목 하나 → article 카드 한 장. 카드 안에 그림(img)·제목(h3)·설명(p)·링크(a)를 넣는다
// 10주차 showList 와 같은 순서다(비우기 → for → 만들어 붙이기). 화면과 F12 › Elements 를 본다.

// JS 안에 적은 객체라서 이름에 따옴표가 없고 작은따옴표를 쓴다(11주차). JSON 파일에서는 안 된다(ex01)
const sampleProjects = [
    {
        title: '자기소개 페이지',
        description: '3주차에 HTML 뼈대로 만들었습니다.',
        image: 'ex04_picture.png',
        link: 'https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week03_semantic_html'
    },
    {
        title: '다크 모드',
        description: '6주차에 버튼 하나로 화면을 어둡게 했습니다.',
        image: 'ex04_picture.png',
        link: 'https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week06_dom_crud'
    },
    {
        title: '방명록 저장',
        description: '11주차에 새로고침해도 글이 남게 했습니다.',
        image: 'ex04_picture.png',
        link: 'https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week11_auth_rls'
    }
];
const projectList = document.querySelector('#project-list');

// 넘겨받은 배열을 함수 안에서는 projects 라는 이름으로 쓴다(5주차 ex08 매개변수)
function showProjects(projects) {
    projectList.innerHTML = '';                               // 10주차: 비우기 전용
    for (let i = 0; i < projects.length; i++) {
        const article = document.createElement('article');   // 카드 한 장
        article.classList.add('card');                        // 6주차 classList → .card 규칙이 붙는다
        const image = document.createElement('img');          // 1. 그림
        image.src = projects[i].image;                        // 그림 파일 주소
        image.alt = `${projects[i].title} 그림`;              // 그림이 안 보일 때 대신 보이는 글
        image.width = 160;
        const title = document.createElement('h3');          // 2. 제목
        title.textContent = projects[i].title;
        const description = document.createElement('p');      // 3. 설명 — 실제 문장이라 p
        description.textContent = projects[i].description;
        const link = document.createElement('a');             // 4. 링크
        link.href = projects[i].link;                         // 누르면 갈 주소
        link.textContent = '교재 열기';
        article.append(image, title, description, link);      // 넣은 순서대로 카드 안에 쌓인다
        projectList.append(article);
    }
}

showProjects(sampleProjects);
