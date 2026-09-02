const STATIC_MAP_ORIGIN = 'https://spi.map.kakao.com';
const STATIC_MAP_PATH = '/map2/map/skyviewimageservice';
const ALLOWED_RESPONSE_TYPES = new Set(['image/png', 'image/jpeg', 'image/webp']);
const MAX_RESPONSE_BYTES = 10 * 1024 * 1024;
const ATTRIBUTION_WIDTH = 80;
const ATTRIBUTION_HEIGHT = 32;

function boundedInteger(value, name, minimum, maximum) {
  const number = Number(value);
  if (!Number.isInteger(number) || number < minimum || number > maximum) {
    throw new RangeError(`${name}은(는) ${minimum}부터 ${maximum} 사이의 정수여야 합니다.`);
  }
  return number;
}

/** Normalizes the deliberately small surface exposed by the lesson UI. */
export function normalizeStaticMapOptions({
  latitude,
  longitude,
  width = 640,
  height = 480,
  level = 4,
  timeout = 10_000,
} = {}) {
  const normalizedLatitude = Number(latitude);
  const normalizedLongitude = Number(longitude);
  if (!Number.isFinite(normalizedLatitude) || normalizedLatitude < -90 || normalizedLatitude > 90) {
    throw new RangeError('위도는 -90부터 90 사이의 숫자여야 합니다.');
  }
  if (!Number.isFinite(normalizedLongitude) || normalizedLongitude < -180 || normalizedLongitude > 180) {
    throw new RangeError('경도는 -180부터 180 사이의 숫자여야 합니다.');
  }

  return {
    latitude: normalizedLatitude,
    longitude: normalizedLongitude,
    width: boundedInteger(width, '너비', 160, 1280),
    height: boundedInteger(height, '높이', 120, 960),
    level: boundedInteger(level, '지도 레벨', 1, 14),
    timeout: boundedInteger(timeout, '대기 시간', 1_000, 30_000),
  };
}

/**
 * Accepts only the one HTTPS endpoint emitted by Kakao's SKYVIEW StaticMap.
 * Query parameters are opaque: this module neither builds nor enumerates them.
 */
export function validateStaticMapSource(source) {
  let url;
  try {
    url = new URL(String(source));
  } catch {
    throw new TypeError('Kakao 정적 지도 이미지 주소가 올바르지 않습니다.');
  }

  if (
    url.origin !== STATIC_MAP_ORIGIN ||
    url.pathname !== STATIC_MAP_PATH ||
    url.username ||
    url.password ||
    url.port ||
    url.hash
  ) {
    throw new TypeError('허용되지 않은 정적 지도 이미지 주소입니다.');
  }
  return url.href;
}

export function buildStaticImageProxyUrl(source) {
  const validatedSource = validateStaticMapSource(source);
  return `/api/kakao-static-image?source=${encodeURIComponent(validatedSource)}`;
}

function validateImageDimensions(width, height) {
  if (!(width > 0) || !(height > 0) || width * height > 2_000_000) {
    throw new RangeError('정적 지도 이미지 크기가 허용 범위를 벗어났습니다.');
  }
}

function waitForSingleImage(container, timeout) {
  return new Promise((resolve, reject) => {
    let watchedImage;
    let observer;
    let settled = false;

    const cleanup = () => {
      clearTimeout(timer);
      observer?.disconnect();
      watchedImage?.removeEventListener('load', inspect);
      watchedImage?.removeEventListener('error', handleImageError);
    };
    const finish = (callback, value) => {
      if (settled) return;
      settled = true;
      cleanup();
      callback(value);
    };
    const handleImageError = () => {
      finish(reject, new Error('Kakao 정적 지도 이미지를 불러오지 못했습니다.'));
    };
    const inspect = () => {
      const images = container.querySelectorAll('img');
      if (images.length > 1) {
        finish(reject, new Error('Kakao 정적 지도에서 단일 이미지를 확인할 수 없습니다.'));
        return;
      }
      if (images.length === 0) return;

      const image = images[0];
      if (image !== watchedImage) {
        watchedImage?.removeEventListener('load', inspect);
        watchedImage?.removeEventListener('error', handleImageError);
        watchedImage = image;
        watchedImage.addEventListener('load', inspect);
        watchedImage.addEventListener('error', handleImageError);
      }
      if (!image.src || !image.complete) return;
      if (!(image.naturalWidth > 0) || !(image.naturalHeight > 0)) {
        handleImageError();
        return;
      }
      finish(resolve, image);
    };

    const timer = setTimeout(
      () => finish(reject, new Error('Kakao 정적 지도 이미지 로딩 시간이 초과되었습니다.')),
      timeout,
    );
    observer = new MutationObserver(inspect);
    observer.observe(container, {
      childList: true,
      subtree: true,
      attributes: true,
      attributeFilter: ['src'],
    });
    inspect();
  });
}

