import assert from 'node:assert/strict';
import test from 'node:test';

import {
  canvasFilter,
  clientPointToCanvasPoint,
  downloadFilename,
  fitWithin,
  fixedRotationLayout,
  parseCoordinates,
} from '../js/editor-core.js';

test('parseCoordinates validates WGS84 ranges', () => {
  assert.deepEqual(parseCoordinates('35.1', '127.2'), {
    latitude: 35.1,
    longitude: 127.2,
  });
  assert.throws(() => parseCoordinates('91', '127'), /위도/);
  assert.throws(() => parseCoordinates('35', '181'), /경도/);
  assert.throws(() => parseCoordinates('NaN', '127'), /유한한 숫자/);
  assert.throws(() => parseCoordinates('  ', '127'), /모두 입력/);
  assert.deepEqual(parseCoordinates('-90', '180'), {
    latitude: -90,
    longitude: 180,
  });
});

test('rotation keeps a fixed viewport and clips without scaling', () => {
  const expected = {
    outputWidth: 617,
    outputHeight: 480,
    editableWidth: 617,
    editableHeight: 480,
    centerX: 308.5,
    centerY: 240,
    clip: { x: 0, y: 0, width: 617, height: 480 },
    attribution: { x: 0, y: 448, width: 80, height: 32 },
    scale: 1,
  };

  for (const [angle, expectedRadians] of [
    [0, 0],
    [17, (17 * Math.PI) / 180],
    [90, Math.PI / 2],
    [180, Math.PI],
    [-90, (3 * Math.PI) / 2],
  ]) {
    const { radians, ...layout } = fixedRotationLayout(
      617,
      480,
      80,
      32,
      angle,
    );
    assert.deepEqual(layout, expected);
    assert.ok(Math.abs(radians - expectedRadians) < 1e-12);
  }
});

test('image import size is bounded', () => {
  assert.deepEqual(fitWithin(8000, 4000, 4096), {
    width: 4096,
    height: 2048,
    scale: 0.512,
  });
});

test('filter and filename values are normalized', () => {
  assert.equal(canvasFilter(200, 10), 'brightness(150%) contrast(50%)');
  assert.equal(canvasFilter(0, 0), 'brightness(50%) contrast(50%)');
  assert.equal(
    downloadFilename('png', new Date('2026-08-26T03:04:05.006Z')),
    'aerial-canvas-2026-08-26T03-04-05-006Z.png',
  );
});

test('client pointer coordinates follow the displayed canvas scale', () => {
  const canvas = {
    width: 1000,
    height: 500,
    getBoundingClientRect: () => ({
      left: 10,
      top: 20,
      width: 500,
      height: 250,
    }),
  };

  assert.deepEqual(
    clientPointToCanvasPoint(
      { clientX: 260, clientY: 145 },
      canvas,
      400,
    ),
    {
      x: 500,
      y: 250,
      normalizedX: 0.5,
      normalizedY: 0.625,
      insideEditableArea: true,
    },
  );
  assert.equal(
    clientPointToCanvasPoint(
      { clientX: 260, clientY: 265 },
      canvas,
      400,
    ).insideEditableArea,
    false,
  );
});
