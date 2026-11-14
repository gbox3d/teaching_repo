function describeObservation(method, status, responseText) {
  // 연구 과제: HTTP 성공 번호와 실제 변경을 구별하는 관찰 안내를 작성한다.
  // 1. PATCH 200 []를 새 값 저장 완료로 표시하지 않는다.
  // 2. DELETE 204는 같은 ID를 GET해 빈 배열인지 확인하도록 안내한다.
  // 3. POST 201에서 새 id를 읽고 다른 브라우저의 GET 결과와 비교한다.
  // 응답 원문과 요청 키를 그대로 기록하지 말고 변경한 행의 수·ID만 활용한다.
  return '실험 과제: 같은 글을 GET으로 다시 읽고, 예상과 실제 결과를 기록하세요.';
}
