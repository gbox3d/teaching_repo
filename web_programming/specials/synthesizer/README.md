# 웹 신시사이저 특강

브라우저에서 소리를 합성하고, 배열과 JSON으로 연주 순서를 만듭니다. 정규 **12주차의 fetch·JSON 이후**에 선택하는 방학 연구·보강 특강입니다. 정규 시험 범위에 포함하지 않으며 진행 시간에 상한을 두지 않습니다.

## 학습 목표

- Oscillator → Filter → Gain → 출력 노드의 연결을 설명합니다.
- 같은 음에서 파형·주파수·엔벨로프·필터 중 하나를 바꾸고 차이를 기록합니다.
- 16칸 배열을 리듬으로, 구간·마디 객체를 곡으로 표현합니다.
- `fetch`의 상태 확인, JSON 파싱, 실패 처리와 화면 갱신을 구분합니다.
- 멜로디 조합기에서 편집한 곡을 JSON으로 저장하고 다시 불러옵니다.

## 자료와 진행 순서

| 단계 | 자료 | 확인할 결과 |
|---|---|---|
| 소리 비교 | [ex01~ex06 안내](examples/README.md) | 버튼별 수치와 파형·청감 비교 기록 |
| 시간·배열 | [ex07~ex08 안내](examples/README.md) | 호출 시각과 예약 시각의 차이, 변경한 리듬 배열 |
| 정적 JSON | [ex09](examples/ex09_fetch_song.html) · [requests.http](examples/requests.http) | HTTP 200·404, JSON 표와 마디 목록 |
| 연주기 | [따라하기](walkthrough.md) · [연주기](examples/build/index.html) | 제목·BPM·리듬을 수정한 곡 |
| 선택 확장 | [ex10](examples/ex10_melody.html) · [조합기](examples/build/compose.html) | 음의 시작·길이 비교와 JSON 왕복 저장 |
| 연구 기록 | [실습](lab.md) | 예상·변경·관찰 결과와 재현 방법 |

비교 예제는 **10개**입니다. ex01~ex09를 기본 흐름으로 사용하고 ex10과 조합기는 멜로디 연구로 이어갑니다. [한국어 슬라이드](slides.md)와 [영어 슬라이드](slides_en.md)는 각각 16장입니다.

## 실행

Node.js를 설치한 뒤 저장소 루트에서 실행합니다. 추가 패키지는 없습니다.

```powershell
node web_programming/tools/static-server/server.mjs web_programming/specials/synthesizer/examples 8000
```

- 비교 예제: `http://localhost:8000/ex01_wave.html`
- 연주기: `http://localhost:8000/build/`
- 조합기: `http://localhost:8000/build/compose.html`
- 종료: 서버 터미널에서 `Ctrl+C`

`fetch`와 ES 모듈을 사용하는 페이지는 HTTP 서버로 엽니다. 로컬 실습은 HTTP, GitHub Pages 공개 주소는 HTTPS입니다. 곡 JSON은 같은 서버의 정적 파일이며 백엔드·DB·API 키·`.env`가 필요하지 않습니다. 재생은 사용자가 버튼을 누른 뒤 시작합니다.

## 파일 구성

- `examples/ex01_wave.html` ~ `ex10_melody.html`: 비교 화면 10개
- `examples/shared/examples.css`: 비교 화면 공용 CSS
- `examples/ex09_song.json`: JSON 읽기 예제 데이터
- `examples/build/`: 연주기와 조합기 실행 파일 9개 및 사용 안내
- `score/`: 별도 악보 스키마의 참고 JSON 3개와 [형식 안내](score/README.md)

연주기 실행 파일은 `index.html`, `main.css`, `index.js`, `synth.js`, `song.js`, `only_you.json`, `my_song.json`의 **7개**입니다. `compose.html`, `compose.js`를 포함하면 **9개**입니다. 복사할 때는 `build` 폴더 전체를 사용합니다.

## 데이터와 연구 범위

`my_song.json`은 멜로디 없는 8마디 연습곡입니다. `only_you.json`에는 28마디와 136개 멜로디 음이 있고, ex10에도 멜로디가 있습니다. 음원 파일은 포함하지 않습니다. `score/`는 연주기와 형식이 달라 직접 불러올 수 없습니다.

학생이 공개할 결과물에는 직접 만든 곡·멜로디 또는 사용 권한이 있는 자료를 사용합니다. 기존 참고 악보의 재배포 권한을 이 교재가 보증하지 않습니다.

## 참고 문서

- [MDN: Web Audio API 사용](https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API/Using_Web_Audio_API): 오디오 노드와 사용자 조작 후 재생
- [MDN: fetch 사용](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch): `response.ok`와 JSON 파싱
- [web.dev: 두 시계와 오디오 예약](https://web.dev/articles/audio-scheduling): JavaScript 타이머와 오디오 시계의 역할
