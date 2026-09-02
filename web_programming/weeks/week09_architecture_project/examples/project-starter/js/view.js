export function renderItems(list, status, items) {
  list.replaceChildren();

  if (items.length === 0) {
    status.dataset.kind = "empty";
    status.textContent = "아직 항목이 없습니다. 첫 행동을 안내하세요.";
    return;
  }

  status.dataset.kind = "success";
  status.textContent = `${items.length}개 항목을 표시합니다.`;
  const fragment = document.createDocumentFragment();

  for (const item of items) {
    const listItem = document.createElement("li");
    const title = document.createElement("strong");
    const summary = document.createElement("p");
    title.textContent = String(item.title ?? "제목 없음");
    summary.textContent = String(item.summary ?? "");
    listItem.dataset.id = String(item.id);
    listItem.append(title, summary);
    fragment.append(listItem);
  }

  list.append(fragment);
}

export function renderError(list, status) {
  list.replaceChildren();
  status.dataset.kind = "error";
  status.textContent = "데이터를 불러오지 못했습니다. 다시 시도해 주세요.";
}
