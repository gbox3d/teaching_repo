import { CanvasEditor } from './canvas-editor.js';
import { createCollaborationBridge } from './collaboration-bridge.js';
import { loadImageFile } from './image-loader.js';
import { parseCoordinates } from './editor-core.js';
import { createKakaoStaticImage } from './static-map.js';
import {
  addressToCoordinates,
  createMap,
  loadKakaoMaps,
  observeMapResize,
  setMapPosition,
  setMapType,
  waitForTiles,
} from './map.js';

const $ = (selector) => {
  const element = document.querySelector(selector);
  if (!element) throw new Error(`Required element not found: ${selector}`);
  return element;
};

const elements = {
  status: $('#app-status'),
  map: $('#map'),
  mapSetup: $('#map-setup'),
  mapType: $('#map-type'),
  addressForm: $('#address-form'),
  address: $('#address'),
  addressSubmit: $('#address-submit'),
  coordinateForm: $('#coordinate-form'),
  latitude: $('#latitude'),
  longitude: $('#longitude'),
  coordinateSubmit: $('#coordinate-submit'),
  gpsButton: $('#gps-button'),
  locationSummary: $('#location-summary'),
  staticImageButton: $('#static-image-button'),
  imageFile: $('#image-file'),
  canvas: $('#editor-canvas'),
  canvasEmpty: $('#canvas-empty'),
  imageSummary: $('#image-summary'),
  attributionNote: $('#attribution-note'),
  rotation: $('#rotation'),
  rotationOutput: $('#rotation-output'),
  brightness: $('#brightness'),
  brightnessOutput: $('#brightness-output'),
  contrast: $('#contrast'),
  contrastOutput: $('#contrast-output'),
  brushColor: $('#brush-color'),
  brushSize: $('#brush-size'),
  drawToggle: $('#draw-toggle'),
  annotationText: $('#annotation-text'),
  addText: $('#add-text'),
  undoButton: $('#undo-button'),
  resetButton: $('#reset-button'),
  downloadPng: $('#download-png'),
  downloadJpeg: $('#download-jpeg'),
  collaborationState: $('#collaboration-state'),
  collaborationLog: $('#collaboration-log'),
};

const mapControlElements = [
  elements.mapType,
  elements.addressSubmit,
  elements.coordinateSubmit,
  elements.gpsButton,
];

const editorControlElements = [
  elements.rotation,
  elements.brightness,
  elements.contrast,
  elements.brushColor,
  elements.brushSize,
  elements.drawToggle,
  elements.annotationText,
  elements.addText,
  elements.resetButton,
  elements.downloadPng,
  elements.downloadJpeg,
];

let mapController = null;
let mapBusy = false;
let mapReady = false;
let staticImageBusy = false;
let currentImageKind = 'none';
let editor = null;
let collaborationBridge = null;

function setStatus(message, kind = 'info') {
  elements.status.textContent = message;
  elements.status.dataset.kind = kind;
  elements.status.setAttribute('role', kind === 'error' ? 'alert' : 'status');
}

function setMapControlsEnabled(enabled) {
  for (const control of mapControlElements) {
    control.disabled = !enabled || mapBusy;
  }
  syncStaticImageButton();
}

function syncStaticImageButton() {
  elements.staticImageButton.disabled =
    !mapController || !mapReady || mapBusy || staticImageBusy;
  elements.imageFile.disabled = staticImageBusy;
}

function resetEditorControls() {
  elements.rotation.value = '0';
  elements.rotationOutput.value = '0°';
  elements.brightness.value = '100';
  elements.brightnessOutput.value = '100%';
  elements.contrast.value = '100';
  elements.contrastOutput.value = '100%';
  elements.drawToggle.checked = false;
}

