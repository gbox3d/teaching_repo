import test from 'node:test';
import assert from 'node:assert/strict';

import {
  buildStaticImageProxyUrl,
  decodeStaticImageBlob,
  normalizeStaticMapOptions,
  validateStaticMapSource,
} from '../js/static-map.js';
import { validateKakaoStaticImageUrl } from '../static-map-relay.mjs';

const VALID_SOURCE =
  'https://spi.map.kakao.com/map2/map/skyviewimageservice' +
  '?IW=640&IH=480&MX=123&MY=456&SCALE=10&service=open';

test('normalizes bounded StaticMap options', () => {
  assert.deepEqual(
    normalizeStaticMapOptions({
      latitude: '37.5512',
      longitude: '126.9882',
      width: '640',
      height: 480,
      level: 4,
    }),
    {
      latitude: 37.5512,
      longitude: 126.9882,
      width: 640,
      height: 480,
      level: 4,
      timeout: 10_000,
    },
  );
});

test('rejects coordinates, dimensions and levels outside the lesson bounds', () => {
  assert.throws(
    () => normalizeStaticMapOptions({ latitude: 91, longitude: 127 }),
    /위도/,
  );
  assert.throws(
    () => normalizeStaticMapOptions({ latitude: 35, longitude: 181 }),
    /경도/,
  );
  assert.throws(
    () => normalizeStaticMapOptions({ latitude: 35, longitude: 127, width: 2000 }),
    /너비/,
  );
  assert.throws(
    () => normalizeStaticMapOptions({ latitude: 35, longitude: 127, level: 15 }),
    /지도 레벨/,
  );
});

test('accepts only the exact Kakao SKYVIEW StaticMap endpoint', () => {
  assert.equal(validateStaticMapSource(VALID_SOURCE), VALID_SOURCE);

  for (const source of [
    VALID_SOURCE.replace('https:', 'http:'),
    VALID_SOURCE.replace('spi.map.kakao.com', 'evil.spi.map.kakao.com'),
    VALID_SOURCE.replace('skyviewimageservice', 'other-service'),
    'https://user@spi.map.kakao.com/map2/map/skyviewimageservice?MX=123',
    `${VALID_SOURCE}#fragment`,
  ]) {
    assert.throws(() => validateStaticMapSource(source), /허용되지 않은/);
  }
});

test('builds a same-origin proxy URL without interpreting Kakao query fields', () => {
  const proxyUrl = buildStaticImageProxyUrl(VALID_SOURCE);
  assert.ok(proxyUrl.startsWith('/api/kakao-static-image?source='));
  assert.equal(
    new URLSearchParams(proxyUrl.split('?')[1]).get('source'),
    VALID_SOURCE,
  );
  assert.equal(validateKakaoStaticImageUrl(VALID_SOURCE).href, VALID_SOURCE);
});

test('decodes an allowed response through createImageBitmap and forwards close', async () => {
  const originalCreateImageBitmap = globalThis.createImageBitmap;
  let closed = false;
  globalThis.createImageBitmap = async () => ({
    width: 640,
    height: 480,
    close() {
      closed = true;
    },
  });

  try {
    const decoded = await decodeStaticImageBlob(
      new Blob(['image-bytes'], { type: 'image/png' }),
    );
    assert.equal(decoded.width, 640);
    assert.equal(decoded.height, 480);
    decoded.close();
    assert.equal(closed, true);
  } finally {
    if (originalCreateImageBitmap === undefined) {
      delete globalThis.createImageBitmap;
    } else {
      globalThis.createImageBitmap = originalCreateImageBitmap;
    }
  }
});

test('rejects unsupported proxy response types before decoding', async () => {
  await assert.rejects(
    decodeStaticImageBlob(new Blob(['not-an-image'], { type: 'text/html' })),
    /지원되는 이미지 형식/,
  );
});
