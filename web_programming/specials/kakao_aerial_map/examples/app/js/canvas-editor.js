import {
  canvasFilter,
  clamp,
  clientPointToCanvasPoint,
  downloadFilename,
  fitWithin,
  fixedRotationLayout,
  normalizeAngle,
} from './editor-core.js';

const DEFAULT_MAX_DIMENSION = 3072;
const DEFAULT_MAX_PIXELS = 12_000_000;
const MAX_TEXT_LENGTH = 80;
const MAX_ACTIONS = 200;
const MAX_STROKE_POINTS = 4_096;

function createCanvas(width, height) {
  const canvas = document.createElement('canvas');
  canvas.width = width;
  canvas.height = height;
  return canvas;
}

function context2d(canvas) {
  const context = canvas.getContext('2d', {
    alpha: true,
    willReadFrequently: false,
  });
  if (!context) {
    throw new Error('이 브라우저에서는 Canvas 2D를 사용할 수 없습니다.');
  }
  context.imageSmoothingEnabled = true;
  context.imageSmoothingQuality = 'high';
  return context;
}

function sourceDimension(source, names) {
  for (const name of names) {
    const value = Number(source?.[name]);
    if (Number.isFinite(value) && value > 0) return Math.round(value);
  }
  return 0;
}

function importSize(width, height, maximumDimension, maximumPixels) {
  const bounded = fitWithin(width, height, maximumDimension);
  const boundedPixels = bounded.width * bounded.height;
  if (boundedPixels <= maximumPixels) return bounded;

  const pixelScale = Math.sqrt(maximumPixels / boundedPixels);
  return {
    width: Math.max(1, Math.floor(bounded.width * pixelScale)),
    height: Math.max(1, Math.floor(bounded.height * pixelScale)),
    scale: bounded.scale * pixelScale,
  };
}

function signedAngle(value, fallback = 0) {
  const number = Number(value);
  if (!Number.isFinite(number)) return fallback;
  const normalized = normalizeAngle(number);
  return normalized > 180 ? normalized - 360 : normalized;
}

function finiteOr(value, fallback) {
  const number = Number(value);
  return Number.isFinite(number) ? number : fallback;
}

function safeColor(value, fallback) {
  if (typeof value !== 'string') return fallback;
  const candidate = value.trim();
  if (!candidate) return fallback;

  if (globalThis.CSS?.supports?.('color', candidate)) return candidate;
  return /^#[0-9a-f]{3,8}$/iu.test(candidate) ? candidate : fallback;
}

function canvasToBlob(canvas, type, quality) {
  return new Promise((resolve, reject) => {
    canvas.toBlob(
      (blob) => {
        if (blob) resolve(blob);
        else reject(new Error('이미지 파일을 만들지 못했습니다.'));
      },
      type,
      quality,
    );
  });
}

export class CanvasEditor {
  constructor(
    canvas,
    {
      onChange = null,
      maxDimension = DEFAULT_MAX_DIMENSION,
      maxPixels = DEFAULT_MAX_PIXELS,
    } = {},
  ) {
    if (!(canvas instanceof HTMLCanvasElement)) {
      throw new TypeError('CanvasEditor에는 HTMLCanvasElement가 필요합니다.');
    }

    this.canvas = canvas;
    this.context = context2d(canvas);
    this.onChange = typeof onChange === 'function' ? onChange : null;
    this.maxDimension = clamp(
      Math.round(finiteOr(maxDimension, DEFAULT_MAX_DIMENSION)),
      512,
      4096,
    );
    this.maxPixels = clamp(
      Math.round(finiteOr(maxPixels, DEFAULT_MAX_PIXELS)),
      1_000_000,
      16_000_000,
    );

    this.contentCanvas = null;
    this.attributionCanvas = null;
    this.label = '';
    this.sourceWidth = 0;
    this.sourceHeight = 0;
    this.importScale = 1;

    this.rotation = 0;
    this.brightness = 100;
    this.contrast = 100;
    this.drawing = false;
    this.brushColor = '#ff3b30';
    this.brushSize = 6;
    this.actions = [];
    this.currentStroke = null;
    this.activePointerId = null;
    this.geometry = null;

    this.boundPointerDown = this.handlePointerDown.bind(this);
    this.boundPointerMove = this.handlePointerMove.bind(this);
    this.boundPointerEnd = this.handlePointerEnd.bind(this);
    this.boundPointerCancel = this.handlePointerCancel.bind(this);

    canvas.addEventListener('pointerdown', this.boundPointerDown);
    canvas.addEventListener('pointermove', this.boundPointerMove);
    canvas.addEventListener('pointerup', this.boundPointerEnd);
    canvas.addEventListener('pointercancel', this.boundPointerCancel);
    canvas.addEventListener('lostpointercapture', this.boundPointerCancel);
    canvas.dataset.drawing = 'false';
  }

