import { fetchCards } from "./api.js";
import { renderState } from "./ui.js";

const source = document.querySelector("#source");
const loadButton = document.querySelector("#load-button");
const result = document.querySelector("#result");
const status = document.querySelector("#status");

if (!source || !loadButton || !result || !status) {
  throw new Error("필수 DOM 요소가 없습니다.");
}

async function loadSelectedSource() {
  renderState(result, status, { kind: "loading" });
  loadButton.disabled = true;

  try {
    const cards = await fetchCards(source.value);
    renderState(
      result,
      status,
      cards.length === 0 ? { kind: "empty" } : { kind: "success", cards }
    );
  } catch (error) {
    console.error("카드 요청 실패:", error);
    renderState(result, status, { kind: "error" });
  } finally {
    loadButton.disabled = false;
  }
}

loadButton.addEventListener("click", loadSelectedSource);
