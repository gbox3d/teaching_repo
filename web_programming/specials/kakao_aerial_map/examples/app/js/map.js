const SDK_SCRIPT_ID = 'kakao-maps-sdk';
const DEFAULT_POSITION = Object.freeze({
  latitude: 37.566826,
  longitude: 126.978656,
});

let sdkPromise;

function kakaoMaps() {
  return globalThis.kakao?.maps;
}

function requireKakaoMaps() {
  const maps = kakaoMaps();
  if (!maps) {
    throw new Error('Kakao Maps SDK가 아직 준비되지 않았습니다.');
  }
  return maps;
}

function sdkReady(maps) {
  return Boolean(maps?.Map && maps?.services?.Geocoder);
}

/**
 * Loads the official Kakao Maps JavaScript SDK once.
 * The services library is requested for address geocoding.
 */
export function loadKakaoMaps(javascriptKey) {
  const key = String(javascriptKey ?? '').trim();
  if (!key) {
    return Promise.reject(
      new Error('config.json에 Kakao Maps JavaScript 키를 설정해 주세요.'),
    );
  }

  const existingMaps = kakaoMaps();
  if (sdkReady(existingMaps)) {
    return Promise.resolve(existingMaps);
  }
  if (sdkPromise) return sdkPromise;

  sdkPromise = new Promise((resolve, reject) => {
    const finishLoading = () => {
      const maps = kakaoMaps();
      if (!maps?.load) {
        reject(new Error('Kakao Maps SDK 응답을 확인할 수 없습니다.'));
        return;
      }

      maps.load(() => {
        if (!sdkReady(maps)) {
          reject(new Error('Kakao Maps services 라이브러리를 불러오지 못했습니다.'));
          return;
        }
        resolve(maps);
      });
    };

    const failLoading = () => {
      sdkPromise = undefined;
      reject(
        new Error(
          'Kakao Maps SDK를 불러오지 못했습니다. 키와 localhost:3000 등록 상태를 확인해 주세요.',
        ),
      );
    };

    const existingScript = document.getElementById(SDK_SCRIPT_ID);
    if (existingScript) {
      existingScript.addEventListener('load', finishLoading, { once: true });
      existingScript.addEventListener('error', failLoading, { once: true });
      return;
    }

    const script = document.createElement('script');
    script.id = SDK_SCRIPT_ID;
    script.async = true;
    script.src =
      `https://dapi.kakao.com/v2/maps/sdk.js?appkey=${encodeURIComponent(key)}` +
      '&autoload=false&libraries=services';
    script.addEventListener('load', finishLoading, { once: true });
    script.addEventListener('error', failLoading, { once: true });
    document.head.append(script);
  });

  return sdkPromise;
}

function mapTypeId(type) {
  const maps = requireKakaoMaps();
  const normalized = String(type ?? 'SKYVIEW').trim().toUpperCase();
  const allowedTypes = new Set(['ROADMAP', 'SKYVIEW', 'HYBRID']);
  if (!allowedTypes.has(normalized)) {
    throw new RangeError(`지원하지 않는 지도 유형입니다: ${normalized}`);
  }
  return maps.MapTypeId[normalized];
}

/**
 * Creates a Kakao map plus the marker and geocoder used by the lesson app.
 */
export function createMap(
  container,
  {
    latitude = DEFAULT_POSITION.latitude,
    longitude = DEFAULT_POSITION.longitude,
    level = 4,
    mapType = 'SKYVIEW',
  } = {},
) {
  const maps = requireKakaoMaps();
  if (!(container instanceof HTMLElement)) {
    throw new TypeError('지도 컨테이너 요소가 필요합니다.');
  }

  const position = new maps.LatLng(Number(latitude), Number(longitude));
  const map = new maps.Map(container, {
    center: position,
    level: Number(level),
    mapTypeId: mapTypeId(mapType),
  });
  const marker = new maps.Marker({ map, position });
  const geocoder = new maps.services.Geocoder();

  return { map, marker, geocoder };
}

/**
 * Converts a Korean address to WGS84 latitude/longitude using Kakao services.
 */