  get hasSource() {
    return Boolean(this.contentCanvas);
  }

  get canUndo() {
    return this.actions.length > 0 || Boolean(this.currentStroke);
  }

  get state() {
    return {
      hasSource: this.hasSource,
      canUndo: this.canUndo,
      drawing: this.drawing,
      label: this.label,
      rotation: this.rotation,
      brightness: this.brightness,
      contrast: this.contrast,
      brushColor: this.brushColor,
      brushSize: this.brushSize,
      actionCount: this.actions.length,
      width: this.hasSource ? this.canvas.width : 0,
      height: this.hasSource ? this.canvas.height : 0,
      editableHeight: this.geometry?.editableHeight ?? 0,
      protectedWidth: this.attributionCanvas?.width ?? 0,
      protectedHeight: this.attributionCanvas?.height ?? 0,
      sourceWidth: this.sourceWidth,
      sourceHeight: this.sourceHeight,
      importScale: this.importScale,
    };
  }

  async setSource(
    source,
    {
      attributionWidth = 0,
      attributionHeight = 0,
      label = '',
      close = false,
    } = {},
  ) {
    const sourceWidth = sourceDimension(source, [
      'videoWidth',
      'naturalWidth',
      'width',
    ]);
    const sourceHeight = sourceDimension(source, [
      'videoHeight',
      'naturalHeight',
      'height',
    ]);

    if (!(sourceWidth > 0) || !(sourceHeight > 0)) {
      throw new RangeError('불러올 이미지의 크기를 확인할 수 없습니다.');
    }

    const sourceBadgeHeight = clamp(
      Math.round(finiteOr(attributionHeight, 0)),
      0,
      sourceHeight,
    );
    const sourceBadgeWidth = sourceBadgeHeight
      ? clamp(
          Math.round(finiteOr(attributionWidth, 0)) || sourceWidth,
          1,
          sourceWidth,
        )
      : 0;
    const size = importSize(
      sourceWidth,
      sourceHeight,
      this.maxDimension,
      this.maxPixels,
    );
    if (sourceBadgeHeight > 0 && size.scale < 1) {
      throw new RangeError(
        '출처 표시를 원본 픽셀로 보존하려면 지도 영역을 더 작게 표시한 뒤 다시 가져와 주세요.',
      );
    }
    const scaledBadgeWidth = sourceBadgeWidth
      ? clamp(
          Math.max(1, Math.round(sourceBadgeWidth * size.scale)),
          1,
          size.width,
        )
      : 0;
    const scaledBadgeHeight = sourceBadgeHeight
      ? clamp(
          Math.max(1, Math.round(sourceBadgeHeight * size.scale)),
          1,
          size.height,
        )
      : 0;

    const nextContentCanvas = createCanvas(size.width, size.height);
    const contentContext = context2d(nextContentCanvas);
    let nextAttributionCanvas = null;

    try {
      contentContext.drawImage(
        source,
        0,
        0,
        sourceWidth,
        sourceHeight,
        0,
        0,
        size.width,
        size.height,
      );

      if (scaledBadgeWidth > 0 && scaledBadgeHeight > 0) {
        nextAttributionCanvas = createCanvas(
          scaledBadgeWidth,
          scaledBadgeHeight,
        );
        const attributionContext = context2d(nextAttributionCanvas);
        attributionContext.drawImage(
          source,
          0,
          sourceHeight - sourceBadgeHeight,
          sourceBadgeWidth,
          sourceBadgeHeight,
          0,
          0,
          scaledBadgeWidth,
          scaledBadgeHeight,
        );
        attributionContext.getImageData(0, 0, 1, 1);
      }

      // Fail early with a clear import error instead of discovering a tainted
      // canvas only when the student tries to download the result.
      contentContext.getImageData(0, 0, 1, 1);
    } catch (error) {
      if (error?.name === 'SecurityError') {
        throw new DOMException(
          '브라우저 보안 정책상 외부 URL 이미지는 편집할 수 없습니다. 동일 출처 이미지나 로컬 파일을 사용해 주세요.',
          'SecurityError',
        );
      }
      throw error;
    } finally {
      if (close && typeof source?.close === 'function') source.close();
    }

    this.contentCanvas = nextContentCanvas;
    this.attributionCanvas = nextAttributionCanvas;
    this.label = String(label ?? '').slice(0, 200);
    this.sourceWidth = sourceWidth;
    this.sourceHeight = sourceHeight;
    this.importScale = size.scale;
    this.rotation = 0;
    this.brightness = 100;
    this.contrast = 100;
    this.drawing = false;
    this.actions = [];
    this.cancelCurrentStroke();
    this.canvas.dataset.drawing = 'false';

    this.render();
    this.emitChange();
    return this.state;
  }

