const form = document.querySelector("#item-form");
const titleInput = document.querySelector("#item-title");
const list = document.querySelector("#item-list");
const emptyMessage = document.querySelector("#empty-message");
const status = document.querySelector("#status");

if (!form || !titleInput || !list || !emptyMessage || !status) {
  throw new Error("필수 DOM 요소를 찾을 수 없습니다.");
}

let items = [];

function render() {
  // TODO: 현재 items를 기준으로 list와 empty 상태를 그린다.
  console.table(items);
}

form.addEventListener("submit", (event) => {
  event.preventDefault();
  const title = titleInput.value.trim();

  // TODO: 입력 검증 → 상태 변경 → render 순서로 구현한다.
  status.textContent = title
    ? `"${title}"의 처리 코드를 작성하세요.`
    : "빈 입력을 처리하는 코드를 작성하세요.";
});

list.addEventListener("click", (event) => {
  // TODO: 실제 공개 연습에서 요구한 action과 id를 처리한다.
  console.log("clicked:", event.target);
});

render();
