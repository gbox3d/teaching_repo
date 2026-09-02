import { supabase } from "./api.js";

export async function listPosts() {
  const result = await supabase
    .from("posts")
    .select("id,title,owner_id,created_at")
    .order("created_at", { ascending: false });
  if (result.error) throw result.error;
  return result.data;
}

export async function createPost(title, ownerId) {
  const result = await supabase
    .from("posts")
    .insert({ title, owner_id: ownerId })
    .select("id")
    .single();
  if (result.error) throw result.error;
  return result.data;
}

export async function updatePost(id, title) {
  const result = await supabase
    .from("posts")
    .update({ title })
    .eq("id", id)
    .select("id");
  if (result.error) throw result.error;
  return result.data;
}

export async function deletePost(id) {
  const result = await supabase
    .from("posts")
    .delete()
    .eq("id", id)
    .select("id");
  if (result.error) throw result.error;
  return result.data;
}
