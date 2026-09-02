---
marp: true
theme: default
paginate: true
header: 웹프로그래밍 특강
footer: 사람과 AI가 같이 쓰는 Kakao 항공 지도 Canvas
---

# 사람과 AI가 같이 쓰는 페이지

## AI와 인간의 공감

Kakao SKYVIEW · 제한 relay · Canvas · 명시적 공동 작업 API

---

## 오늘 완성할 흐름

~~~text
주소 / GPS → Kakao 지도
                  ↓
       공식 StaticMap SKYVIEW 한 장
                  ↓
          엄격한 로컬 relay
                  ↓
              Canvas
                  ↕
        사람·AI 공동 작업 API
~~~

---

## 공감은 capability 계약이다

- 무엇을 함께 읽을 수 있는가?
- 어떤 명령을 함께 실행할 수 있는가?
- 무엇은 사람만 시작하는가?
- 누가 무엇을 실행했는가?
- 되돌릴 수 있는가?

“AI가 할 수 있다”보다 “어떤 경계에서 할 수 있다”가 먼저다.

---

## 사람 전용 capability

| capability | 이유 |
|---|---|
| GPS 권한 | 위치 정보 동의 |
| 로컬 파일 선택 | 개인 데이터 경계 |
| 최종 다운로드 | 외부 효과 발생 |

이 세 기능은 UI에서 사람이 직접 시작한다.

<code>execute()</code>로 요청하면 <code>PROTECTED_COMMAND</code>로 거부된다.

---

## 사람·AI 공용 capability

- 현재 상태 읽기
- 주소 검색
- 좌표 이동
- 지도 유형 변경
- 정적 항공뷰 한 장 준비
- 회전·밝기·대비
- 텍스트 추가
- 실행 취소
- 현재 Canvas Blob 또는 Data URL 읽기

각 명령은 이름과 가역성 metadata를 공개한다.

---

## 전체 module 구조

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

---

## 설정은 Git 최상위 한 곳

~~~json
{
  "kakaoMaps": {
    "javascriptKey": "발급받은-JavaScript-키"
  }
}
~~~

경로:

~~~text
<저장소 루트>\config.json
~~~

- <code>/config.json</code> Git 제외
- JavaScript SDK domain: <code>http://localhost:3000</code>
- REST API 키·Admin 키 미사용

---

## JavaScript 키는 브라우저에서 보인다

~~~text
config.json
  → /runtime-config.json
  → Kakao JavaScript SDK
~~~

- 저장소 제외와 runtime 비공개는 다른 문제
- 허용 도메인과 사용량 관리
- runtime 응답은 key와 setup 여부만 전달
- relay도 JavaScript SDK가 생성한 image URL만 사용

---

## 주소를 좌표로

~~~js
const first = results[0];
const position = new kakao.maps.LatLng(
  Number(first.y),
  Number(first.x)
);
~~~

- <code>x</code>: 경도
- <code>y</code>: 위도
- <code>LatLng</code>: 위도, 경도

AI가 좌표를 제안해도 이 계약을 검증한다.

---

## GPS는 사람이 결정

~~~js
navigator.geolocation.getCurrentPosition(
  usePosition,
  showAlternative
);
~~~

- 사람이 버튼을 눌러 요청
- 승인·거부·시간 초과 구분
- 거부해도 주소·좌표 사용 가능
- 서버·파일에 자동 저장하지 않음

---

## SKYVIEW와 HYBRID

~~~js
map.setMapTypeId(kakao.maps.MapTypeId.SKYVIEW);
map.setMapTypeId(kakao.maps.MapTypeId.HYBRID);
~~~

- 동적 지도는 위치 탐색과 확대 수준 결정
- 공식 <code>MapTypeId</code>만 허용
- 동적 타일 URL은 열거하거나 조합하지 않음

---

## 공식 SDK가 정적 항공뷰를 만든다

~~~js
new kakao.maps.StaticMap(container, {
  center: new kakao.maps.LatLng(latitude, longitude),
  level,
  mapTypeId: kakao.maps.MapTypeId.SKYVIEW
});
~~~

