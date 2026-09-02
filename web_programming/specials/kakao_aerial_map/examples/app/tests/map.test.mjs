import assert from 'node:assert/strict';
import test from 'node:test';

import { addressToCoordinates, setMapType, waitForTiles } from '../js/map.js';

const previousKakao = globalThis.kakao;

function installKakaoMock() {
  globalThis.kakao = {
    maps: {
      MapTypeId: {
        ROADMAP: 1,
        SKYVIEW: 2,
        HYBRID: 3,
      },
      services: {
        Status: {
          OK: 'OK',
          ZERO_RESULT: 'ZERO_RESULT',
          ERROR: 'ERROR',
        },
      },
    },
  };
}

test.after(() => {
  if (previousKakao === undefined) delete globalThis.kakao;
  else globalThis.kakao = previousKakao;
});

test('addressToCoordinates maps Kakao x/y to longitude/latitude', async () => {
  installKakaoMock();
  const geocoder = {
    addressSearch(_query, callback) {
      callback(
        [
          {
            x: '127.1234',
            y: '35.9876',
            address_name: '지번 주소',
            road_address: { address_name: '도로명 주소' },
          },
        ],
        'OK',
      );
    },
  };

  assert.deepEqual(await addressToCoordinates(geocoder, '서울시청'), {
    latitude: 35.9876,
    longitude: 127.1234,
    address: '도로명 주소',
    addressName: '지번 주소',
    roadAddressName: '도로명 주소',
  });
});

test('addressToCoordinates distinguishes no result from service failure', async () => {
  installKakaoMock();
  await assert.rejects(
    addressToCoordinates(
      { addressSearch: (_query, callback) => callback([], 'ZERO_RESULT') },
      '없는 주소',
    ),
    /찾지 못했습니다/,
  );
  await assert.rejects(
    addressToCoordinates(
      { addressSearch: (_query, callback) => callback([], 'ERROR') },
      '오류 주소',
    ),
    /요청에 실패/,
  );
});

test('setMapType uses only the public base map type IDs', () => {
  installKakaoMock();
  const selected = [];
  const map = { setMapTypeId: (value) => selected.push(value) };

  setMapType(map, 'SKYVIEW');
  setMapType(map, 'hybrid');
  assert.deepEqual(selected, [2, 3]);
  assert.throws(() => setMapType(map, 'TILE_URL'), /지원하지 않는/);
});

test('waitForTiles removes its listener when an operation is aborted', async () => {
  installKakaoMock();
  const map = {};
  const removed = [];
  globalThis.kakao.maps.event = {
    addListener() {},
    removeListener(target, name, handler) {
      removed.push({ target, name, handler });
    },
  };
  const controller = new AbortController();
  const waiting = waitForTiles(map, {
    timeout: 1_000,
    signal: controller.signal,
  });

  controller.abort();
  await assert.rejects(waiting, (error) => error.name === 'AbortError');
  assert.equal(removed.length, 1);
  assert.equal(removed[0].target, map);
  assert.equal(removed[0].name, 'tilesloaded');
});
