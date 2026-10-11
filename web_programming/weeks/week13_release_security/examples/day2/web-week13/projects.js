const projectList = document.querySelector('#project-list');
const notice = document.querySelector('#notice');

function showProjects(projects) {
  projectList.innerHTML = '';
  for (let i = 0; i < projects.length; i++) {
    const article = document.createElement('article');
    article.classList.add('card');
    const image = document.createElement('img');
    image.src = projects[i].image;
    image.alt = `${projects[i].title} 화면 그림`;
    image.width = 240;
    const title = document.createElement('h3');
    title.textContent = projects[i].title;
    const description = document.createElement('p');
    description.textContent = projects[i].description;
    const link = document.createElement('a');
    link.href = projects[i].link;
    link.textContent = `${projects[i].title} 열기`;
    article.append(image, title, description, link);
    projectList.append(article);
  }
}

async function loadProjects() {
  try {
    const response = await fetch('data/projects.json');
    if (!response.ok) {
      notice.textContent = '프로젝트를 불러오지 못했습니다.';
      return;
    }
    const projects = await response.json();
    notice.textContent = '';
    showProjects(projects);
  } catch (error) {
    notice.textContent = '프로젝트를 불러오지 못했습니다.';
  }
}

loadProjects();
