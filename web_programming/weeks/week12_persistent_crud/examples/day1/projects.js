const projectList = document.querySelector('#project-list');

function showProjects(projects) {
  projectList.innerHTML = '';
  for (let i = 0; i < projects.length; i++) {
    const article = document.createElement('article');
    article.classList.add('card');
    const title = document.createElement('h3');
    title.textContent = projects[i].title;
    const description = document.createElement('p');
    description.textContent = projects[i].description;
    article.append(title, description);
    projectList.append(article);
  }
}

async function loadProjects() {
  const response = await fetch('data/projects.json');
  const projects = await response.json();
  console.log(projects);
  showProjects(projects);
}

loadProjects();
