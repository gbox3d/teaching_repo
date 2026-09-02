import {
  SUPABASE_PUBLISHABLE_KEY,
  SUPABASE_URL
} from "./config.js";

const CLIENT_MODULE_URL = "https://esm.sh/@supabase/supabase-js@2";

export function hasSupabaseConfig() {
  return (
    /^https:\/\/[a-z0-9-]+\.supabase\.co$/i.test(SUPABASE_URL) &&
    !SUPABASE_URL.includes("YOUR_PROJECT_REF") &&
    SUPABASE_PUBLISHABLE_KEY.startsWith("sb_publishable_") &&
    !SUPABASE_PUBLISHABLE_KEY.endsWith("REPLACE_ME")
  );
}

export async function createCourseClient() {
  if (!hasSupabaseConfig()) {
    throw new Error("Supabase publishable client 설정이 필요합니다.");
  }

  const { createClient } = await import(CLIENT_MODULE_URL);
  return createClient(SUPABASE_URL, SUPABASE_PUBLISHABLE_KEY);
}
