import { listItems } from "./data-source.js";
import { renderError, renderItems } from "./view.js";

const result = document.querySelector("#result");
const status = document.querySelector("#status");
const list = document.querySelector("#item-list");

if (!result || !status || !list) {
  throw new Error("필수 DOM 요소가 없습니다.");
}

async function start() {
  result.setAttribute("aria-busy", "true");
  status.dataset.kind = "loading";
  status.textContent = "데이터를 불러오는 중입니다…";

  try {
    const items = await listItems();
    renderItems(list, status, items);
  } catch (error) {
    console.error("walking skeleton 실패:", error);
    renderError(list, status);
  } finally {
    result.setAttribute("aria-busy", "false");
  }
}

start();
