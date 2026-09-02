# 특강 실습 — 사람·AI 공동 Kakao 항공 지도 Canvas

70분 동안 위치·권한, StaticMap 단일 이미지 relay, 공동 작업 API, Canvas 이미지 공유와 사람 전용 저장을 검증한다. 각 활동은 **문제 → 예상 → 구현 → 관찰 → 오류 설명 → 확장** 순서를 지킨다.

## 준비 5분

~~~powershell
cd <저장소 루트>\web_programming\specials\kakao_aerial_map\examples\app
npm start
~~~

[http://localhost:3000](http://localhost:3000)을 열고 Console과 Network를 함께 둔다.

확인:

- 실제 키: Git 최상위 <code>config.json</code>
- SDK domain: <code>http://localhost:3000</code>
- server: <code>127.0.0.1:3000</code>
- 실제 키·개인 GPS·개인 파일 내용은 제출하지 않음

역할:

- 사람 역할: GPS·파일 선택·최종 다운로드
- AI 역할: <code>window.aerialCanvasLab</code>의 공개 capability만 사용

## 실습 1 — 위치 상태와 사람 전용 권한 15분

### 1. 문제

사람 UI와 AI 명령이 같은 위치·지도 상태를 공유해야 한다. GPS 권한은 사람 UI에서만 시작하고, 공동 작업 <code>execute()</code>에서는 호출할 수 없어야 한다.

### 2. 예상

| 행동 | 예상 state | 예상 activity |
|---|---|---|
| 사람 주소 제출 | location 변경 | actor human |
| AI setLocation | location 변경 | actor ai |
| AI setMapType | map.type 변경 | actor ai |
| AI gps-permission | 변경 없음 | PROTECTED_COMMAND |
| 사람 GPS 거부 | 기존 상태 유지 | 주소·좌표 대안 |

### 3. 구현

1. <code>window.aerialCanvasLab.getState()</code>를 호출한다.
2. <code>capabilities.commands</code>와 <code>capabilities.protected</code>를 각각 기록한다.
3. 사람 UI에서 공개 주소를 제출한다.
4. AI 역할에서 다음 명령을 실행한다.

~~~js
const lab = window.aerialCanvasLab;

await lab.execute(
  "setLocation",
  {
    latitude: 37.566826,
    longitude: 126.978656,
    label: "공동 작업 좌표"
  }
);

await lab.execute(
  "setMapType",
  { type: "HYBRID" }
);
~~~

5. <code>lab.execute("gps-permission")</code>을 호출해 보호 오류를 확인한다.
6. GPS 실제 권한은 사람 역할이 버튼으로 승인하거나 거부한다.

### 4. 관찰

- [ ] state에 location, map, workspace, boundaries가 있다.
- [ ] 사람 UI와 AI 명령이 같은 latitude·longitude·type을 갱신한다.
- [ ] actor가 human과 ai로 구분된다.
- [ ] GPS는 protected, callable false다.
- [ ] AI의 GPS 명령은 handler에 도달하지 않는다.
- [ ] GPS 거부 뒤 주소·좌표 대안이 남는다.

### 5. 오류 설명

다음을 완성한다.

~~~text
GPS는 ________ 정보이므로 ________ 전용 capability다.
execute()는 command 이름을 확인한 뒤 ________ code로 거부한다.
따라서 AI는 위치 후보를 제안할 수 있지만 ________ 요청은 시작할 수 없다.
~~~

### 6. 확장

1. 현재 state와 명령 전 state를 비교하는 diff UI를 설계한다.
2. 위치 label에 actor와 적용 시각을 추가한다.
3. GPS 거부를 error가 아니라 <code>declined</code> 결정 상태로 표현한다.

## 실습 2 — StaticMap 단일 이미지 relay 15분

### 1. 문제

공식 JavaScript SDK가 만든 SKYVIEW StaticMap의 동일한 단일 image resource만 검증해 same-origin Blob으로 전달한다. 직접 확인 GET 1회와 relay 재요청 GET 1회, 총 2회의 네트워크 GET이 발생한다. 동적 tile을 열거·조합하거나 임의 URL을 relay하지 않는다.

### 2. 예상

| 입력 | 예상 |
|---|---|
| SDK가 만든 exact SKYVIEW URL | 허용 |
| 다른 origin | 400 거부 |
| 다른 path | 400 거부 |
| source 두 개 | 400 거부 |
| 너무 빠른 연속 요청 | 429 |
| HTML 응답 | 502 또는 검증 실패 |
| 8MB 초과 | 검증 실패 |

### 3. 구현

1. 현재 위치·지도 level을 정한다.
2. 사람 UI의 **정적 항공뷰를 사람·AI 작업공간에 전달**을 누르거나 AI에서 다음을 실행한다.

~~~js
await window.aerialCanvasLab.execute("loadAerialView");
~~~

3. Network에서 cross-origin 직접 확인 GET 1회와 <code>/api/kakao-static-image</code> relay GET 1회를 찾는다. 둘은 같은 SDK 생성 image resource를 가리킨다.
4. status, content type, cache control만 기록한다. source query 전체를 제출물에 복사하지 않는다.
5. <code>getState().workspace.sourceKind</code>가 <code>kakao-static</code>인지 확인한다.
6. source image 크기와 Canvas 크기를 비교한다.
7. 원본 전체가 고정 크기 Canvas에서 배율 1로 중심 회전되고 화면 밖만 clip되는지 확인한다. 회전 전후 Canvas 크기를 비교하고, 좌하단 80×32px 출처 표지가 필터·주석·회전 뒤 같은 좌하단에 마지막 합성되는지 관찰한다.

### 4. 관찰

- [ ] SDK StaticMap 컨테이너에서 image가 정확히 하나다.
- [ ] relay route로 source 하나만 전달된다.
- [ ] relay route가 Host와 same-origin Sec-Fetch-Site·Referer(및 전달된 Origin)를 검증한다.
- [ ] 응답 MIME은 JPEG 또는 PNG다.
- [ ] 응답은 no-store다.
- [ ] 동적 tile을 열거하거나 조합하는 앱 코드가 없다.
- [ ] redirect·cache·대량 저장 경로가 없다.
- [ ] 좌하단 80×32px 출처 표지가 별도 보관되고 마지막에 같은 좌하단으로 합성된다.
- [ ] 회전 전후 Canvas 크기가 같고 화면 밖 픽셀만 clip된다.

### 5. 오류 설명

다음 두 흐름의 차이를 설명한다.

~~~text
A: cross-origin image를 localhost Canvas에 직접 drawImage
B: exact StaticMap image URL 검증 → local relay → same-origin Blob
~~~

A가 tainted Canvas가 되고 B가 origin-clean Canvas가 되는 시점을 한 문장씩 쓴다.

### 6. 확장

1. client 검증과 server 검증을 비교하는 표를 만든다.
2. request limit 500ms가 없을 때 생길 수 있는 중복 요청을 설명한다.
3. allowlist에 새 origin을 추가하지 않고 실패 메시지만 개선한다.

## 실습 3 — 공동 작업 명령·로그·가역성 20분

### 1. 문제

사람 UI와 공개 AI API가 공유 상태를 갱신하되 공개 <code>execute()</code>의 actor는 항상 AI로 고정된다. 호출자는 human으로 위장하거나 summary를 덮어쓸 수 없다. 모든 성공·거부·실패는 actor·command·status·summary·timestamp를 남기며 command는 직렬 실행된다. capability의 reversible metadata를 실행 전에 확인한다.

### 2. 예상

| command | actor | reversible | 예상 |
|---|---|---:|---|
| setMapType | ai | true | 지도 유형 변경 |
| setTransform | ai | true | Canvas 편집 |
| addText | human | true | 문구 추가 |
| undo | ai | false | 마지막 편집 취소 |
| loadAerialView | ai | false | source 교체 |
| download | ai | 해당 없음 | PROTECTED_COMMAND |
| missing | ai | 해당 없음 | UNKNOWN_COMMAND |

### 3. 구현

1. <code>lab.capabilities.commands</code>를 읽는다.
2. state를 저장한 뒤 <code>setTransform</code>을 실행한다.

~~~js
const lab = window.aerialCanvasLab;
const before = lab.getState();

const after = await lab.execute(
  "setTransform",
  { rotation: 0, brightness: 105, contrast: 115 }
);
~~~

3. <code>addText</code>와 <code>undo</code>를 차례로 실행한다.
4. UI activity 목록을 확인한다.
5. <code>collaboration-activity</code> event detail을 한 번 관찰한다.
6. <code>download</code>, <code>file-selection</code>, 존재하지 않는 명령을 실행해 오류 code를 구분한다.

### 4. 관찰

- [ ] 전역 API와 capabilities가 frozen이다.
- [ ] 공개 API actor는 항상 ai이며 actor·summary 입력을 받지 않는다.
- [ ] 실행 결과는 최신 getState 형식이다.
- [ ] activity가 정확히 한 건 추가된다.
- [ ] summary는 간결하고 실제 결과를 설명한다.
- [ ] timestamp는 ISO-8601이다.
- [ ] protected·unknown·실행 실패가 status와 code를 남긴다.
- [ ] 연속 명령은 호출 순서대로 직렬 실행된다.
- [ ] loadAerialView는 별도 좌표 payload 없이 현재 공유 위치를 사용한다.
- [ ] reversible metadata가 명령 목록에 보인다.

### 5. 오류 설명

<code>loadAerialView</code>와 <code>setTransform</code>의 reversible 차이를 설명한다. source 교체가 왜 단순 transform보다 되돌리기 어려운지, 사용자에게 어떤 사전 안내가 필요한지 쓴다.

### 6. 확장

1. 실행 전 reversible false 명령에 확인 상태를 추가한다.
2. activity를 actor별 색으로 구분한다.
3. 이전 state를 메모리에 보관하는 command history를 설계한다.
4. summary 최대 길이와 민감 정보 제거 규칙을 제안한다.

## 실습 4 — 이미지 공유·편집·사람 저장 15분

### 1. 문제

현재 Canvas 이미지는 사람과 AI가 Blob 또는 Data URL로 읽을 수 있지만, 파일 다운로드는 사람만 시작해야 한다. StaticMap source와 로컬 파일 source의 출처 metadata도 구분한다.

### 2. 예상

| 행동 | AI 가능 | activity | 외부 효과 |
|---|---:|---|---|
| getImageBlob | O | readAerialImage | 없음 |
| getImageDataUrl | O | readAerialImage | 없음 |
| setTransform | O | setTransform | Canvas 변경 |
| file picker | X | 사람 기록 | 파일 선택 |
| download | X | 사람 기록 | 파일 저장 |

### 3. 구현

1. AI 역할이 현재 Canvas를 읽는다.

~~~js
const lab = window.aerialCanvasLab;

const blob = await lab.getImageBlob("png");
const dataUrl = await lab.getImageDataUrl("jpeg");

console.log(blob.type, blob.size, dataUrl.startsWith("data:image/jpeg"));
~~~

2. UI activity에서 <code>readAerialImage</code> 두 건을 확인한다.
3. 사람이 PNG·JPEG·WebP 로컬 파일을 직접 선택한다.
4. source kind가 <code>local-file</code>, <code>attributionWidth</code>와 <code>attributionHeight</code>가 모두 0인지 확인한다.
5. AI가 밝기·대비를 적용하고 사람이 undo 또는 초기화를 수행한다.
6. 사람이 PNG 또는 JPEG 버튼으로 최종 저장한다.

### 4. 관찰

- [ ] Blob과 Data URL은 현재 Canvas만 표현한다.
- [ ] 브라우저 다른 영역은 읽지 않는다.
- [ ] 이미지 읽기는 다운로드를 시작하지 않는다.
- [ ] AI 이미지 열람의 성공·실패가 actor ai와 status로 기록된다.
- [ ] 이미지 읽기는 진행 중인 사람 stroke를 종료·commit하지 않는 read-only snapshot이다.
- [ ] 로컬 파일 선택은 사람 UI에서만 가능하다.
- [ ] 저장은 사람 버튼에서만 시작한다.
- [ ] PNG는 무손실, JPEG는 손실 압축이다.

### 5. 오류 설명

다음 문장을 완성한다.

~~~text
getImageBlob()은 ________ 를 반환하지만 ________ 를 시작하지 않는다.
다운로드는 외부 효과이므로 ________ 전용 capability다.
따라서 AI는 공유된 이미지를 분석할 수 있지만 파일 저장은 ________ 이 결정한다.
~~~

### 6. 확장

1. image read activity에 format과 byte size를 추가한다.
2. Data URL 최대 길이 정책을 설계한다.
3. 사람 저장 전에 format·크기·source kind를 확인하는 dialog를 설계한다.
4. human-only는 협업 API 계약이며 전체 브라우저 제어를 위임받은 자동화 도구를 격리하는 보안 sandbox가 아님을 설명한다.

## 제출 증거

- <code>getState()</code>의 네 최상위 영역
- 공용 command와 human-only capability 표
- StaticMap 단일 image → relay → Blob 흐름도
- relay 응답 status·MIME·no-store
- Kakao 출처 영역 보호 관찰
- AI 명령 activity 한 건
- protected command 오류 code
- <code>getImageBlob()</code> 결과 type·size
- 사람 전용 파일 선택·다운로드 설명
- 금지 경로가 없는 이유 한 문단

## 완료 점검

| 항목 | 완료 기준 |
|---|---|
| 설정 | 루트 config·Git 제외·localhost:3000 |
| 지도 | 주소·GPS·SKYVIEW/HYBRID |
| relay | exact single image·allowlist·no-store·rate |
| Canvas | same-origin Blob·출처 보존 |
| 협업 | getState·execute·activity |
| 가역성 | command metadata·undo |
| 이미지 | Blob·Data URL 명시적 공유 |
| 사람 전용 | GPS·파일·다운로드 |
| 제외 | tile 조합·화면 읽기/촬영·cache·대량 저장 없음 |

## 운영 전 확인

제한 relay 설계가 Kakao 이용 정책상 허용을 자동 보증하는 것은 아니다. 수업 밖 배포·운영 전 최신 Kakao Maps API 이용정책과 출처표시 정책을 확인하며 법적 허용을 단정하지 않는다.

## 공식 참고

- [Kakao 지도 Web API 레퍼런스](https://apis.map.kakao.com/web/documentation/)
- [Kakao StaticMap 샘플](https://apis.map.kakao.com/web/sample/staticMap/)
- [Kakao Map REST API](https://developers.kakao.com/docs/ko/kakaomap/rest-api)
- [MDN CORS enabled images](https://developer.mozilla.org/en-US/docs/Web/HTML/How_to/CORS_enabled_image)
- [MDN Canvas.toBlob](https://developer.mozilla.org/en-US/docs/Web/API/HTMLCanvasElement/toBlob)
- [MDN Geolocation](https://developer.mozilla.org/en-US/docs/Web/API/Geolocation/getCurrentPosition)
