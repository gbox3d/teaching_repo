export function renderState(list, status, state) {
  list.replaceChildren();
  status.dataset.kind = state.kind;

  if (state.kind === "setup") {
    status.textContent =
      "js/config.js의 project URL과 publishable key placeholder를 바꾸세요.";
    return;
  }

  if (state.kind === "loading") {
    status.textContent = "공개 글을 불러오는 중입니다…";
    return;
  }

  if (state.kind === "empty") {
    status.textContent = "공개된 글이 없습니다.";
    return;
  }

  if (state.kind === "error") {
    status.textContent =
      "글을 불러오지 못했습니다. Console과 Network를 확인한 뒤 다시 시도하세요.";
    return;
  }

  status.textContent = `${state.posts.length}개 공개 글을 불러왔습니다.`;
  const fragment = document.createDocumentFragment();

  for (const post of state.posts) {
    const item = document.createElement("li");
    const title = document.createElement("strong");
    const summary = document.createElement("p");
    title.textContent = post.title;
    summary.textContent = post.summary;
    item.dataset.id = String(post.id);
    fragment.append(item);
    item.append(title, summary);
  }

  list.append(fragment);
}
