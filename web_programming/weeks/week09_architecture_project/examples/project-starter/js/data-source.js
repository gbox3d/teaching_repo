const DATA_URL = "./data/items.json";

export async function listItems() {
  const response = await fetch(DATA_URL);

  if (!response.ok) {
    throw new Error(`항목 요청 실패: HTTP ${response.status}`);
  }

  const value = await response.json();

  if (!Array.isArray(value)) {
    throw new TypeError("항목 응답은 배열이어야 합니다.");
  }

  return value;
}