function syncEditorUi(state = {}) {
  const enabled = Boolean(state.width > 0 && state.height > 0);

  for (const control of editorControlElements) {
    control.disabled = !enabled;
  }
  elements.undoButton.disabled = !enabled || !editor?.canUndo;
  elements.canvasEmpty.hidden = enabled;
  elements.attributionNote.hidden = !(state.protectedHeight > 0);

  if (enabled) {
    const label = state.label ? `${state.label} · ` : '';
    elements.imageSummary.textContent =
      `${label}${state.width} × ${state.height}px · 편집 ${state.actionCount ?? 0}개`;
  } else {
    elements.imageSummary.textContent = '이미지를 불러오지 않았습니다.';
  }
  syncCollaborationState();
}

function getSharedState() {
  const latitude = Number(elements.latitude.value);
  const longitude = Number(elements.longitude.value);
  const editorState = editor?.state ?? { hasSource: false, width: 0, height: 0 };

  return {
    location: {
      latitude: Number.isFinite(latitude) ? latitude : null,
      longitude: Number.isFinite(longitude) ? longitude : null,
      label: elements.locationSummary.textContent.trim(),
    },
    map: {
      ready: mapReady,
      busy: mapBusy,
      type: elements.mapType.value,
    },
    workspace: {
      ...editorState,
      sourceKind: currentImageKind,
    },
    boundaries: {
      browserScreenAccess: false,
      gpsPermission: 'human-only',
      fileSelection: 'human-only',
      download: 'human-only',
      trustModel: 'cooperative-api-contract',
    },
  };
}

function syncCollaborationState() {
  const state = editor?.state;
  if (!state?.hasSource) {
    elements.collaborationState.textContent =
      '공유할 항공뷰를 기다리고 있습니다. 브라우저 화면은 읽지 않습니다.';
    return;
  }

  const source =
    currentImageKind === 'kakao-static'
      ? 'Kakao 정적 항공뷰'
      : '사람이 선택한 로컬 이미지';
  elements.collaborationState.textContent =
    `${source} ${state.width} × ${state.height}px을(를) 사람과 AI가 함께 사용 중입니다.`;
}

function appendCollaborationActivity(activity) {
  elements.collaborationLog.querySelector('[data-empty="true"]')?.remove();
  const item = document.createElement('li');
  const actor = activity.actor === 'ai' ? 'AI' : '사람';
  item.dataset.status = activity.status ?? 'success';
  const time = new Date(activity.timestamp).toLocaleTimeString('ko-KR', {
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
  });
  item.textContent = `${time} · ${actor} · ${activity.summary}`;
  elements.collaborationLog.prepend(item);
  while (elements.collaborationLog.children.length > 12) {
    elements.collaborationLog.lastElementChild?.remove();
  }
}

function recordActivity(actor, command, summary, status = 'success') {
  const activity = Object.freeze({
    actor,
    command,
    status,
    summary,
    timestamp: new Date().toISOString(),
  });
  appendCollaborationActivity(activity);
  window.dispatchEvent(new CustomEvent('collaboration-activity', { detail: activity }));
}

function blobToDataUrl(blob) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.addEventListener('load', () => resolve(String(reader.result)), { once: true });
    reader.addEventListener('error', () => reject(new Error('이미지 데이터를 읽지 못했습니다.')), {
      once: true,
    });
    reader.readAsDataURL(blob);
  });
}

editor = new CanvasEditor(elements.canvas, {
  maxDimension: 4096,
  onChange: syncEditorUi,
});
syncEditorUi();

function setEditorTransform() {
  return editor.setTransform({
    rotation: Number(elements.rotation.value),
    brightness: Number(elements.brightness.value),
    contrast: Number(elements.contrast.value),
  });
}

function applyEditorTransform(transform = {}) {
  if (!editor.hasSource) throw new Error('먼저 함께 볼 항공사진을 불러와 주세요.');
  const state = editor.setTransform(transform);
  elements.rotation.value = String(state.rotation);
  elements.rotationOutput.value = `${state.rotation}°`;
  elements.brightness.value = String(state.brightness);
  elements.brightnessOutput.value = `${state.brightness}%`;
  elements.contrast.value = String(state.contrast);
  elements.contrastOutput.value = `${state.contrast}%`;
  return state;
}