export function addressToCoordinates(geocoder, address) {
  const query = String(address ?? '').trim();
  if (!query) {
    return Promise.reject(new TypeError('검색할 주소를 입력해 주세요.'));
  }
  if (!geocoder?.addressSearch) {
    return Promise.reject(new TypeError('주소 검색기가 준비되지 않았습니다.'));
  }

  const maps = requireKakaoMaps();
  return new Promise((resolve, reject) => {
    geocoder.addressSearch(query, (results, status) => {
      if (status === maps.services.Status.ZERO_RESULT) {
        reject(new Error('주소를 찾지 못했습니다. 도로명이나 지번 주소를 확인해 주세요.'));
        return;
      }
      if (status !== maps.services.Status.OK) {
        reject(new Error('주소 검색 서비스 요청에 실패했습니다. 잠시 후 다시 시도해 주세요.'));
        return;
      }
      if (!results?.length) {
        reject(new Error('주소 검색 결과가 비어 있습니다. 다른 주소로 다시 시도해 주세요.'));
        return;
      }

      const first = results[0];
      const latitude = Number(first.y);
      const longitude = Number(first.x);
      if (!Number.isFinite(latitude) || !Number.isFinite(longitude)) {
        reject(new Error('주소 검색 결과의 좌표가 올바르지 않습니다.'));
        return;
      }

      resolve({
        latitude,
        longitude,
        address: first.road_address?.address_name || first.address_name || query,
        addressName: first.address_name || query,
        roadAddressName: first.road_address?.address_name || '',
      });
    });
  });
}

/** Moves both the map center and its single lesson marker. */
export function setMapPosition(
  map,
  marker,
  latitude,
  longitude,
  { level } = {},
) {
  const maps = requireKakaoMaps();
  const position = new maps.LatLng(Number(latitude), Number(longitude));
  map.setCenter(position);
  marker?.setPosition(position);
  if (Number.isFinite(Number(level))) map.setLevel(Number(level));
  return position;
}

/** Switches among ROADMAP, SKYVIEW and HYBRID through the public SDK. */
export function setMapType(map, type) {
  map.setMapTypeId(mapTypeId(type));
}

/**
 * Resolves after Kakao reports that the visible tiles have loaded.
 * The timeout keeps map operations from waiting forever while offline.
 */
export function waitForTiles(map, { timeout = 12_000, container, signal } = {}) {
  const maps = requireKakaoMaps();
  if (!map) return Promise.reject(new TypeError('지도 인스턴스가 필요합니다.'));
  if (signal?.aborted) {
    const error = new Error('지도 이미지 대기가 중단되었습니다.');
    error.name = 'AbortError';
    return Promise.reject(error);
  }

  return new Promise((resolve, reject) => {
    let settled = false;
    let imagePollTimer;
    let timer;

    const cleanup = () => {
      maps.event.removeListener(map, 'tilesloaded', handleTilesLoaded);
      clearTimeout(timer);
      clearTimeout(imagePollTimer);
      signal?.removeEventListener?.('abort', handleAbort);
    };
    const handleTilesLoaded = () => {
      if (settled) return;
      settled = true;
      cleanup();
      resolve();
    };
    const handleLoadedImages = () => {
      if (settled || !container?.querySelectorAll) return;
      const images = [...container.querySelectorAll('img')];
      if (
        images.length > 0 &&
        images.every((image) => image.complete && image.naturalWidth > 0)
      ) {
        handleTilesLoaded();
        return;
      }
      imagePollTimer = setTimeout(handleLoadedImages, 50);
    };
    const handleAbort = () => {
      if (settled) return;
      settled = true;
      cleanup();
      const error = new Error('지도 이미지 대기가 중단되었습니다.');
      error.name = 'AbortError';
      reject(error);
    };
    timer = setTimeout(() => {
      if (settled) return;
      settled = true;
      cleanup();
      reject(new Error('항공사진 로딩 시간이 초과되었습니다. 네트워크 상태를 확인해 주세요.'));
    }, Math.max(1_000, Number(timeout) || 12_000));

    maps.event.addListener(map, 'tilesloaded', handleTilesLoaded);
    signal?.addEventListener?.('abort', handleAbort, { once: true });
    imagePollTimer = setTimeout(handleLoadedImages, 250);
  });
}

/** Keeps the SDK layout in sync with responsive container changes. */
export function observeMapResize(map, container) {
  if (!map?.relayout || !(container instanceof HTMLElement)) {
    throw new TypeError('지도와 컨테이너 요소가 필요합니다.');
  }

  let frameId = 0;
  const relayout = () => {
    cancelAnimationFrame(frameId);
    frameId = requestAnimationFrame(() => map.relayout());
  };

  if (typeof ResizeObserver === 'function') {
    const observer = new ResizeObserver(relayout);
    observer.observe(container);
    return () => {
      cancelAnimationFrame(frameId);
      observer.disconnect();
    };
  }

  window.addEventListener('resize', relayout);
  return () => {
    cancelAnimationFrame(frameId);
    window.removeEventListener('resize', relayout);
  };
}
