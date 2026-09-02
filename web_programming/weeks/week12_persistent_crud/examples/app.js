import { supabase } from "./api.js";
import {
  createPost,
  deletePost,
  listPosts,
  updatePost
} from "./postService.js";
import {
  createComment,
  deleteComment,
  listComments
} from "./commentService.js";

const statusNode = document.querySelector("#status");
const postForm = document.querySelector("#post-form");
const commentSection = document.querySelector("#comment-section");
const postsNode = document.querySelector("#posts");
const commentsNode = document.querySelector("#comments");
let user = null;
let selectedPostId = null;

function status(message, kind = "info") {
  statusNode.textContent = message;
  statusNode.dataset.kind = kind;
}

function button(label, action) {
  const node = document.createElement("button");
  node.type = "button";
  node.textContent = label;
  node.addEventListener("click", action);
  return node;
}

async function refreshPosts() {
  status("게시글 읽는 중…");
  try {
    const posts = await listPosts();
    postsNode.replaceChildren();
    document.querySelector("#post-empty").hidden = posts.length !== 0;

    posts.forEach((post) => {
      const item = document.createElement("li");
      const title = document.createElement("span");
      title.textContent = post.title;
      item.append(title, button("댓글", () => selectPost(post.id)));

      if (user?.id === post.owner_id) {
        item.append(
          button("수정", () => edit(post)),
          button("삭제", () => removePost(post.id))
        );
      }
      postsNode.append(item);
    });
    status("게시글 " + posts.length + "개");
  } catch (error) {
    status("게시글 오류: " + error.message, "error");
  }
}

async function selectPost(id) {
  selectedPostId = id;
  commentSection.hidden = false;
  await refreshComments();
}

async function refreshComments() {
  try {
    const comments = await listComments(selectedPostId);
    commentsNode.replaceChildren();
    document.querySelector("#comment-empty").hidden = comments.length !== 0;
    comments.forEach((comment) => {
      const item = document.createElement("li");
      const text = document.createElement("span");
      text.textContent = comment.body;
      item.append(text);
      if (user?.id === comment.owner_id) {
        item.append(button("삭제", async () => {
          await deleteComment(comment.id);
          await refreshComments();
        }));
      }
      commentsNode.append(item);
    });
  } catch (error) {
    status("댓글 오류: " + error.message, "error");
  }
}

async function edit(post) {
  const title = window.prompt("새 제목", post.title)?.trim();
  if (!title) return;
  const changed = await updatePost(post.id, title);
  if (changed.length === 0) status("수정 권한이 없거나 글이 없습니다.", "error");
  await refreshPosts();
}

async function removePost(id) {
  const removed = await deletePost(id);
  if (removed.length === 0) status("삭제 권한이 없거나 글이 없습니다.", "error");
  if (selectedPostId === id) {
    selectedPostId = null;
    commentSection.hidden = true;
  }
  await refreshPosts();
}

document.querySelector("#auth-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const email = document.querySelector("#email").value.trim();
  const password = document.querySelector("#password").value;
  const result = await supabase.auth.signInWithPassword({ email, password });
  if (result.error) status(result.error.message, "error");
});

document.querySelector("#logout").addEventListener("click", () => supabase.auth.signOut());

postForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const input = document.querySelector("#title");
  await createPost(input.value.trim(), user.id);
  input.value = "";
  await refreshPosts();
});

document.querySelector("#comment-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  if (!user) return status("로그인이 필요합니다.", "error");
  const input = document.querySelector("#body");
  await createComment(selectedPostId, input.value.trim(), user.id);
  input.value = "";
  await refreshComments();
});

supabase.auth.onAuthStateChange((_event, session) => {
  user = session?.user ?? null;
  postForm.hidden = !user;
  status(user ? "로그인: " + user.email : "비로그인");
  refreshPosts();
});

const sessionResult = await supabase.auth.getSession();
user = sessionResult.data.session?.user ?? null;
postForm.hidden = !user;
await refreshPosts();