function formatCoordinate(value) {
  return Number(value).toFixed(6);
}

function updateLocation(latitude, longitude, label) {
  elements.latitude.value = formatCoordinate(latitude);
  elements.longitude.value = formatCoordinate(longitude);
  elements.locationSummary.textContent =
    `${label} · 위도 ${formatCoordinate(latitude)}, 경도 ${formatCoordinate(longitude)}`;
}

async function settleMap(successMessage, updateMap) {
  mapReady = false;
  syncStaticImageButton();
  const controller = new AbortController();
  const tilesReady = waitForTiles(mapController.map, {
    timeout: 12_000,
    container: elements.map,
    signal: controller.signal,
  });
  try {
    await updateMap();
    await tilesReady;
    mapReady = true;
    setStatus(successMessage, 'success');
  } catch (error) {
    controller.abort();
    await tilesReady.catch(() => undefined);
    throw error;
  } finally {
    syncStaticImageButton();
  }
}

async function runMapOperation(operation, { rethrow = false } = {}) {
  if (!mapController) {
    const error = new Error('지도가 아직 준비되지 않았습니다.');
    if (rethrow) throw error;
    setStatus(error.message, 'error');
    return false;
  }
  if (mapBusy) {
    const error = new Error('다른 지도 작업이 끝난 뒤 다시 시도해 주세요.');
    if (rethrow) throw error;
    return false;
  }

  mapBusy = true;
  setMapControlsEnabled(true);

  try {
    await operation();
    return true;
  } catch (error) {
    setStatus(error instanceof Error ? error.message : String(error), 'error');
    if (rethrow) throw error;
    return false;
  } finally {
    mapBusy = false;
    setMapControlsEnabled(true);
  }
}

async function moveToLocation(latitude, longitude, label) {
  await settleMap(`${label}의 지도를 불러왔습니다.`, () => {
    setMapPosition(
      mapController.map,
      mapController.marker,
      latitude,
      longitude,
      { level: 4 },
    );
    updateLocation(latitude, longitude, label);
  });
}

async function findAddress(addressValue = elements.address.value) {
  const address = String(addressValue ?? '').trim();
  if (!address) throw new Error('찾을 주소를 입력해 주세요.');
  if (address.length > 200) throw new RangeError('주소는 200자 이내로 입력해 주세요.');
  elements.address.value = address;

  setStatus(`“${address}” 주소를 찾고 있습니다.`);
  const result = await addressToCoordinates(mapController.geocoder, address);
  await moveToLocation(
    result.latitude,
    result.longitude,
    result.address || address,
  );
}

async function loadStaticAerialView() {
  if (!mapReady) throw new Error('항공뷰 지도가 준비된 뒤 다시 시도해 주세요.');
  if (staticImageBusy) throw new Error('정적 항공뷰를 이미 준비하고 있습니다.');

  const coordinates = parseCoordinates(
    elements.latitude.value,
    elements.longitude.value,
  );
  const previousImageKind = currentImageKind;
  staticImageBusy = true;
  setMapControlsEnabled(false);
  setStatus('사람과 AI가 함께 볼 정적 항공뷰 한 장을 준비하고 있습니다.');

  try {
    const loaded = await createKakaoStaticImage({
      ...coordinates,
      width: Math.round(elements.map.clientWidth),
      height: Math.round(elements.map.clientHeight),
      level: Number(mapController.map.getLevel?.() ?? 4),
    });
    await editor.setSource(loaded.image, {
      attributionWidth: loaded.attributionWidth,
      attributionHeight: loaded.attributionHeight,
      label:
        `${loaded.label} · ${formatCoordinate(coordinates.latitude)}, ` +
        formatCoordinate(coordinates.longitude),
      close: true,
    });
    currentImageKind = 'kakao-static';
    resetEditorControls();
    syncCollaborationState();
    setStatus(
      '정적 항공뷰를 Canvas에 전달했습니다. 사람과 AI가 같은 이미지를 사용합니다.',
      'success',
    );
    return {
      summary: `정적 항공뷰 ${loaded.width} × ${loaded.height}px 공유`,
    };
  } catch (error) {
    currentImageKind = previousImageKind;
    syncCollaborationState();
    throw error;
  } finally {
    staticImageBusy = false;
    setMapControlsEnabled(Boolean(mapController));
  }
}

