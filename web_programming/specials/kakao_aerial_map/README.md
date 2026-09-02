# 특강 — 사람과 AI가 같이 쓰는 Kakao 항공 지도 Canvas

Kakao 지도 Web API로 주소·GPS 위치의 <code>SKYVIEW</code>·<code>HYBRID</code> 지도를 조회한다. 사용자가 **정적 항공뷰 전달**을 선택하거나 허용된 공동 작업 명령이 실행되면, 공식 JavaScript SDK가 생성한 <code>StaticMap(SKYVIEW)</code> 단일 이미지 하나만 엄격한 로컬 relay를 거쳐 same-origin Blob이 된다. 이 이미지는 로컬 파일과 같은 Canvas 편집기에서 회전·밝기·대비·텍스트·자유 그리기 후 PNG 또는 JPEG로 사용할 수 있다.

특강의 중심 주제는 **“사람과 AI가 같이 쓰는 페이지 — AI와 인간의 공감”**이다. 사람과 AI가 같은 명시적 상태·명령·이미지 리소스를 보되, GPS 권한·로컬 파일 선택·최종 다운로드는 사람에게만 남긴다. 공동 작업은 누가 무엇을 했는지 기록하고, 명령별 가역성 metadata를 공개한다.

## 학습 목표

1. JavaScript 키, 허용 도메인, 런타임 설정의 역할을 구분한다.
2. 주소 결과의 경도 <code>x</code>와 위도 <code>y</code>를 지도 좌표에 적용하고 GPS 거부 대안을 설계한다.
3. <code>ROADMAP</code>·<code>SKYVIEW</code>·<code>HYBRID</code>를 공식 SDK로 전환한다.
4. cross-origin StaticMap 이미지를 브라우저에서 직접 Canvas에 그릴 때 tainted Canvas가 되는 이유를 설명한다.
5. 공식 SDK가 생성한 단일 SKYVIEW 이미지에만 허용되는 로컬 relay의 검증 경계를 설명한다.
6. same-origin Blob을 Canvas source로 디코딩하고 Kakao 출처 영역을 보존한다.
7. <code>window.aerialCanvasLab</code>의 상태·명령·이미지 공유 계약을 사용한다.
8. 사람 전용 capability와 사람·AI 공용 capability를 구분한다.
9. AI 행동의 actor·command·summary·timestamp와 reversible metadata를 확인한다.

## 110분 운영 흐름

| 시간 | 활동 | 결과 |
|---:|---|---|
| 0–10분 | 앱 구조, 키, 공감형 capability | 공유·보호 경계 설명 |
| 10–20분 | 주소→좌표, GPS, 지도 유형 | SKYVIEW/HYBRID 조회 |
| 20–30분 | StaticMap, CORS, 제한 relay | same-origin 이미지 흐름 예상 |
| 30–35분 | 실습 준비 | 서버·Console·Network 기준점 |
| 35–50분 | 실습 1: 위치·지도·사람 전용 권한 | 상태와 동의 증거 |
| 50–65분 | 실습 2: 정적 항공뷰 단일 이미지 | 검증된 Canvas source |
| 65–85분 | 실습 3: AI 공동 작업 API | 명령·로그·가역성 |
| 85–100분 | 실습 4: 편집·이미지 공유·저장 | Blob·Data URL·다운로드 구분 |
| 100–110분 | 결과 공유·정리 | 전체 계약 설명 |

## 전체 구조

~~~text
주소 / GPS
  → Kakao 동적 지도 ROADMAP / SKYVIEW / HYBRID
  → 현재 위치와 지도 상태

현재 위치
  → 공식 Kakao JS SDK StaticMap(SKYVIEW)
  → SDK가 만든 단일 <img> URL
  → 엄격한 127.0.0.1 relay
  → same-origin image Blob
  → Canvas editor

로컬 PNG / JPEG / WebP
  → image-loader.js
  → Canvas editor

Canvas editor
  ↔ window.aerialCanvasLab
       ├─ getState()
       ├─ execute()
       ├─ getImageBlob()
       └─ getImageDataUrl()
~~~

동적 지도 타일을 열거하거나 조합하지 않는다. 브라우저 화면 전체를 읽거나 촬영하지 않는다. relay는 공식 StaticMap이 만든 단일 SKYVIEW 이미지 URL 한 개만 요청한다.

