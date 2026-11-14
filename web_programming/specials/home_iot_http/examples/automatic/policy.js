// 함수의 결과만 결정한다. HTTP 요청과 반복 실행은 runner.js가 맡는다.
function decideFan(temperature, currentOn, settings) {
  if (settings.mode === 'single') {
    return temperature >= settings.threshold;
  }
  if (temperature >= settings.high) return true;
  if (temperature <= settings.low) return false;
  return currentOn; // 두 기준 사이에서는 앞 상태를 유지한다.
}
