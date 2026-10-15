import { expect, test } from '@jest/globals';
import { formatTranslation } from '../services/google-translate.js';

test('formatTranslation joins sentence segments', () => {
  const data = [[['他喝醉了，', 'He was drunk, '], ['記不得關門。', 'and forgot the door.']], null, 'en'];
  expect(formatTranslation(data)).toBe('他喝醉了，記不得關門。');
});

test('formatTranslation lists dictionary meanings by part of speech', () => {
  const data = [[['喝醉了', 'drunk']], [['形容詞', ['喝醉了', '醉', '酒醉', '陶醉', '醉醺醺', '多餘']], ['名詞', ['醉漢']]], 'en'];
  expect(formatTranslation(data)).toBe('喝醉了\n形容詞：喝醉了、醉、酒醉、陶醉、醉醺醺\n名詞：醉漢');
});

test('formatTranslation returns empty text for unexpected data', () => {
  expect(formatTranslation(null)).toBe('');
  expect(formatTranslation({})).toBe('');
});
