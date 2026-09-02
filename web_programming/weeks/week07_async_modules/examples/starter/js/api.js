function isCard(value) {
  return (
    value !== null &&
    typeof value === "object" &&
    (typeof value.id === "string" || typeof value.id === "number") &&
    typeof value.title === "string" &&
    typeof value.category === "string"
  );
}

export async function fetchCards(url) {
  const response = await fetch(url);

  if (!response.ok) {
    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
  }

  const value = await response.json();

  if (!Array.isArray(value)) {
    throw new TypeError("응답의 최상위 값이 배열이 아닙니다.");
  }

  if (!value.every(isCard)) {
    throw new TypeError("필수 field가 없는 카드가 있습니다.");
  }

  return value.map((card) => ({
    id: String(card.id),
    title: card.title.trim(),
    category: card.category.trim()
  }));
}