앱이 이미지 URL을 조립하지 않는다.

공식 SDK가 만든 컨테이너에서 완전히 로드된 이미지가 정확히 한 개인지 확인한다.

---

## 직접 Canvas에 그리면?

StaticMap image는 Kakao origin의 cross-origin resource다.

~~~text
Kakao image element
  → localhost Canvas에 직접 drawImage
  → tainted Canvas
  → getImageData / toBlob / toDataURL 차단
~~~

same-origin Blob으로 다시 받아야 Canvas에서 읽고 저장할 수 있다.

---

## 제한 relay의 목적

~~~text
SDK가 만든 단일 image URL
  → cross-origin 직접 image 확인 GET 1회
  → browser exact origin/path 검사
  → localhost relay
  → 같은 image resource 재요청 GET 1회
  → server allowlist 재검사
  → JPEG/PNG no-store 응답
  → same-origin Blob
~~~

일반 목적 proxy가 아니다.

---

## 브라우저 쪽 검증

- 위도 −90~90, 경도 −180~180
- 너비 160~1280
- 높이 120~960
- 지도 level 1~14
- exact HTTPS origin과 path
- 요청 Host와 same-origin Sec-Fetch-Site·Referer(및 전달된 Origin)
- username·password·port·fragment 없음
- decoded image 최대 200만 화소
- 응답 크기와 요청 크기 일치

query field를 만들거나 해석하지 않는다.

---

## 서버 쪽 검증

- GET, source 정확히 한 개
- URL 길이 최대 2048
- exact origin·path
- 정해진 parameter만 한 번씩
- <code>service=open</code>
- redirect 거부
- timeout 10초
- 응답 JPEG·PNG, 최대 8MB
- 동시 한 요청, 최소 500ms 간격
- <code>cache-control: no-store</code>

---

## 하지 않는 일

- 동적 지도 타일 열거
- 여러 타일 수집·조합
- 임의 URL relay
- redirect 추적
- 화면 전체 읽기
- 화면 촬영
- relay 응답 cache
- 대량 저장

한 위치와 동일한 StaticMap image resource라는 경계를 유지한다. 네트워크 GET은 직접 확인 1회와 origin-clean relay 재요청 1회, 총 2회다.

---

## Kakao 출처 영역

~~~text
┌──────────────────────┐
│ 원본 StaticMap 전체  │  고정 크기·배율 1·중심 회전
│                      │  화면 밖만 clip
│ attribution 80×32px  │  좌하단에 마지막 합성
└──────────────────────┘
~~~

- 회전 전후 Canvas 크기 불변
- 좌하단 출처 표지만 별도 보관
- 필터·주석·회전 뒤 같은 좌하단에 마지막 합성

---

## 로컬 파일도 같은 editor

- 사람이 선택한 PNG·JPEG·WebP
- 20MB 이하
- 최대 2,400만 화소
- 외부 URL 입력 없음
- 서버 upload 없음
- attribution 너비·높이 0

StaticMap Blob과 로컬 파일은 source 경로는 다르지만 같은 편집 상태 모델을 쓴다.

---

## 명시적 공동 작업 API

~~~js
const lab = window.aerialCanvasLab;

lab.getState();
await lab.execute("setMapType", { type: "HYBRID" });
await lab.execute("loadAerialView");
const blob = await lab.getImageBlob("png");
~~~

전역 객체와 capability 목록은 frozen 상태다.
공개 인터페이스의 actor는 항상 AI로 고정되며 호출자가 human으로 위장하거나 summary를 덮어쓸 수 없다.

---

## getState()

~~~text
location
  latitude, longitude, label

map
  ready, busy, type

workspace
  sourceKind, transform, size, annotations

boundaries
  browserScreenAccess=false
  gpsPermission=human-only
  fileSelection=human-only
  download=human-only
~~~

---

## execute()와 allowlist

| command | reversible |
|---|---|
| findAddress | true |
| setLocation | true |
| setMapType | true |
| loadAerialView | false |
| setTransform | true |
| addText | true |
| undo | false |

