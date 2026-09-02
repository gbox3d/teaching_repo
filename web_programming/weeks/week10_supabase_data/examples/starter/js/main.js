import { listPublishedPosts } from "./data-source.js";
import {
  createCourseClient,
  hasSupabaseConfig
} from "./supabase-client.js";
import { renderState } from "./ui.js";

const result = document.querySelector("#result");
const status = document.querySelector("#status");
const list = document.querySelector("#post-list");
const reloadButton = document.querySelector("#reload-button");

if (!result || !status || !list || !reloadButton) {
  throw new Error("필수 DOM 요소가 없습니다.");
}

async function loadPosts() {
  if (!hasSupabaseConfig()) {
    renderState(list, status, { kind: "setup" });
    return;
  }

  result.setAttribute("aria-busy", "true");
  reloadButton.disabled = true;
  renderState(list, status, { kind: "loading" });

  try {
    const client = await createCourseClient();
    const posts = await listPublishedPosts(client);
    renderState(
      list,
      status,
      posts.length === 0 ? { kind: "empty" } : { kind: "success", posts }
    );
  } catch (error) {
    console.error("Supabase 공개 읽기 실패:", error);
    renderState(list, status, { kind: "error" });
  } finally {
    result.setAttribute("aria-busy", "false");
    reloadButton.disabled = false;
  }
}

reloadButton.addEventListener("click", loadPosts);
loadPosts();
