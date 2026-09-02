const STATIC_MAP_ORIGIN = 'https://spi.map.kakao.com';
const STATIC_MAP_PATH = '/map2/map/skyviewimageservice';
const REQUIRED_PARAMETERS = Object.freeze([
  'IW',
  'IH',
  'MX',
  'MY',
  'SCALE',
  'service',
]);
const OPTIONAL_PARAMETERS = Object.freeze(['CX', 'CY']);
const ALLOWED_PARAMETERS = new Set([...REQUIRED_PARAMETERS, ...OPTIONAL_PARAMETERS]);
const ALLOWED_CONTENT_TYPES = new Set(['image/jpeg', 'image/png']);

function singleParameter(url, name) {
  const values = url.searchParams.getAll(name);
  if (values.length !== 1 || !values[0]) {
    throw new TypeError(`정적 지도 URL의 ${name} 값이 올바르지 않습니다.`);
  }
  return values[0];
}

function finiteParameter(url, name) {
  const value = Number(singleParameter(url, name));
  if (!Number.isFinite(value)) {
    throw new TypeError(`정적 지도 URL의 ${name} 값은 숫자여야 합니다.`);
  }
  return value;
}

async function readBoundedBody(response, maximumBytes) {
  if (!response.body?.getReader) {
    const body = Buffer.from(await response.arrayBuffer());
    if (!(body.length > 0) || body.length > maximumBytes) {
      throw new RangeError('Kakao 정적 지도 이미지 크기가 올바르지 않습니다.');
    }
    return body;
  }

  const reader = response.body.getReader();
  const chunks = [];
  let totalBytes = 0;
  try {
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      totalBytes += value.byteLength;
      if (totalBytes > maximumBytes) {
        await reader.cancel();
        throw new RangeError('Kakao 정적 지도 이미지 크기가 올바르지 않습니다.');
      }
      chunks.push(Buffer.from(value));
    }
  } finally {
    reader.releaseLock();
  }

  if (!(totalBytes > 0)) {
    throw new RangeError('Kakao 정적 지도 이미지 크기가 올바르지 않습니다.');
  }
  return Buffer.concat(chunks, totalBytes);
}

/** Accepts only a single SKYVIEW image URL created by Kakao's public StaticMap SDK. */
export function validateKakaoStaticImageUrl(value) {
  const source = String(value ?? '').trim();
  if (!source || source.length > 2_048) {
    throw new TypeError('정적 지도 이미지 URL이 없거나 너무 깁니다.');
  }

  let url;
  try {
    url = new URL(source);
  } catch {
    throw new TypeError('정적 지도 이미지 URL 형식이 올바르지 않습니다.');
  }

  if (
    url.origin !== STATIC_MAP_ORIGIN ||
    url.pathname !== STATIC_MAP_PATH ||
    url.username ||
    url.password ||
    url.hash
  ) {
    throw new TypeError('허용된 Kakao SKYVIEW 정적 이미지 주소가 아닙니다.');
  }

  for (const name of url.searchParams.keys()) {
    if (!ALLOWED_PARAMETERS.has(name)) {
      throw new TypeError(`허용되지 않은 정적 지도 파라미터입니다: ${name}`);
    }
  }
  for (const name of REQUIRED_PARAMETERS) singleParameter(url, name);

  for (const name of ['IW', 'IH']) {
    const dimension = finiteParameter(url, name);
    if (!Number.isInteger(dimension) || dimension < 1 || dimension > 2_048) {
      throw new RangeError(`${name}는 1~2048 정수여야 합니다.`);
    }
  }
  for (const name of ['MX', 'MY']) finiteParameter(url, name);
  for (const name of OPTIONAL_PARAMETERS) {
    if (url.searchParams.has(name)) finiteParameter(url, name);
  }

  const scale = finiteParameter(url, 'SCALE');
  if (!(scale > 0)) throw new RangeError('SCALE은 0보다 커야 합니다.');
  if (singleParameter(url, 'service') !== 'open') {
    throw new TypeError('Kakao 공개 지도 서비스 URL만 사용할 수 있습니다.');
  }

  return url;
}

export async function relayKakaoStaticImage(
  source,
  {
    fetchImpl = globalThis.fetch,
    timeout = 10_000,
    maximumBytes = 8 * 1024 * 1024,
  } = {},
) {
  if (typeof fetchImpl !== 'function') {
    throw new TypeError('서버의 fetch 구현이 필요합니다.');
  }

  const url = validateKakaoStaticImageUrl(source);
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeout);

  try {
    const response = await fetchImpl(url, {
      method: 'GET',
      redirect: 'error',
      signal: controller.signal,
      headers: {
        accept: 'image/jpeg,image/png',
        referer: 'http://localhost:3000/',
        'user-agent': 'KakaoAerialCanvasLab/1.0',
      },
    });
    if (!response.ok) {
      throw new Error(`Kakao 정적 지도 응답 오류: HTTP ${response.status}`);
    }

    const contentType = String(response.headers.get('content-type') ?? '')
      .split(';', 1)[0]
      .trim()
      .toLowerCase();
    if (!ALLOWED_CONTENT_TYPES.has(contentType)) {
      throw new TypeError('Kakao 정적 지도 응답이 이미지가 아닙니다.');
    }

    const announcedLength = Number(response.headers.get('content-length'));
    if (Number.isFinite(announcedLength) && announcedLength > maximumBytes) {
      throw new RangeError('Kakao 정적 지도 이미지가 허용 크기를 초과했습니다.');
    }

    const body = await readBoundedBody(response, maximumBytes);

    return { body, contentType };
  } finally {
    clearTimeout(timer);
  }
}