## 사람과 AI의 공감 계약

| capability | 접근 | 설명 |
|---|---|---|
| 상태 읽기 | 사람·AI | 위치, 지도, workspace, boundary |
| 허용 명령 실행 | 사람·AI | 주소, 좌표, 지도 유형, 정적 항공뷰, 편집, undo |
| 현재 Canvas 이미지 읽기 | 사람·AI | Blob 또는 Data URL |
| GPS 권한 | 사람 전용 | 직접 버튼을 눌러 브라우저 권한 결정 |
| 로컬 파일 선택 | 사람 전용 | 파일 picker를 직접 시작 |
| 최종 다운로드 | 사람 전용 | 저장 버튼을 직접 누름 |

공용 명령은 allowlist에 이름과 <code>reversible</code>을 공개한다. 명령은 앞 명령이 끝난 뒤 다음 명령을 시작하도록 직렬 실행된다. 성공과 거부·실패 모두 <code>actor</code>, <code>command</code>, <code>status</code>, 간결한 <code>summary</code>, ISO <code>timestamp</code>를 활동 기록에 남긴다.

공개 <code>window.aerialCanvasLab</code>의 actor는 항상 <code>ai</code>다. 호출자가 actor를 <code>human</code>으로 위장하거나 summary를 덮어쓸 options는 공개하지 않는다. 사람 UI만 내부 bridge를 통해 <code>human</code> 활동을 기록한다.

사람 전용 capability는 공개 <code>execute()</code>로 호출하려 해도 <code>PROTECTED_COMMAND</code>로 거부된다. 다만 이것은 협력 페이지의 API 계약이지, 브라우저 전체 제어 권한을 이미 위임받은 자동화 도구를 격리하는 보안 sandbox는 아니다.

## 실행

~~~powershell
cd <저장소 루트>\web_programming\specials\kakao_aerial_map\examples\app
npm start
~~~