async function executeShared(command, payload, options) {
  try {
    return await collaborationBridge.execute(command, payload, options);
  } catch (error) {
    setStatus(error instanceof Error ? error.message : String(error), 'error');
    return null;
  }
}

async function getSharedImageBlob(format = 'png', { actor = 'ai' } = {}) {
  if (actor !== 'ai' && actor !== 'human') {
    throw new TypeError('이미지를 읽는 주체는 사람 또는 AI여야 합니다.');
  }
  try {
    const blob = await editor.toBlob(format);
    recordActivity(
      actor,
      'readAerialImage',
      `공동 작업 이미지 ${editor.state.width} × ${editor.state.height}px 열람`,
    );
    return blob;
  } catch (error) {
    recordActivity(
      actor,
      'readAerialImage',
      `공동 작업 이미지 열람 실패: ${error instanceof Error ? error.message : String(error)}`,
      'failure',
    );
    throw error;
  }
}

collaborationBridge = createCollaborationBridge({
  getState: getSharedState,
  eventTarget: window,
  onActivity: appendCollaborationActivity,
  commands: {
    findAddress: {
      reversible: true,
      handler: async ({ address } = {}) => {
        await runMapOperation(() => findAddress(address), { rethrow: true });
        return { summary: `주소 “${elements.address.value}”로 지도 이동` };
      },
    },
    setLocation: {
      reversible: true,
      handler: async ({ latitude, longitude, label = '공동 작업 좌표' } = {}) => {
        const coordinates = parseCoordinates(latitude, longitude);
        const normalizedLabel = String(label ?? '').trim().slice(0, 120) || '공동 작업 좌표';
        await runMapOperation(async () => {
          setStatus('공동 작업 좌표로 이동하고 있습니다.');
          await moveToLocation(
            coordinates.latitude,
            coordinates.longitude,
            normalizedLabel,
          );
        }, { rethrow: true });
        return {
          summary:
            `위도 ${formatCoordinate(coordinates.latitude)}, ` +
            `경도 ${formatCoordinate(coordinates.longitude)}로 이동`,
        };
      },
    },
    setMapType: {
      reversible: true,
      handler: async ({ type } = {}) => {
        const normalized = String(type ?? '').trim().toUpperCase();
        if (!['ROADMAP', 'SKYVIEW', 'HYBRID'].includes(normalized)) {
          throw new RangeError('지도 종류는 ROADMAP, SKYVIEW, HYBRID 중 하나여야 합니다.');
        }
        elements.mapType.value = normalized;
        await runMapOperation(async () => {
          setStatus('지도 종류를 바꾸고 있습니다.');
          await settleMap(
            `${elements.mapType.selectedOptions[0].textContent} 지도를 불러왔습니다.`,
            () => setMapType(mapController.map, normalized),
          );
        }, { rethrow: true });
        return { summary: `지도 종류를 ${normalized}(으)로 변경` };
      },
    },
    loadAerialView: {
      reversible: false,
      handler: loadStaticAerialView,
    },
    setTransform: {
      reversible: true,
      handler: (transform) => {
        const state = applyEditorTransform(transform);
        return {
          summary:
            `회전 ${state.rotation}°, 밝기 ${state.brightness}%, ` +
            `대비 ${state.contrast}% 적용`,
        };
      },
    },
    addText: {
      reversible: true,
      handler: ({ text, color } = {}) => {
        if (color) {
          const brush = editor.setBrush({ color });
          elements.brushColor.value = brush.color;
        }
        if (!editor.addText(text)) throw new Error('추가할 문구를 입력해 주세요.');
        return { summary: `문구 “${String(text).trim().slice(0, 40)}” 추가` };
      },
    },
    undo: {
      reversible: false,
      handler: () => {
        if (!editor.undo()) throw new Error('취소할 편집이 없습니다.');
        return { summary: '마지막 편집 취소' };
      },
    },
  },
});