function decodeWithImageElement(blob) {
  return new Promise((resolve, reject) => {
    const objectUrl = URL.createObjectURL(blob);
    const image = new Image();
    const cleanup = () => URL.revokeObjectURL(objectUrl);
    image.addEventListener(
      'load',
      () => {
        cleanup();
        try {
          validateImageDimensions(image.naturalWidth, image.naturalHeight);
          resolve({
            image,
            width: image.naturalWidth,
            height: image.naturalHeight,
            close() {},
          });
        } catch (error) {
          reject(error);
        }
      },
      { once: true },
    );
    image.addEventListener(
      'error',
      () => {
        cleanup();
        reject(new Error('정적 지도 이미지 응답을 해석하지 못했습니다.'));
      },
      { once: true },
    );
    image.decoding = 'async';
    image.src = objectUrl;
  });
}

/** Exported for deterministic decoder tests; normal callers use createKakaoStaticImage. */
export async function decodeStaticImageBlob(blob) {
  if (!(blob instanceof Blob) || !ALLOWED_RESPONSE_TYPES.has(blob.type.toLowerCase())) {
    throw new TypeError('프록시가 지원되는 이미지 형식으로 응답하지 않았습니다.');
  }
  if (!(blob.size > 0) || blob.size > MAX_RESPONSE_BYTES) {
    throw new RangeError('정적 지도 이미지 응답 크기가 허용 범위를 벗어났습니다.');
  }

  if (typeof createImageBitmap !== 'function') return decodeWithImageElement(blob);

  let image;
  try {
    image = await createImageBitmap(blob);
    validateImageDimensions(image.width, image.height);
    return {
      image,
      width: image.width,
      height: image.height,
      close: () => image.close(),
    };
  } catch (error) {
    image?.close?.();
    throw error;
  }
}

function createOffscreenContainer(width, height) {
  const container = document.createElement('div');
  container.setAttribute('aria-hidden', 'true');
  Object.assign(container.style, {
    position: 'fixed',
    left: '-10000px',
    top: '0',
    width: `${width}px`,
    height: `${height}px`,
    overflow: 'hidden',
    opacity: '0',
    pointerEvents: 'none',
    zIndex: '-1',
  });
  document.body.append(container);
  return container;
}

/**
 * Asks the loaded official Kakao SDK for one SKYVIEW StaticMap, then sends only
 * that SDK-emitted URL to the same-origin image proxy for Canvas-safe decoding.
 */
export async function createKakaoStaticImage(options) {
  const normalized = normalizeStaticMapOptions(options);
  const maps = globalThis.kakao?.maps;
  if (!maps?.StaticMap || !maps?.LatLng || !maps?.MapTypeId?.SKYVIEW) {
    throw new Error('Kakao Maps SDK가 아직 준비되지 않았습니다.');
  }

  const container = createOffscreenContainer(normalized.width, normalized.height);
  try {
    new maps.StaticMap(container, {
      center: new maps.LatLng(normalized.latitude, normalized.longitude),
      level: normalized.level,
      mapTypeId: maps.MapTypeId.SKYVIEW,
    });

    const staticImage = await waitForSingleImage(container, normalized.timeout);
    const source = validateStaticMapSource(staticImage.currentSrc || staticImage.src);
    const controller = new AbortController();
    const abortTimer = setTimeout(() => controller.abort(), normalized.timeout);
    let response;
    try {
      response = await fetch(buildStaticImageProxyUrl(source), {
        method: 'GET',
        credentials: 'same-origin',
        cache: 'no-store',
        redirect: 'error',
        signal: controller.signal,
      });
    } catch (error) {
      if (error?.name === 'AbortError') {
        throw new Error('정적 지도 이미지 요청 시간이 초과되었습니다.');
      }
      throw new Error('정적 지도 이미지 프록시에 연결하지 못했습니다.', { cause: error });
    } finally {
      clearTimeout(abortTimer);
    }

    if (!response.ok) {
      throw new Error(`정적 지도 이미지를 받지 못했습니다. (HTTP ${response.status})`);
    }
    const decoded = await decodeStaticImageBlob(await response.blob());
    if (decoded.width !== normalized.width || decoded.height !== normalized.height) {
      decoded.close();
      throw new Error('정적 지도 이미지의 크기가 요청한 크기와 다릅니다.');
    }

    return {
      ...decoded,
      attributionWidth: Math.min(ATTRIBUTION_WIDTH, decoded.width),
      attributionHeight: Math.min(ATTRIBUTION_HEIGHT, decoded.height),
      label: 'Kakao StaticMap 항공사진',
    };
  } finally {
    container.remove();
  }
}