  setTransform({ rotation, brightness, contrast } = {}) {
    if (rotation !== undefined) {
      this.rotation = signedAngle(rotation, this.rotation);
    }
    if (brightness !== undefined) {
      this.brightness = clamp(
        finiteOr(brightness, this.brightness),
        50,
        150,
      );
    }
    if (contrast !== undefined) {
      this.contrast = clamp(finiteOr(contrast, this.contrast), 50, 150);
    }

    if (this.hasSource) this.render();
    this.emitChange();
    return this.state;
  }

  setDrawing(enabled) {
    this.drawing = Boolean(enabled) && this.hasSource;
    if (!this.drawing) this.finishCurrentStroke();
    this.canvas.dataset.drawing = String(this.drawing);
    this.emitChange();
    return this.drawing;
  }

  setBrush({ color, size } = {}) {
    if (color !== undefined) {
      this.brushColor = safeColor(color, this.brushColor);
    }
    if (size !== undefined) {
      this.brushSize = clamp(finiteOr(size, this.brushSize), 1, 64);
    }
    this.emitChange();
    return { color: this.brushColor, size: this.brushSize };
  }

  addText(text) {
    if (!this.hasSource) return false;
    const value = String(text ?? '').trim().slice(0, MAX_TEXT_LENGTH);
    if (!value) return false;

    this.finishCurrentStroke();
    this.appendAction({
      type: 'text',
      text: value,
      x: 0.5,
      y: 0.5,
      color: this.brushColor,
      fontScale: 0.065,
    });
    this.render();
    this.emitChange();
    return true;
  }

  undo() {
    if (!this.hasSource) return false;
    if (this.currentStroke) {
      this.cancelCurrentStroke();
      this.render();
      this.emitChange();
      return true;
    }
    if (!this.actions.length) return false;

    this.actions.pop();
    this.render();
    this.emitChange();
    return true;
  }

  reset() {
    if (!this.hasSource) return this.state;
    this.rotation = 0;
    this.brightness = 100;
    this.contrast = 100;
    this.drawing = false;
    this.actions = [];
    this.cancelCurrentStroke();
    this.canvas.dataset.drawing = 'false';
    this.render();
    this.emitChange();
    return this.state;
  }

  async toBlob(format = 'png') {
    if (!this.hasSource) {
      throw new Error('먼저 편집할 이미지를 불러와 주세요.');
    }

    const normalizedFormat = String(format).toLowerCase();
    if (normalizedFormat !== 'png' && normalizedFormat !== 'jpeg') {
      throw new TypeError("저장 형식은 'png' 또는 'jpeg'여야 합니다.");
    }

    this.render();

    let exportCanvas = this.canvas;
    let mimeType = 'image/png';
    let quality;
    if (normalizedFormat === 'jpeg') {
      exportCanvas = createCanvas(this.canvas.width, this.canvas.height);
      const exportContext = context2d(exportCanvas);
      exportContext.fillStyle = '#ffffff';
      exportContext.fillRect(0, 0, exportCanvas.width, exportCanvas.height);
      exportContext.drawImage(this.canvas, 0, 0);
      mimeType = 'image/jpeg';
      quality = 0.92;
    }

    return canvasToBlob(exportCanvas, mimeType, quality);
  }

  async download(format = 'png') {
    const normalizedFormat = String(format).toLowerCase();
    const blob = await this.toBlob(normalizedFormat);
    const filename = downloadFilename(normalizedFormat);
    const objectUrl = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = objectUrl;
    link.download = filename;
    link.hidden = true;
    document.body.append(link);

    try {
      link.click();
    } finally {
      link.remove();
      setTimeout(() => URL.revokeObjectURL(objectUrl), 0);
    }

    return filename;
  }