const publicCapabilities = Object.freeze({
  ...collaborationBridge.capabilities,
  interfaceActor: 'ai',
  trustBoundary: 'cooperative-page-interface',
  imageResource: Object.freeze({
    id: 'current-canvas-image',
    access: 'human-ai',
    methods: Object.freeze(['getImageBlob', 'getImageDataUrl']),
    browserScreenAccess: false,
  }),
});

const collaborationApi = Object.freeze({
  version: collaborationBridge.version,
  capabilities: publicCapabilities,
  getState: collaborationBridge.getState,
  execute(command, payload) {
    return collaborationBridge.execute(command, payload, { actor: 'ai' });
  },
  getImageBlob(format = 'png') {
    return getSharedImageBlob(format, { actor: 'ai' });
  },
  async getImageDataUrl(format = 'png') {
    return blobToDataUrl(await getSharedImageBlob(format, { actor: 'ai' }));
  },
});

Object.defineProperty(window, 'aerialCanvasLab', {
  value: collaborationApi,
  enumerable: true,
});
document.documentElement.dataset.aiCollaboration = 'ready';

elements.addressForm.addEventListener('submit', (event) => {
  event.preventDefault();
  if (!allowHumanUiAction(event, '주소 찾기')) return;
  void executeShared(
    'findAddress',
    { address: elements.address.value },
    { actor: 'human' },
  );
});

elements.coordinateForm.addEventListener('submit', (event) => {
  event.preventDefault();
  if (!allowHumanUiAction(event, '좌표 이동')) return;
  void executeShared(
    'setLocation',
    {
      latitude: elements.latitude.value,
      longitude: elements.longitude.value,
      label: '입력 좌표',
    },
    { actor: 'human' },
  );
});

function getCurrentPosition() {
  if (!navigator.geolocation) {
    return Promise.reject(new Error('이 브라우저는 위치 정보 API를 지원하지 않습니다.'));
  }

  return new Promise((resolve, reject) => {
    navigator.geolocation.getCurrentPosition(resolve, reject, {
      enableHighAccuracy: true,
      timeout: 10_000,
      maximumAge: 30_000,
    });
  });
}

function geolocationMessage(error) {
  const messages = new Map([
    [1, 'GPS 권한이 거부되었습니다. 브라우저 권한을 확인해 주세요.'],
    [2, '현재 위치를 확인할 수 없습니다. 잠시 후 다시 시도해 주세요.'],
    [3, 'GPS 위치 확인 시간이 초과되었습니다.'],
  ]);
  return messages.get(error?.code) ?? 'GPS 위치를 가져오지 못했습니다.';
}

function allowHumanUiAction(event, label) {
  if (event.isTrusted) return true;
  setStatus(`${label}은(는) 사람이 페이지에서 직접 선택해야 합니다.`, 'error');
  return false;
}

elements.gpsButton.addEventListener('click', (event) => {
  if (!allowHumanUiAction(event, 'GPS 위치 사용')) return;
  void runMapOperation(async () => {
    setStatus('GPS 위치를 확인하고 있습니다.');
    let position;
    try {
      position = await getCurrentPosition();
    } catch (error) {
      throw new Error(geolocationMessage(error));
    }
    const coordinates = parseCoordinates(
      position.coords.latitude,
      position.coords.longitude,
    );
    await moveToLocation(
      coordinates.latitude,
      coordinates.longitude,
      `현재 GPS 위치 (정확도 약 ${Math.round(position.coords.accuracy)}m)`,
    );
  }).then((completed) => {
    if (completed) {
      recordActivity('human', 'gps-permission', '사람이 GPS 위치 사용을 승인하고 지도 이동');
    }
  });
});

