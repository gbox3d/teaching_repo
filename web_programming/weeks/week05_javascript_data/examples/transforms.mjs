const categoryLabels = new Map([
  ['study', '학습'],
  ['hobby', '취미'],
  ['volunteer', '봉사'],
]);

function normalizeText(value) {
  return String(value).trim().toLocaleLowerCase('ko-KR');
}

export function searchActivities(items, query) {
  const normalizedQuery = normalizeText(query);

  if (!normalizedQuery) {
    return [...items];
  }

  return items.filter(({ title, description, tags }) => {
    const textMatches = [title, description]
      .map(normalizeText)
      .some((text) => text.includes(normalizedQuery));
    const tagMatches = tags
      .map(normalizeText)
      .some((tag) => tag.includes(normalizedQuery));

    return textMatches || tagMatches;
  });
}

export function filterByCategory(items, category) {
  return category === 'all'
    ? [...items]
    : items.filter((item) => item.category === category);
}

export function findActivityById(items, id) {
  return items.find((item) => item.id === id);
}

export function uniqueTags(items) {
  return [...new Set(items.flatMap(({ tags }) => tags))].sort();
}

export function sortByStartsAt(items, direction = 'asc') {
  if (direction !== 'asc' && direction !== 'desc') {
    throw new RangeError(`Unsupported sort direction: ${direction}`);
  }

  const factor = direction === 'asc' ? 1 : -1;

  return [...items].sort((first, second) => {
    const byDate = first.startsAt.localeCompare(second.startsAt) * factor;
    return byDate || first.id.localeCompare(second.id);
  });
}

export function toCardModels(items) {
  return items.map(({ id, title, category, capacity, joined, startsAt }) => {
    const remainingSeats = Math.max(capacity - joined, 0);

    return {
      id,
      title,
      categoryLabel: categoryLabels.get(category) ?? '기타',
      startsAt,
      availability: remainingSeats === 0 ? '마감' : `${remainingSeats}자리 남음`,
    };
  });
}

export function summarizeActivities(items) {
  return items.reduce(
    (summary, { category, capacity, joined }) => {
      summary.totalActivities += 1;
      summary.totalCapacity += capacity;
      summary.totalJoined += joined;
      summary.openActivities += joined < capacity ? 1 : 0;
      summary.categoryCounts.set(
        category,
        (summary.categoryCounts.get(category) ?? 0) + 1,
      );
      return summary;
    },
    {
      totalActivities: 0,
      totalCapacity: 0,
      totalJoined: 0,
      openActivities: 0,
      categoryCounts: new Map(),
    },
  );
}
