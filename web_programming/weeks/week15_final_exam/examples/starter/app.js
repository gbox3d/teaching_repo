import { fetchCards, setFailMode } from "./service.js";

const list = document.querySelector("#cards");
const statusNode = document.querySelector("#status");
const retry = document.querySelector("#retry");
let cards = [];

function setStatus(message, kind = "info") {
  statusNode.textContent = message;
  statusNode.dataset.kind = kind;
}

function render(items) {
  list.replaceChildren();
  for (const item of items) {
    const row = document.createElement("li");
    row.textContent = item.title + " · " + item.category;
    list.append(row);
  }
  // TODO: empty 상태를 구분한다.
}

async function load() {
  retry.hidden = true;
  setStatus("불러오는 중…");
  try {
    cards = await fetchCards();
    render(cards);
    setStatus(cards.length + "개");
  } catch (_error) {
    // TODO: 안전한 오류 문구와 retry를 연결한다.
    setStatus("불러오지 못했습니다.", "error");
  }
}

document.querySelector("#search-form").addEventListener("submit", (event) => {
  event.preventDefault();
  const query = document.querySelector("#query").value.trim().toLowerCase();
  // TODO: title과 category 검색 결과를 render한다.
  render(cards);
  setStatus("검색어: " + query);
});

document.querySelector("#fail-mode").addEventListener("change", (event) => {
  setFailMode(event.target.checked);
});

retry.addEventListener("click", load);
load();
