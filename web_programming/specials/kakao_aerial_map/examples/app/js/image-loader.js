const MAX_FILE_BYTES = 20 * 1024 * 1024;
const MAX_IMAGE_PIXELS = 24_000_000;
const MAX_IMAGE_DIMENSION = 16_384;
const ALLOWED_IMAGE_TYPES = new Set(['image/png', 'image/jpeg', 'image/webp']);

function waitForEvent(target, eventName, timeout, errorMessage) {
  return new Promise((resolve, reject) => {
    const timer = setTimeout(() => {
      cleanup();
      reject(new Error(errorMessage));
    }, timeout);
    const handleEvent = () => {
      cleanup();
      resolve();
    };
    const cleanup = () => {
      clearTimeout(timer);
      target.removeEventListener(eventName, handleEvent);
    };

    target.addEventListener(eventName, handleEvent, { once: true });
  });
}

function validateDecodedDimensions(width, height) {
  if (!(width > 0) || !(height > 0)) {
    throw new Error('이미지 크기를 확인할 수 없습니다.');
  }
  if (
    width > MAX_IMAGE_DIMENSION ||
    height > MAX_IMAGE_DIMENSION ||
    width * height > MAX_IMAGE_PIXELS
  ) {
    throw new RangeError('이미지는 최대 2,400만 화소, 한 변 16,384px까지 사용할 수 있습니다.');
  }
}

function safeFileLabel(file) {
  return String(file.name || '로컬 이미지').replace(/[\u0000-\u001f]/g, '').slice(0, 120);
}

async function decodeWithImageElement(file) {
  const objectUrl = URL.createObjectURL(file);
  try {
    const image = new Image();
    image.decoding = 'async';
    image.src = objectUrl;
    if (typeof image.decode === 'function') {
      await image.decode();
    } else {
      await waitForEvent(image, 'load', 10_000, '이미지 파일을 읽지 못했습니다.');
    }
    validateDecodedDimensions(image.naturalWidth, image.naturalHeight);
    return {
      image,
      width: image.naturalWidth,
      height: image.naturalHeight,
      attributionHeight: 0,
      label: safeFileLabel(file),
      close() {},
    };
  } finally {
    URL.revokeObjectURL(objectUrl);
  }
}

/** Decodes a local PNG/JPEG/WebP without uploading or fetching any URL. */
export async function loadImageFile(file) {
  if (!(file instanceof Blob)) {
    throw new TypeError('로컬 이미지 파일을 선택해 주세요.');
  }
  const type = String(file.type || '').toLowerCase();
  if (!ALLOWED_IMAGE_TYPES.has(type)) {
    throw new TypeError('PNG, JPEG, WebP 이미지만 사용할 수 있습니다.');
  }
  if (!(file.size > 0) || file.size > MAX_FILE_BYTES) {
    throw new RangeError('이미지 파일 크기는 20MB 이하여야 합니다.');
  }

  if (typeof createImageBitmap !== 'function') {
    return decodeWithImageElement(file);
  }

  let image;
  try {
    image = await createImageBitmap(file);
    validateDecodedDimensions(image.width, image.height);
    return {
      image,
      width: image.width,
      height: image.height,
      attributionHeight: 0,
      label: safeFileLabel(file),
      close: () => image.close(),
    };
  } catch (error) {
    image?.close();
    if (error instanceof RangeError) throw error;
    throw new Error('선택한 이미지 파일을 해석하지 못했습니다.', { cause: error });
  }
}