elements.mapType.addEventListener('change', (event) => {
  if (!allowHumanUiAction(event, '지도 종류 변경')) return;
  void executeShared(
    'setMapType',
    { type: elements.mapType.value },
    { actor: 'human' },
  );
});

elements.staticImageButton.addEventListener('click', (event) => {
  if (!allowHumanUiAction(event, '정적 항공뷰 전달')) return;
  void executeShared('loadAerialView', {}, { actor: 'human' });
});

elements.imageFile.addEventListener('change', (event) => {
  if (!allowHumanUiAction(event, '로컬 파일 선택')) {
    elements.imageFile.value = '';
    return;
  }
  const [file] = elements.imageFile.files ?? [];
  if (!file) return;
  if (staticImageBusy) {
    elements.imageFile.value = '';
    setStatus('다른 이미지를 준비하고 있습니다. 완료된 뒤 다시 선택해 주세요.', 'error');
    return;
  }

  void (async () => {
    const previousImageKind = currentImageKind;
    staticImageBusy = true;
    syncStaticImageButton();
    try {
      setStatus('로컬 이미지를 여는 중입니다.');
      const loaded = await loadImageFile(file);
      await editor.setSource(loaded.image, {
        attributionWidth: 0,
        attributionHeight: 0,
        label: loaded.label,
        close: true,
      });
      currentImageKind = 'local-file';
      resetEditorControls();
      syncCollaborationState();
      setStatus('로컬 이미지를 열었습니다. 파일은 서버로 전송되지 않습니다.', 'success');
      recordActivity('human', 'file-selection', `로컬 이미지 “${loaded.label}” 선택`);
    } catch (error) {
      currentImageKind = previousImageKind;
      syncCollaborationState();
      setStatus(error instanceof Error ? error.message : String(error), 'error');
    } finally {
      staticImageBusy = false;
      syncStaticImageButton();
      elements.imageFile.value = '';
    }
  })();
});

elements.rotation.addEventListener('input', (event) => {
  if (!allowHumanUiAction(event, '회전 편집')) return;
  elements.rotationOutput.value = `${elements.rotation.value}°`;
  setEditorTransform();
});

elements.brightness.addEventListener('input', (event) => {
  if (!allowHumanUiAction(event, '밝기 편집')) return;
  elements.brightnessOutput.value = `${elements.brightness.value}%`;
  setEditorTransform();
});

elements.contrast.addEventListener('input', (event) => {
  if (!allowHumanUiAction(event, '대비 편집')) return;
  elements.contrastOutput.value = `${elements.contrast.value}%`;
  setEditorTransform();
});

function recordEditorTransform(event) {
  if (!allowHumanUiAction(event, '변환 기록')) return;
  const state = editor.state;
  recordActivity(
    'human',
    'setTransform',
    `회전 ${state.rotation}°, 밝기 ${state.brightness}%, 대비 ${state.contrast}% 적용`,
  );
}

elements.rotation.addEventListener('change', recordEditorTransform);
elements.brightness.addEventListener('change', recordEditorTransform);
elements.contrast.addEventListener('change', recordEditorTransform);

elements.drawToggle.addEventListener('change', (event) => {
  if (!allowHumanUiAction(event, '자유 그리기 변경')) return;
  editor.setDrawing(elements.drawToggle.checked);
  recordActivity(
    'human',
    'setDrawing',
    `자유 그리기 ${elements.drawToggle.checked ? '켜기' : '끄기'}`,
  );
});

function updateBrush(event) {
  if (!allowHumanUiAction(event, '그리기 도구 변경')) return;
  editor.setBrush({
    color: elements.brushColor.value,
    size: Number(elements.brushSize.value),
  });
}

elements.brushColor.addEventListener('input', updateBrush);
elements.brushSize.addEventListener('input', updateBrush);

