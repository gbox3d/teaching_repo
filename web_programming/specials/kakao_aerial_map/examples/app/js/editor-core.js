export function clamp(value, minimum, maximum) {
  return Math.min(maximum, Math.max(minimum, value));
}

export function normalizeAngle(value) {
  const angle = Number(value);
  if (!Number.isFinite(angle)) return 0;
  return ((angle % 360) + 360) % 360;
}

export function fixedRotationLayout(
  width,
  totalHeight,
  protectedWidth,
  protectedHeight,
  angleDegrees,
) {
  const outputWidth = Math.round(Number(width));
  const outputHeight = Math.round(Number(totalHeight));
  if (!(outputWidth > 0) || !(outputHeight > 0)) {
    throw new RangeError('Image dimensions must be positive.');
  }

  const safeProtectedHeight = clamp(
    Math.round(Number(protectedHeight) || 0),
    0,
    outputHeight,
  );
  const safeProtectedWidth = safeProtectedHeight
    ? clamp(Math.round(Number(protectedWidth) || 0), 0, outputWidth)
    : 0;
  const radians = (normalizeAngle(angleDegrees) * Math.PI) / 180;

  return {
    outputWidth,
    outputHeight,
    editableWidth: outputWidth,
    editableHeight: outputHeight,
    centerX: outputWidth / 2,
    centerY: outputHeight / 2,
    clip: { x: 0, y: 0, width: outputWidth, height: outputHeight },
    attribution: {
      x: 0,
      y: outputHeight - safeProtectedHeight,
      width: safeProtectedWidth,
      height: safeProtectedHeight,
    },
    scale: 1,
    radians,
  };
}

export function parseCoordinates(latitudeValue, longitudeValue) {
  const latitudeText = String(latitudeValue ?? '').trim();
  const longitudeText = String(longitudeValue ?? '').trim();

  if (!latitudeText || !longitudeText) {
    throw new TypeError('위도와 경도를 모두 입력해 주세요.');
  }

  const latitude = Number(latitudeText);
  const longitude = Number(longitudeText);

  if (!Number.isFinite(latitude) || !Number.isFinite(longitude)) {
    throw new TypeError('위도와 경도는 유한한 숫자여야 합니다.');
  }
  if (latitude < -90 || latitude > 90) {
    throw new RangeError('위도는 -90부터 90 사이여야 합니다.');
  }
  if (longitude < -180 || longitude > 180) {
    throw new RangeError('경도는 -180부터 180 사이여야 합니다.');
  }

  return { latitude, longitude };
}

export function fitWithin(width, height, maximumDimension = 4096) {
  if (!(width > 0) || !(height > 0)) {
    throw new RangeError('Image dimensions must be positive.');
  }

  const scale = Math.min(1, maximumDimension / Math.max(width, height));
  return {
    width: Math.max(1, Math.round(width * scale)),
    height: Math.max(1, Math.round(height * scale)),
    scale,
  };
}

export function canvasFilter(brightness, contrast) {
  const brightnessNumber = Number(brightness);
  const contrastNumber = Number(contrast);
  const safeBrightness = Number.isFinite(brightnessNumber)
    ? clamp(brightnessNumber, 50, 150)
    : 100;
  const safeContrast = Number.isFinite(contrastNumber)
    ? clamp(contrastNumber, 50, 150)
    : 100;
  return `brightness(${safeBrightness}%) contrast(${safeContrast}%)`;
}

export function clientPointToCanvasPoint(event, canvas, editableHeight) {
  const rect = canvas.getBoundingClientRect();
  const x = ((event.clientX - rect.left) * canvas.width) / rect.width;
  const y = ((event.clientY - rect.top) * canvas.height) / rect.height;

  return {
    x: clamp(x, 0, canvas.width),
    y: clamp(y, 0, editableHeight),
    normalizedX: clamp(x / canvas.width, 0, 1),
    normalizedY: clamp(y / editableHeight, 0, 1),
    insideEditableArea: y >= 0 && y <= editableHeight,
  };
}

export function downloadFilename(extension, now = new Date()) {
  const stamp = now.toISOString().replace(/[:.]/g, '-');
  return `aerial-canvas-${stamp}.${extension}`;
}
