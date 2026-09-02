import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
import { SUPABASE_URL, SUPABASE_PUBLISHABLE_KEY } from "./config.js";

const supabase = createClient(SUPABASE_URL, SUPABASE_PUBLISHABLE_KEY);

const statusNode = document.querySelector("#status");
const authForm = document.querySelector("#auth-form");
const postForm = document.querySelector("#post-form");
const authRequired = document.querySelector("#auth-required");
const postsNode = document.querySelector("#posts");
const emptyNode = document.querySelector("#empty");
let currentUser = null;

function setStatus(message, kind = "info") {
  statusNode.textContent = message;
  statusNode.dataset.kind = kind;
}

function credentials() {
  return {
    email: document.querySelector("#email").value.trim(),
    password: document.querySelector("#password").value
  };
}

function renderAuth(session) {
  currentUser = session?.user ?? null;
  postForm.hidden = !currentUser;
  authRequired.hidden = Boolean(currentUser);
  setStatus(currentUser ? "로그인: " + currentUser.email : "비로그인 상태");
  renderPosts();
}

async function runAuth(action) {
  setStatus("인증 요청 중…");
  const values = credentials();
  let result;

  if (action === "signup") {
    result = await supabase.auth.signUp(values);
  } else if (action === "signin") {
    result = await supabase.auth.signInWithPassword(values);
  } else {
    result = await supabase.auth.signOut();
  }

  if (result.error) setStatus(result.error.message, "error");
}

async function loadPosts() {
  const result = await supabase
    .from("posts")
    .select("id,title,owner_id,created_at")
    .order("created_at", { ascending: false });

  if (result.error) throw result.error;
  return result.data;
}

function postItem(post) {
  const item = document.createElement("li");
  const text = document.createElement("span");
  text.textContent = post.title;
  item.append(text);

  if (currentUser?.id === post.owner_id) {
    const edit = document.createElement("button");
    edit.type = "button";
    edit.textContent = "수정";
    edit.addEventListener("click", () => editPost(post));

    const remove = document.createElement("button");
    remove.type = "button";
    remove.textContent = "삭제";
    remove.addEventListener("click", () => deletePost(post.id));
    item.append(edit, remove);
  }

  return item;
}

async function renderPosts() {
  postsNode.replaceChildren();
  emptyNode.hidden = true;
  try {
    const posts = await loadPosts();
    posts.forEach((post) => postsNode.append(postItem(post)));
    emptyNode.hidden = posts.length !== 0;
  } catch (error) {
    setStatus("목록을 읽지 못했습니다: " + error.message, "error");
  }
}

async function addPost(title) {
  const result = await supabase
    .from("posts")
    .insert({ title, owner_id: currentUser.id });
  if (result.error) throw result.error;
}

async function editPost(post) {
  const nextTitle = window.prompt("새 제목", post.title)?.trim();
  if (!nextTitle) return;
  const result = await supabase
    .from("posts")
    .update({ title: nextTitle })
    .eq("id", post.id);
  if (result.error) setStatus(result.error.message, "error");
  await renderPosts();
}

async function deletePost(id) {
  const result = await supabase.from("posts").delete().eq("id", id);
  if (result.error) setStatus(result.error.message, "error");
  await renderPosts();
}

authForm.addEventListener("submit", (event) => {
  event.preventDefault();
  runAuth("signin");
});

authForm.addEventListener("click", (event) => {
  const action = event.target.dataset.action;
  if (action === "signup" || action === "signout") runAuth(action);
});

postForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  if (!currentUser) return setStatus("로그인이 필요합니다.", "error");
  const titleInput = document.querySelector("#title");
  try {
    await addPost(titleInput.value.trim());
    titleInput.value = "";
    await renderPosts();
  } catch (error) {
    setStatus(error.message, "error");
  }
});

document.querySelector("#reload").addEventListener("click", renderPosts);

supabase.auth.onAuthStateChange((_event, session) => renderAuth(session));
const sessionResult = await supabase.auth.getSession();
renderAuth(sessionResult.data.session);