  render() {
    if (!this.hasSource) return;

    const contentWidth = this.contentCanvas.width;
    const contentHeight = this.contentCanvas.height;
    const protectedWidth = this.attributionCanvas?.width ?? 0;
    const protectedHeight = this.attributionCanvas?.height ?? 0;
    const layout = fixedRotationLayout(
      contentWidth,
      contentHeight,
      protectedWidth,
      protectedHeight,
      this.rotation,
    );
    const { outputWidth, outputHeight } = layout;

    if (
      this.canvas.width !== outputWidth ||
      this.canvas.height !== outputHeight
    ) {
      this.canvas.width = outputWidth;
      this.canvas.height = outputHeight;
      this.context = context2d(this.canvas);
    }

    const context = this.context;

    context.save();
    context.setTransform(1, 0, 0, 1, 0, 0);
    context.clearRect(0, 0, outputWidth, outputHeight);
    context.beginPath();
    context.rect(
      layout.clip.x,
      layout.clip.y,
      layout.clip.width,
      layout.clip.height,
    );
    context.clip();
    context.translate(layout.centerX, layout.centerY);
    context.rotate(layout.radians);
    context.translate(-contentWidth / 2, -contentHeight / 2);
    context.beginPath();
    context.rect(0, 0, contentWidth, contentHeight);
    context.clip();
    context.filter = canvasFilter(this.brightness, this.contrast);
    context.drawImage(this.contentCanvas, 0, 0);
    context.filter = 'none';
    this.drawActions(context, contentWidth, contentHeight);
    context.restore();

    // Redraw only the source badge outside the transform, filter, and annotation
    // stack. The full-width map remains visually continuous while attribution
    // stays readable at its original pixels.
    if (this.attributionCanvas) {
      context.save();
      context.setTransform(1, 0, 0, 1, 0, 0);
      context.globalAlpha = 1;
      context.globalCompositeOperation = 'source-over';
      context.filter = 'none';
      context.imageSmoothingEnabled = false;
      context.drawImage(
        this.attributionCanvas,
        layout.attribution.x,
        layout.attribution.y,
      );
      context.restore();
    }

    this.geometry = {
      centerX: layout.centerX,
      centerY: layout.centerY,
      contentWidth,
      contentHeight,
      editableHeight: layout.editableHeight,
      radians: layout.radians,
    };
  }

  drawActions(context, width, height) {
    for (const action of this.actions) {
      this.drawAction(context, action, width, height);
    }
    if (this.currentStroke) {
      this.drawAction(context, this.currentStroke, width, height);
    }
  }

  drawAction(context, action, width, height) {
    if (action.type === 'stroke') {
      if (!action.points.length) return;
      context.save();
      context.strokeStyle = action.color;
      context.fillStyle = action.color;
      context.lineWidth = Math.max(
        1,
        action.sizeScale * Math.min(width, height),
      );
      context.lineCap = 'round';
      context.lineJoin = 'round';
      context.beginPath();
      const first = action.points[0];
      context.moveTo(first.x * width, first.y * height);
      for (let index = 1; index < action.points.length; index += 1) {
        const point = action.points[index];
        context.lineTo(point.x * width, point.y * height);
      }
      if (action.points.length === 1) {
        context.arc(
          first.x * width,
          first.y * height,
          context.lineWidth / 2,
          0,
          Math.PI * 2,
        );
        context.fill();
      } else {
        context.stroke();
      }
      context.restore();
      return;
    }

    if (action.type === 'text') {
      context.save();
      let fontSize = clamp(
        Math.round(action.fontScale * Math.min(width, height)),
        16,
        180,
      );
      context.font = `700 ${fontSize}px Pretendard, "Noto Sans KR", "Malgun Gothic", sans-serif`;
      const maximumWidth = width * 0.9;
      const measuredWidth = context.measureText(action.text).width;
      if (measuredWidth > maximumWidth) {
        fontSize = Math.max(12, Math.floor(fontSize * (maximumWidth / measuredWidth)));
        context.font = `700 ${fontSize}px Pretendard, "Noto Sans KR", "Malgun Gothic", sans-serif`;
      }
      context.textAlign = 'center';
      context.textBaseline = 'middle';
      context.lineJoin = 'round';
      context.lineWidth = Math.max(2, fontSize * 0.09);
      context.strokeStyle = 'rgb(0 0 0 / 72%)';
      context.fillStyle = action.color;
      const x = action.x * width;
      const y = action.y * height;
      context.strokeText(action.text, x, y, maximumWidth);
      context.fillText(action.text, x, y, maximumWidth);
      context.restore();
    }
  }

