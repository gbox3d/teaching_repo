// 세 TODO를 채운다. 반환값은 true 또는 false여야 한다.
// HTTP·시작/중지·재시도는 제공된 automatic/runner.js가 처리한다.
function decideFan(temperature, currentOn, settings) {
  if (settings.mode === 'single') {
    // TODO 1: temperature가 settings.threshold 이상이면 true, 미만이면 false.
    return null;
  }
  // TODO 2: settings.high 이상이면 켜고 settings.low 이하이면 끈다.
  // TODO 3: 두 기준 사이이면 currentOn을 그대로 반환한다.
  return null;
}
