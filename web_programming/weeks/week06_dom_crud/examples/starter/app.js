const form = document.querySelector("#todo-form");
const titleInput = document.querySelector("#todo-title");
const list = document.querySelector("#todo-list");
const emptyMessage = document.querySelector("#empty-message");
const status = document.querySelector("#status");

if (!form || !titleInput || !list || !emptyMessage || !status) {
  throw new Error("필수 DOM 요소를 찾을 수 없습니다.");
}

let todos = [];

function render() {
  // TODO 1: todos 전체를 기준으로 목록을 다시 그린다.
  // TODO 2: todos.length에 따라 emptyMessage를 표시하거나 숨긴다.
  console.table(todos);
}

form.addEventListener("submit", (event) => {
  event.preventDefault();
  const title = titleInput.value.trim();

  if (!title) {
    status.textContent = "한 글자 이상 입력하세요.";
    titleInput.focus();
    return;
  }

  status.textContent = `"${title}"을(를) 배열에 추가하는 코드를 작성하세요.`;
  // TODO 3: 고유 id를 가진 객체를 todos에 추가하고 render()를 호출한다.
});

list.addEventListener("click", (event) => {
  const button = event.target.closest("button[data-action]");
  if (!button) return;

  // TODO 4: action과 가장 가까운 data-id를 읽어 CRUD를 분기한다.
  console.log("action:", button.dataset.action);
});

render();