  eventToContentPoint(event) {
    if (!this.geometry || !this.hasSource) return null;
    const rect = this.canvas.getBoundingClientRect();
    if (!(rect.width > 0) || !(rect.height > 0)) return null;

    const canvasPoint = clientPointToCanvasPoint(
      event,
      this.canvas,
      this.geometry.editableHeight,
    );
    const outputY =
      ((event.clientY - rect.top) * this.canvas.height) / rect.height;
    if (
      !canvasPoint.insideEditableArea ||
      outputY < 0 ||
      outputY >= this.geometry.editableHeight
    ) {
      return null;
    }

    const outputX =
      ((event.clientX - rect.left) * this.canvas.width) / rect.width;
    const translatedX = outputX - this.geometry.centerX;
    const translatedY = outputY - this.geometry.centerY;
    const cosine = Math.cos(this.geometry.radians);
    const sine = Math.sin(this.geometry.radians);
    const sourceX =
      translatedX * cosine +
      translatedY * sine +
      this.geometry.contentWidth / 2;
    const sourceY =
      -translatedX * sine +
      translatedY * cosine +
      this.geometry.contentHeight / 2;

    if (
      sourceX < 0 ||
      sourceX > this.geometry.contentWidth ||
      sourceY < 0 ||
      sourceY > this.geometry.contentHeight
    ) {
      return null;
    }

    return {
      x: clamp(sourceX / this.geometry.contentWidth, 0, 1),
      y: clamp(sourceY / this.geometry.contentHeight, 0, 1),
    };
  }

  handlePointerDown(event) {
    if (!this.drawing || !this.hasSource || event.button !== 0) return;
    const point = this.eventToContentPoint(event);
    if (!point) return;

    event.preventDefault();
    this.finishCurrentStroke();
    this.activePointerId = event.pointerId;
    this.currentStroke = {
      type: 'stroke',
      color: this.brushColor,
      sizeScale:
        this.brushSize /
        Math.max(1, Math.min(this.contentCanvas.width, this.contentCanvas.height)),
      points: [point],
    };
    this.canvas.setPointerCapture?.(event.pointerId);
    this.render();
  }

  handlePointerMove(event) {
    if (
      this.activePointerId !== event.pointerId ||
      !this.currentStroke ||
      !this.drawing
    ) {
      return;
    }

    event.preventDefault();
    const events = event.getCoalescedEvents?.() ?? [event];
    let changed = false;
    for (const sample of events) {
      if (this.currentStroke.points.length >= MAX_STROKE_POINTS) break;
      const point = this.eventToContentPoint(sample);
      if (!point) continue;
      const previous = this.currentStroke.points.at(-1);
      const distance = Math.hypot(point.x - previous.x, point.y - previous.y);
      if (distance < 0.0005) continue;
      this.currentStroke.points.push(point);
      changed = true;
    }
    if (changed) this.render();
  }

  handlePointerEnd(event) {
    if (this.activePointerId !== event.pointerId) return;
    event.preventDefault();
    this.finishCurrentStroke();
    if (this.canvas.hasPointerCapture?.(event.pointerId)) {
      this.canvas.releasePointerCapture(event.pointerId);
    }
  }

  handlePointerCancel(event) {
    if (this.activePointerId !== event.pointerId) return;
    this.cancelCurrentStroke();
    if (this.hasSource) this.render();
    this.emitChange();
  }

  finishCurrentStroke() {
    if (!this.currentStroke) {
      this.activePointerId = null;
      return false;
    }

    if (this.currentStroke.points.length) {
      this.appendAction(this.currentStroke);
    }
    this.currentStroke = null;
    this.activePointerId = null;
    if (this.hasSource) this.render();
    this.emitChange();
    return true;
  }

  appendAction(action) {
    if (this.actions.length >= MAX_ACTIONS) this.actions.shift();
    this.actions.push(action);
  }

  cancelCurrentStroke() {
    this.currentStroke = null;
    this.activePointerId = null;
  }

  emitChange() {
    if (!this.onChange) return;
    try {
      this.onChange(this.state);
    } catch (error) {
      console.error('CanvasEditor onChange callback failed.', error);
    }
  }

  destroy() {
    this.cancelCurrentStroke();
    this.canvas.removeEventListener('pointerdown', this.boundPointerDown);
    this.canvas.removeEventListener('pointermove', this.boundPointerMove);
    this.canvas.removeEventListener('pointerup', this.boundPointerEnd);
    this.canvas.removeEventListener('pointercancel', this.boundPointerCancel);
    this.canvas.removeEventListener('lostpointercapture', this.boundPointerCancel);
  }
}

export default CanvasEditor;
