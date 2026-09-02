import assert from 'node:assert/strict';
import test from 'node:test';

import {
  relayKakaoStaticImage,
  validateKakaoStaticImageUrl,
} from '../static-map-relay.mjs';

const validUrl =
  'https://spi.map.kakao.com/map2/map/skyviewimageservice' +
  '?IW=640&IH=480&MX=507000&MY=1123000&SCALE=10&service=open';

test('validateKakaoStaticImageUrl accepts only a bounded SDK SKYVIEW URL', () => {
  const url = validateKakaoStaticImageUrl(validUrl);
  assert.equal(url.origin, 'https://spi.map.kakao.com');
  assert.equal(url.pathname, '/map2/map/skyviewimageservice');

  assert.throws(
    () => validateKakaoStaticImageUrl(validUrl.replace('spi.map.kakao.com', 'example.com')),
    /허용된 Kakao/,
  );
  assert.throws(
    () => validateKakaoStaticImageUrl(`${validUrl}&next=https://example.com`),
    /허용되지 않은/,
  );
  assert.throws(
    () => validateKakaoStaticImageUrl(validUrl.replace('IW=640', 'IW=9999')),
    /1~2048/,
  );
  assert.equal(
    validateKakaoStaticImageUrl(`${validUrl}&CX=320&CY=240`).searchParams.get('CX'),
    '320',
  );
});

test('relayKakaoStaticImage returns a verified image body', async () => {
  const calls = [];
  const result = await relayKakaoStaticImage(validUrl, {
    fetchImpl: async (url, options) => {
      calls.push({ url: String(url), options });
      return new Response(new Uint8Array([0xff, 0xd8, 0xff, 0xd9]), {
        status: 200,
        headers: {
          'content-type': 'image/jpeg',
          'content-length': '4',
        },
      });
    },
  });

  assert.equal(calls.length, 1);
  assert.equal(calls[0].options.redirect, 'error');
  assert.equal(result.contentType, 'image/jpeg');
  assert.deepEqual([...result.body], [0xff, 0xd8, 0xff, 0xd9]);
});

test('relayKakaoStaticImage rejects non-image and oversized responses', async () => {
  await assert.rejects(
    relayKakaoStaticImage(validUrl, {
      fetchImpl: async () =>
        new Response('not an image', {
          status: 200,
          headers: { 'content-type': 'text/plain' },
        }),
    }),
    /이미지가 아닙니다/,
  );

  await assert.rejects(
    relayKakaoStaticImage(validUrl, {
      maximumBytes: 3,
      fetchImpl: async () =>
        new Response(new Uint8Array([1, 2, 3, 4]), {
          status: 200,
          headers: { 'content-type': 'image/png' },
        }),
    }),
    /크기가 올바르지 않습니다/,
  );
});