elements.addText.addEventListener('click', (event) => {
  if (!allowHumanUiAction(event, '문구 추가')) return;
  const text = elements.annotationText.value.trim();
  if (!text) {
    setStatus('추가할 문구를 입력해 주세요.', 'error');
    elements.annotationText.focus();
    return;
  }
  void executeShared(
    'addText',
    { text, color: elements.brushColor.value },
    { actor: 'human' },
  ).then((state) => {
    if (!state) return;
    elements.annotationText.value = '';
    setStatus('가운데 문구를 추가했습니다.', 'success');
  });
});

elements.undoButton.addEventListener('click', (event) => {
  if (!allowHumanUiAction(event, '실행 취소')) return;
  void executeShared('undo', undefined, { actor: 'human' }).then((state) => {
    if (state) setStatus('마지막 편집을 취소했습니다.');
  });
});

elements.resetButton.addEventListener('click', (event) => {
  if (!allowHumanUiAction(event, '전체 초기화')) return;
  resetEditorControls();
  editor.reset();
  setStatus('편집 내용을 모두 초기화했습니다.');
  recordActivity('human', 'reset', '편집 내용을 모두 초기화');
});

async function download(format) {
  try {
    await editor.download(format);
    setStatus(`${format.toUpperCase()} 파일을 내려받았습니다.`, 'success');
    recordActivity('human', 'download', `${format.toUpperCase()} 파일 저장`);
  } catch (error) {
    setStatus(error instanceof Error ? error.message : String(error), 'error');
  }
}

elements.downloadPng.addEventListener('click', (event) => {
  if (allowHumanUiAction(event, 'PNG 저장')) void download('png');
});
elements.downloadJpeg.addEventListener('click', (event) => {
  if (allowHumanUiAction(event, 'JPEG 저장')) void download('jpeg');
});

document.addEventListener('keydown', (event) => {
  if (!event.isTrusted) return;
  const target = event.target;
  const isEditing =
    target instanceof HTMLInputElement ||
    target instanceof HTMLTextAreaElement ||
    target instanceof HTMLSelectElement ||
    target?.isContentEditable;

  if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === 'z' && !isEditing) {
    event.preventDefault();
    if (editor.canUndo) {
      void executeShared('undo', undefined, { actor: 'human' });
    }
  }
});

async function readRuntimeConfig() {
  const response = await fetch('/runtime-config.json', {
    cache: 'no-store',
    headers: { accept: 'application/json' },
  });
  const config = await response.json();
  if (!response.ok) throw new Error(config.error || '설정을 읽지 못했습니다.');
  return config;
}

async function initializeMap() {
  try {
    const config = await readRuntimeConfig();
    if (config.setupRequired || !config.kakaoJavaScriptKey) {
      throw new Error(
        '저장소 최상위 config.json에 kakaoMaps.javascriptKey를 설정해 주세요. 로컬 이미지는 지금도 편집할 수 있습니다.',
      );
    }

    setStatus('Kakao Maps SDK를 불러오고 있습니다.');
    await loadKakaoMaps(config.kakaoJavaScriptKey);

    const initial = parseCoordinates(
      elements.latitude.value,
      elements.longitude.value,
    );
    mapController = createMap(elements.map, {
      ...initial,
      level: 4,
      mapType: elements.mapType.value,
    });
    observeMapResize(mapController.map, elements.map);
    elements.mapSetup.hidden = true;
    setMapControlsEnabled(true);

    await runMapOperation(findAddress);
  } catch (error) {
    elements.mapSetup.hidden = false;
    elements.mapSetup.textContent =
      '지도를 시작하지 못했습니다. config.json의 JavaScript 키와 해당 키의 JS SDK 도메인에 http://localhost:3000이 등록됐는지 확인해 주세요.';
    setStatus(error instanceof Error ? error.message : String(error), 'error');
    setMapControlsEnabled(false);
  }
}

void initializeMap();
