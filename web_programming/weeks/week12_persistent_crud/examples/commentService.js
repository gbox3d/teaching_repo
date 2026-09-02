import { supabase } from "./api.js";

export async function listComments(postId) {
  const result = await supabase
    .from("comments")
    .select("id,post_id,owner_id,body,created_at")
    .eq("post_id", postId)
    .order("created_at");
  if (result.error) throw result.error;
  return result.data;
}

export async function createComment(postId, body, ownerId) {
  const result = await supabase
    .from("comments")
    .insert({ post_id: postId, body, owner_id: ownerId });
  if (result.error) throw result.error;
}

export async function deleteComment(id) {
  const result = await supabase
    .from("comments")
    .delete()
    .eq("id", id)
    .select("id");
  if (result.error) throw result.error;
  return result.data;
}
