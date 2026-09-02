export async function listPublishedPosts(client) {
  const { data, error } = await client
    .from("course_posts")
    .select("id, slug, title, summary, created_at")
    .eq("is_published", true)
    .order("created_at", { ascending: false });

  if (error) {
    throw new Error(
      `Supabase ${error.code ?? "UNKNOWN"}: ${error.message}`
    );
  }

  if (!Array.isArray(data)) {
    throw new TypeError("Supabase 응답 data가 배열이 아닙니다.");
  }

  return data;
}
