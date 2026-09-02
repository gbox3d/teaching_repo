export function renderState(result, status, state) {
  result.setAttribute("aria-busy", String(state.kind === "loading"));
  status.dataset.kind = state.kind;
  status.textContent = "";
  const list = result.querySelector("#card-list");
  list.replaceChildren();

  if (state.kind === "loading") {
    status.textContent = "데이터를 불러오는 중입니다…";
    return;
  }

  if (state.kind === "empty") {
    status.textContent = "표시할 카드가 없습니다.";
    return;
  }

  if (state.kind === "error") {
    status.textContent = "데이터를 불러오지 못했습니다. source를 확인하고 다시 시도하세요.";
    return;
  }

  status.textContent = `${state.cards.length}개 카드를 불러왔습니다.`;
  const fragment = document.createDocumentFragment();

  for (const card of state.cards) {
    const item = document.createElement("li");
    const title = document.createElement("strong");
    const category = document.createElement("p");
    title.textContent = card.title;
    category.textContent = card.category;
    item.append(title, category);
    fragment.append(item);
  }

  list.append(fragment);
}
