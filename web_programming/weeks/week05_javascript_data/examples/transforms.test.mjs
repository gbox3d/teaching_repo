import assert from 'node:assert/strict';
import test from 'node:test';

import { activities } from './activities.mjs';
import {
  filterByCategory,
  findActivityById,
  searchActivities,
  sortByStartsAt,
  summarizeActivities,
  toCardModels,
  uniqueTags,
} from './transforms.mjs';

test('search normalizes whitespace and case', () => {
  assert.deepEqual(
    searchActivities(activities, '  WEB  ').map(({ id }) => id),
    ['web-study', 'js-functions'],
  );
});

test('empty search returns a new array with every activity', () => {
  const result = searchActivities(activities, '   ');
  assert.notStrictEqual(result, activities);
  assert.deepEqual(result, activities);
});

test('category filter handles all and unknown categories', () => {
  assert.notStrictEqual(filterByCategory(activities, 'all'), activities);
  assert.equal(filterByCategory(activities, 'all').length, activities.length);
  assert.deepEqual(filterByCategory(activities, 'unknown'), []);
});

test('find returns one activity or undefined', () => {
  assert.equal(findActivityById(activities, 'photo-walk')?.title, '사진 산책');
  assert.equal(findActivityById(activities, 'missing'), undefined);
});

test('unique tags are sorted and contain no duplicates', () => {
  const tags = uniqueTags(activities);
  assert.deepEqual(tags, [...new Set(tags)].sort());
  assert.equal(tags.filter((tag) => tag === 'walk').length, 1);
});

test('sort returns date order without mutating the source array', () => {
  const before = activities.map(({ id }) => id);
  const sorted = sortByStartsAt(activities, 'asc');

  assert.equal(sorted[0].id, 'campus-guide');
  assert.deepEqual(activities.map(({ id }) => id), before);
  assert.notStrictEqual(sorted, activities);
});

test('sort supports descending and rejects an unknown direction', () => {
  assert.equal(sortByStartsAt(activities, 'desc')[0].id, 'river-cleanup');
  assert.throws(
    () => sortByStartsAt(activities, 'sideways'),
    { name: 'RangeError' },
  );
});

test('card model marks an activity with no seats as closed', () => {
  const [card] = toCardModels([
    {
      id: 'closed',
      title: '마감 활동',
      category: 'study',
      capacity: 3,
      joined: 3,
      startsAt: '2026-09-01T10:00:00+09:00',
    },
  ]);

  assert.equal(card.availability, '마감');
  assert.equal(card.categoryLabel, '학습');
});

test('empty summary keeps stable number and Map types', () => {
  const summary = summarizeActivities([]);

  assert.equal(summary.totalActivities, 0);
  assert.equal(summary.totalCapacity, 0);
  assert.equal(summary.totalJoined, 0);
  assert.equal(summary.openActivities, 0);
  assert.ok(summary.categoryCounts instanceof Map);
  assert.equal(summary.categoryCounts.size, 0);
});