command는 직렬 실행한다. <code>loadAerialView</code>는 별도 좌표 payload 없이 현재 공유 위치를 사용한다. unknown·protected command도 거부 결과를 활동 로그에 남긴다.

---

## 활동 기록

~~~json
{
  "actor": "ai",
  "command": "setTransform",
  "status": "success",
  "summary": "회전 0°, 밝기 105%, 대비 115% 적용",
  "timestamp": "2026-08-26T04:00:00.000Z"
}
~~~

- UI 공동 작업 기록
- <code>collaboration-activity</code> event
- 사람이 한 일과 AI가 한 일을 구분
- 되돌릴 수 있는 명령인지 capability에서 확인

---

## 이미지를 명시적으로 공유

~~~js
const blob = await lab.getImageBlob("png");
const dataUrl = await lab.getImageDataUrl("jpeg");
~~~

- 현재 Canvas만 반환
- 다른 브라우저 영역은 읽지 않음
- 다운로드를 시작하지 않음
- 성공·실패 모두 status가 있는 <code>readAerialImage</code> 활동 기록
- 진행 중인 사람 stroke를 종료·commit하지 않는 read-only snapshot

human-only는 협업 API 계약이며, 브라우저 전체 제어를 위임받은 자동화 도구를 격리하는 보안 sandbox는 아니다.

---

## 다운로드는 사람 전용

| 동작 | AI | 사람 |
|---|---:|---:|
| Canvas Blob 읽기 | 가능 | 가능 |
| 편집 명령 | allowlist | allowlist |
| PNG·JPEG 파일 저장 | 불가 | 버튼으로 실행 |

공유 데이터 접근과 외부 효과를 분리한다.

---

## REST 정적 지도 API와 구분

<code>GET /v2/maps/staticmap</code>:

- REST API 키
- PNG·JPEG binary
- 현재 문서에 SKYVIEW 선택 parameter 없음

현재 구현:

- JavaScript 키
- 공식 Web SDK StaticMap(SKYVIEW)
- SDK가 생성한 단일 image URL 제한 relay

---

## 70분 실습

~~~text
준비 5분
  → 위치·human-only 15분
  → 단일 StaticMap relay 15분
  → 공동 작업 API 20분
  → 편집·이미지 공유·저장 15분
~~~

각 단계:

**문제 → 예상 → 구현 → 관찰 → 오류 설명 → 확장**

---

## 완료 질문

1. 일반 proxy와 이번 relay의 차이는 무엇인가?
2. 왜 공식 SDK가 만든 한 image만 받는가?
3. Canvas가 same-origin이 되는 시점은 어디인가?
4. 어떤 capability가 human-only인가?
5. AI 행동은 어떤 metadata로 기록되는가?
6. <code>getImageBlob()</code>과 다운로드는 어떻게 다른가?
7. 화면 전체를 읽지 않는다는 근거는 어디에 보이는가?

---

## 운영 전 확인

제한 relay라는 기술 설계만으로 Kakao 이용 정책상 허용이 자동 보증되지는 않는다.

수업 밖 배포·운영 전 최신 Kakao Maps API 이용정책과 출처표시 정책을 확인한다. 법적 허용을 단정하지 않는다.

---

## 공식 문서

- [Kakao Web API 레퍼런스](https://apis.map.kakao.com/web/documentation/)
- [Kakao StaticMap 샘플](https://apis.map.kakao.com/web/sample/staticMap/)
- [Kakao Map REST API](https://developers.kakao.com/docs/ko/kakaomap/rest-api)
- [MDN CORS enabled images](https://developer.mozilla.org/en-US/docs/Web/HTML/How_to/CORS_enabled_image)
- [MDN Canvas.toBlob](https://developer.mozilla.org/en-US/docs/Web/API/HTMLCanvasElement/toBlob)
- [MDN Geolocation](https://developer.mozilla.org/en-US/docs/Web/API/Geolocation/getCurrentPosition)
