import { activities } from './activities.mjs';
import {
  filterByCategory,
  searchActivities,
  sortByStartsAt,
  summarizeActivities,
  toCardModels,
  uniqueTags,
} from './transforms.mjs';

const originalIds = activities.map(({ id }) => id);
const state = {
  query: '웹',
  category: 'study',
  direction: 'asc',
};

const searched = searchActivities(activities, state.query);
const filtered = filterByCategory(searched, state.category);
const sorted = sortByStartsAt(filtered, state.direction);
const cards = toCardModels(sorted);
const summary = summarizeActivities(activities);

console.log('단계별 개수', {
  all: activities.length,
  searched: searched.length,
  filtered: filtered.length,
  cards: cards.length,
});
console.table(cards);
console.log('고유 태그', uniqueTags(activities));
console.log('전체 요약', {
  ...summary,
  categoryCounts: Object.fromEntries(summary.categoryCounts),
});
console.log('원본 순서 유지', {
  before: originalIds,
  after: activities.map(({ id }) => id),
});