[http://localhost:3000](http://localhost:3000)을 연다. 서버는 <code>127.0.0.1</code>에 bind하며 수업 포트는 3000이다. Kakao Developers의 JavaScript SDK 허용 도메인에도 <code>http://localhost:3000</code>을 등록한다.

## 설정 파일과 키

실제 설정은 Git 최상위 한 파일이다.

~~~text
<저장소 루트>\config.json
~~~

~~~json
{
  "kakaoMaps": {
    "javascriptKey": "발급받은-JavaScript-키"
  }
}
~~~

- Git 최상위 <code>.gitignore</code>의 <code>/config.json</code> 규칙으로 실제 파일을 제외한다.
- 앱의 <code>config.example.json</code>은 값이 없는 스키마 예시다.
- 앱 폴더에 실제 설정을 복사하지 않는다.
- <code>/runtime-config.json</code>은 <code>kakaoJavaScriptKey</code>와 <code>setupRequired</code>만 전달한다.
- JavaScript 키는 클라이언트 SDK 요청에서 보일 수 있으므로 허용 도메인과 사용량을 관리한다.
- 이 앱은 REST API 키와 Admin 키를 사용하지 않는다.

## 주소·GPS·지도 유형

- SDK URL에 <code>libraries=services</code>를 포함한다.
- 주소 검색 결과의 <code>x</code>는 경도, <code>y</code>는 위도다.
- <code>LatLng</code> 생성자는 위도, 경도 순서다.
- 결과 없음과 서비스 오류를 구분한다.
- GPS는 사람이 직접 버튼을 눌렀을 때만 요청한다.
- GPS 위치는 메모리의 지도 이동에만 쓰고 서버나 파일에 자동 저장하지 않는다.
- 지도 전환은 공식 <code>MapTypeId</code> 상수만 허용한다.

## 왜 relay가 필요한가

공식 JavaScript SDK의 <code>StaticMap</code>은 다음처럼 SKYVIEW 이미지 지도를 만든다.

~~~js
new kakao.maps.StaticMap(container, {
  center: new kakao.maps.LatLng(latitude, longitude),
  level,
  mapTypeId: kakao.maps.MapTypeId.SKYVIEW
});
~~~

SDK가 만든 이미지는 Kakao origin의 cross-origin 리소스다. localhost에서 해당 image element를 직접 Canvas에 그리면 Canvas가 tainted 상태가 되어 <code>getImageData()</code>, <code>toBlob()</code>, <code>toDataURL()</code>이 <code>SecurityError</code>로 차단된다.

현재 구현은 이 제한을 숨기지 않는다. 브라우저가 임의 외부 URL을 받는 대신, 공식 SDK가 방금 생성한 StaticMap 컨테이너에서 **동일한 단일 이미지 리소스**가 완전히 로드됐는지 확인한다. 네트워크 GET은 두 번이다.

1. cross-origin image를 확인하기 위해 SDK 생성 resource를 직접 읽는 GET
2. 같은 resource를 origin-clean Blob으로 받기 위한 relay의 GET

리소스를 두 종류 만들거나 여러 타일을 조합하는 것이 아니다. 동일한 SDK 생성 image resource를 client와 server에서 연속 검증한다.

## 엄격한 단일 이미지 relay

브라우저 <code>js/static-map.js</code>:

- 위도 −90~90, 경도 −180~180 검증
- 너비 160~1280, 높이 120~960, 지도 level 1~14
- 공식 SDK의 <code>StaticMap(SKYVIEW)</code> 사용
- 컨테이너의 이미지가 정확히 하나인지 확인
- HTTPS origin <code>spi.map.kakao.com</code>과 정확한 SKYVIEW image service path만 허용
- URL을 직접 만들거나 query field를 해석하지 않음
- 같은 origin의 <code>/api/kakao-static-image</code>로 검증된 source 전달
- 응답 MIME·크기·요청 크기 일치 검증

서버 <code>static-map-relay.mjs</code>와 <code>server.mjs</code>:

- <code>GET</code>과 정확히 한 개의 <code>source</code>만 허용
- 요청 <code>Host</code>가 localhost 또는 127.0.0.1의 수업 포트인지 확인
- <code>Sec-Fetch-Site: same-origin</code>, 허용 <code>Referer</code> origin, 선택적 <code>Origin</code> 검증
- exact origin·path·허용 parameter set·필수 값·<code>service=open</code> 검증
- username·password·fragment·redirect 거부
- timeout 10초, 응답 최대 8MB
- JPEG·PNG만 허용
- 동시 한 요청, 요청 간 최소 500ms
- 요청·응답 <code>cache-control: no-store</code>
- 디스크 cache, 장기 저장, 대량 요청 없음

이것은 일반 목적 proxy가 아니다. 동적 지도 타일을 열거·수집·조합하지 않고, 임의 URL도 전달하지 않는다.

## Kakao 출처 영역

원본 StaticMap 전체를 고정 크기 Canvas의 중심에서 배율 1로 회전하고, Canvas 밖으로 나간 부분만 clip한다. 회전 전후 Canvas 크기는 바뀌지 않는다.

- Kakao 좌하단 출처 표지 80×32px만 별도로 보관한다.
- 필터·주석·회전이 끝난 뒤 표지를 같은 좌하단에 마지막으로 합성한다.
- 로컬 파일은 <code>attributionWidth=0</code>, <code>attributionHeight=0</code>이다.
- 출처 영역을 제거하거나 가리는 기능은 없다.

## 공동 작업 API

브라우저 전역에는 읽기 전용 객체가 공개된다.

~~~js
const lab = window.aerialCanvasLab;

lab.getState();
await lab.execute("setMapType", { type: "HYBRID" });
await lab.execute("loadAerialView");
const blob = await lab.getImageBlob("png");
const dataUrl = await lab.getImageDataUrl("jpeg");
~~~

<code>getState()</code>는 다음 범위를 반환한다.

- <code>location</code>: latitude, longitude, label
- <code>map</code>: ready, busy, type
- <code>workspace</code>: Canvas 편집 상태와 <code>sourceKind</code>
- <code>boundaries</code>: 화면 접근 없음, GPS·파일·다운로드 human-only

공용 명령:

- <code>findAddress</code>
- <code>setLocation</code>
- <code>setMapType</code>
- <code>loadAerialView</code>
- <code>setTransform</code>
- <code>addText</code>
- <code>undo</code>

모든 명령은 직렬 실행된다. <code>loadAerialView</code>는 별도 좌표 payload를 받지 않고 <code>getState()</code>에 보이는 현재 공유 위치만 사용한다.

<code>getImageBlob()</code>과 <code>getImageDataUrl()</code>은 현재 Canvas 이미지만 명시적으로 공유하고 성공·실패 열람 활동을 <code>status</code>와 함께 기록한다. 진행 중인 사람의 자유 그리기 stroke를 종료하거나 actions에 commit하지 않는 read-only snapshot이다. 브라우저의 다른 영역, 다른 문서, 다른 앱은 읽지 않는다.

## REST 정적 지도 API와 구분

Kakao의 공식 REST <code>GET /v2/maps/staticmap</code>은 REST API 키로 PNG·JPEG 바이너리를 반환하는 별도 API다. 2026-08-26 기준 문서 파라미터에는 지도 유형 또는 SKYVIEW 선택 항목이 없다.

현재 앱은 REST 정적 지도 API를 항공 지도 경로로 사용하지 않는다. JavaScript 키로 로드한 공식 Web SDK가 생성한 <code>StaticMap(SKYVIEW)</code> 단일 이미지 URL만 제한 relay한다.

## 로컬 이미지 Canvas 편집

- 사람이 직접 고른 PNG·JPEG·WebP만 불러온다.
- 파일은 서버로 업로드하지 않는다.
- 최대 20MB, 2,400만 화소, 한 변 16,384px를 검증한다.
- 큰 이미지는 Canvas 메모리 안전을 위해 비율 축소될 수 있다.
- 원본과 편집 상태를 분리해 매번 다시 렌더링한다.
- PNG는 무손실, JPEG는 손실 압축이다.

## 사용하지 않는 경로

- 동적 지도 타일 URL 열거·수집·조합
- 화면 전체 읽기 또는 화면 촬영
- 임의 외부 URL relay
- redirect 추적
- relay 응답 cache·디스크 저장·대량 요청
- REST 정적 지도 API의 문서화되지 않은 SKYVIEW 파라미터 추측
- AI가 GPS·파일 선택·최종 다운로드 실행

## 완료 기준

- [ ] 주소·GPS로 지도와 마커를 이동한다.
- [ ] SKYVIEW와 HYBRID를 전환한다.
- [ ] 직접 cross-origin 이미지와 same-origin relay Blob의 차이를 설명한다.
- [ ] 공식 SDK가 만든 단일 SKYVIEW 이미지 URL만 허용됨을 설명한다.
- [ ] relay의 allowlist·크기·MIME·rate·no-store 경계를 말한다.
- [ ] Kakao 출처 영역을 보존한 Canvas를 만든다.
- [ ] <code>getState()</code>와 허용 <code>execute()</code> 명령을 사용한다.
- [ ] <code>getImageBlob()</code> 또는 <code>getImageDataUrl()</code>로 현재 이미지를 명시적으로 읽는다.
- [ ] 사람 전용 capability 호출이 거부됨을 확인한다.
- [ ] AI 활동 기록과 reversible metadata를 확인한다.
- [ ] PNG·JPEG 저장은 사람이 직접 수행한다.

## 자료

- [PT 원고](slides.md)
- 강의 대본: 강의자 별도 관리(비공개)
- [실습 문제](lab.md)
- [예제 실행 안내](examples/README.md)

## 운영 전 확인

이 제한 relay 설계가 Kakao 이용 정책상 허용을 자동 보증하지는 않는다. 수업 밖에서 배포·운영하기 전 최신 Kakao Maps API 이용정책과 출처표시 정책을 다시 확인한다. 이 자료는 법적 허용을 단정하지 않는다.

## 공식 참고 문서

- [Kakao 지도 Web API 가이드](https://apis.map.kakao.com/web/guide/)
- [Kakao 지도 Web API 레퍼런스](https://apis.map.kakao.com/web/documentation/)
- [Kakao StaticMap 샘플](https://apis.map.kakao.com/web/sample/staticMap/)
- [Kakao Map REST API](https://developers.kakao.com/docs/ko/kakaomap/rest-api)
- [MDN CORS enabled images와 tainted Canvas](https://developer.mozilla.org/en-US/docs/Web/HTML/How_to/CORS_enabled_image)
- [MDN Canvas.toBlob](https://developer.mozilla.org/en-US/docs/Web/API/HTMLCanvasElement/toBlob)
- [MDN Geolocation](https://developer.mozilla.org/en-US/docs/Web/API/Geolocation/getCurrentPosition)
