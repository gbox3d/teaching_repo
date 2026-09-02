# 사람·AI 공동 Kakao 항공 지도 Canvas 예제

<code>app</code>은 Kakao 지도 조회, 공식 SDK StaticMap 단일 이미지 relay, 로컬 이미지 편집, 사람·AI 공동 작업 API를 연결한 실행 예제다.

## 실행

~~~powershell
cd <저장소 루트>\web_programming\specials\kakao_aerial_map\examples\app
npm start
~~~

[http://localhost:3000](http://localhost:3000)을 연다. 서버는 <code>127.0.0.1</code>에 bind하고 수업 포트는 3000이다.

## 설정

~~~text
<저장소 루트>
├─ config.json                         실제 값, Git 제외
└─ teaching_materials\web_programming\specials\kakao_aerial_map\examples\app
   └─ config.example.json              키 없는 예시
~~~

~~~json
{
  "kakaoMaps": {
    "javascriptKey": "발급받은-JavaScript-키"
  }
}
~~~

- 실제 설정은 Git 최상위 한 파일만 사용한다.
- <code>/config.json</code>은 Git에서 제외한다.
- JavaScript SDK 허용 도메인에 <code>http://localhost:3000</code>을 등록한다.
- REST API 키와 Admin 키는 사용하지 않는다.

## 파일 책임

| 파일 | 책임 |
|---|---|
| <code>index.html</code> | 지도·정적 항공뷰·편집·공동 작업 UI |
| <code>styles.css</code> | 반응형 지도·Canvas·활동 기록 |
| <code>server.mjs</code> | 로컬 정적 서버, 런타임 설정, 제한 relay route |
| <code>static-map-relay.mjs</code> | 공식 SDK SKYVIEW 단일 image URL 서버 검증·전달 |
| <code>config.example.json</code> | 루트 설정의 키 없는 스키마 |
| <code>js/main.js</code> | UI와 지도·이미지·공동 작업 흐름 |
| <code>js/map.js</code> | SDK, 주소, 지도·마커, 지도 유형 |
| <code>js/static-map.js</code> | StaticMap 생성, 한 image 확인, relay 요청, Blob decode |
| <code>js/image-loader.js</code> | PNG·JPEG·WebP 로컬 파일 검증 |
| <code>js/collaboration-bridge.js</code> | capability, 명령, actor, activity contract |
| <code>js/editor-core.js</code> | 회전·필터·좌표 순수 계산 |
| <code>js/canvas-editor.js</code> | source·편집 상태·출처 보호·Blob·다운로드 |
| <code>tests/*.test.mjs</code> | 지도·relay·편집·협업 계약 테스트 |

~~~text
main.js
 ├─ map.js
 ├─ static-map.js ── /api/kakao-static-image
 ├─ image-loader.js
 ├─ collaboration-bridge.js
 └─ canvas-editor.js
       └─ editor-core.js

server.mjs
 └─ static-map-relay.mjs
~~~

## StaticMap 단일 이미지 흐름

~~~text
현재 좌표·크기·level
  → Kakao 공식 JS SDK StaticMap(SKYVIEW)
  → 컨테이너의 동일한 단일 image resource 확인용 GET
  → exact Kakao SKYVIEW image URL 검증
  → 같은 resource를 GET /api/kakao-static-image?source=...로 재요청
  → 서버 allowlist·크기·MIME·rate 검증
  → no-store image response
  → same-origin Blob
  → createImageBitmap 또는 Image decode
  → CanvasEditor.setSource()
~~~

브라우저 module은 URL query를 만들거나 의미를 해석하지 않는다. 공식 SDK가 생성한 URL을 exact origin·path로 검사해 전달한다. 서버가 다시 parameter allowlist를 검증한다.

네트워크 GET은 동일한 SDK 생성 image resource에 대해 두 번 발생한다.

1. SDK가 만든 cross-origin image element를 완전히 로드하고 단일 resource인지 확인하는 GET
2. 검증된 같은 resource를 origin-clean Blob으로 받는 relay GET

“단일 image”는 resource 종류가 하나라는 뜻이지 network request가 한 번이라는 뜻이 아니다.

## relay 제한

| 경계 | 값 |
|---|---|
| server bind | <code>127.0.0.1</code> |
| method | GET |
| source 개수 | 정확히 1 |
| request Host | <code>localhost:3000</code> 또는 <code>127.0.0.1:3000</code> |
| Fetch Metadata | <code>Sec-Fetch-Site: same-origin</code> |
| Referer·Origin | 허용된 local origin |
| source origin | <code>https://spi.map.kakao.com</code> |
| source path | 정확한 SKYVIEW image service path |
| redirect | 거부 |
| 응답 MIME | JPEG 또는 PNG |
| timeout | 10초 |
| 최대 응답 | 8MB |
| 동시 요청 | 1 |
| 최소 요청 간격 | 500ms |
| cache | <code>no-store</code> |

추가 제한:

- StaticMap 너비 160~1280, 높이 120~960
- 지도 level 1~14
- decoded image 최대 200만 화소
- 응답 크기는 요청한 StaticMap 크기와 같아야 함
- 좌하단 80×32px Kakao 출처 표지 보호

일반 목적 proxy, 동적 타일 수집기, 이미지 cache가 아니다.

## 공동 작업 API

~~~js
const lab = window.aerialCanvasLab;
~~~

공개 항목:

| API | 역할 |
|---|---|
| <code>version</code> | 계약 version |
| <code>capabilities</code> | 공용 명령과 human-only 목록 |
| <code>getState()</code> | 현재 위치·지도·workspace·boundary |
| <code>execute(command, payload)</code> | AI actor로 allowlist 명령 실행 |
| <code>getImageBlob(format)</code> | AI actor로 현재 Canvas Blob snapshot 읽기 |
| <code>getImageDataUrl(format)</code> | AI actor로 현재 Canvas Data URL snapshot 읽기 |

공용 명령:

| command | reversible |
|---|---|
| <code>findAddress</code> | true |
| <code>setLocation</code> | true |
| <code>setMapType</code> | true |
| <code>loadAerialView</code> | false |
| <code>setTransform</code> | true |
| <code>addText</code> | true |
| <code>undo</code> | false |

사람 전용 capability:

- <code>gps-permission</code>
- <code>file-selection</code>
- <code>download</code>

이 세 이름은 명령으로 등록할 수 없고 <code>execute()</code>로 호출하면 <code>PROTECTED_COMMAND</code>가 발생한다. 이 보호는 협력 페이지 인터페이스의 계약이며, 브라우저 전체 제어를 위임받은 외부 자동화 도구를 격리하는 sandbox는 아니다.

## 사용 예

~~~js
const lab = window.aerialCanvasLab;

const before = lab.getState();

await lab.execute(
  "setMapType",
  { type: "HYBRID" }
);

await lab.execute("loadAerialView");

await lab.execute(
  "setTransform",
  { brightness: 105, contrast: 115 }
);

const imageBlob = await lab.getImageBlob("png");
~~~

공개 API의 actor는 항상 <code>ai</code>이며 호출자가 human actor나 임의 summary를 지정할 수 없다. 명령은 직렬 queue에서 하나씩 실행된다. <code>loadAerialView</code>는 좌표 payload를 받지 않고 현재 공유 위치를 사용한다.

<code>getImageBlob()</code>은 Blob을 반환할 뿐 다운로드하지 않는다. <code>getImageDataUrl()</code>도 현재 Canvas만 직렬화한다. 두 호출은 성공 또는 실패 <code>readAerialImage</code> 활동으로 기록된다. 진행 중인 사람 stroke를 끝내거나 commit하지 않는 read-only snapshot이다.

## 상태와 활동 기록

<code>getState()</code>:

~~~text
location   latitude, longitude, label
map        ready, busy, type
workspace  sourceKind, transform, 크기, 주석 상태
boundaries browserScreenAccess=false
           gpsPermission=human-only
           fileSelection=human-only
           download=human-only
~~~

activity:

~~~json
{
  "actor": "ai",
  "command": "setTransform",
  "status": "success",
  "summary": "회전 0°, 밝기 105%, 대비 115% 적용",
  "timestamp": "ISO-8601"
}
~~~

activity는 UI 목록과 <code>collaboration-activity</code> event로 공개된다. 성공은 <code>success</code>, 거부·실패는 <code>failure</code> status를 남긴다. 이미지 열람 실패도 같은 방식으로 기록한다.

## 사람 전용 흐름

- GPS: 사람이 GPS 버튼을 누르고 브라우저 권한을 결정
- 파일: 사람이 file picker를 열어 PNG·JPEG·WebP 선택
- 저장: 사람이 PNG 또는 JPEG 다운로드 버튼을 누름

AI는 위 세 행동을 대신 실행할 수 없다. 다만 사용자가 이미 공유한 현재 Canvas 이미지는 명시적 image API로 읽을 수 있다.

## Kakao 출처 보호

원본 StaticMap 전체는 고정 크기 Canvas의 중심에서 배율 1로 회전하며 Canvas 밖만 clip한다. 회전 전후 Canvas 크기는 불변이다.

- 좌하단 출처 표지 80×32px만 별도 보관
- 필터·주석·회전 뒤 같은 좌하단에 마지막 합성
- PNG 내보내기에서 무손실
- JPEG는 손실 압축 특성 존재

로컬 파일은 <code>attributionWidth=0</code>, <code>attributionHeight=0</code>이다.

## 테스트

~~~powershell
npm run check
npm test
~~~

자동 테스트는 다음을 확인한다.

- 주소 <code>x/y</code> 변환과 지도 유형 allowlist
- StaticMap option 범위
- exact SKYVIEW endpoint
- same-origin relay URL 생성
- relay parameter·MIME·size 검증
- 편집 좌표·회전·필터
- immutable capability contract
- human-only 명령 거부
- actor 검증, activity 기록, reversible metadata

## 사용하지 않는 경로

- 동적 지도 타일 열거·조합
- 화면 전체 읽기 또는 화면 촬영
- 임의 URL relay
- redirect
- 이미지 cache·대량 저장
- GPS·파일·다운로드 AI 실행

## 운영 전 확인

제한 relay 설계가 Kakao 이용 정책상 허용을 자동 보증하는 것은 아니다. 수업 밖 배포·운영 전 최신 Kakao Maps API 이용정책과 출처표시 정책을 확인하며 법적 허용을 단정하지 않는다.

## 공식 참고

- [Kakao 지도 Web API 레퍼런스](https://apis.map.kakao.com/web/documentation/)
- [Kakao StaticMap 샘플](https://apis.map.kakao.com/web/sample/staticMap/)
- [Kakao Map REST API](https://developers.kakao.com/docs/ko/kakaomap/rest-api)
- [MDN CORS enabled images](https://developer.mozilla.org/en-US/docs/Web/HTML/How_to/CORS_enabled_image)
- [MDN Canvas.toBlob](https://developer.mozilla.org/en-US/docs/Web/API/HTMLCanvasElement/toBlob)
