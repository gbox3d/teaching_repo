# 2주차 예제 — 이동 가능한 정적 사이트

## 구성

- [`broken-site/index.html`](broken-site/index.html): 진단 실습용 정상 기준선
- `broken-site/assets/styles.css`: 표현
- `broken-site/assets/app.js`: asset 연결 확인 동작
- `broken-site/assets/campus-mark.svg`: 로컬 SVG 이미지
- `server.mjs`: 예제 파일만 제공하는 설치 없는 로컬 HTTP 서버

폴더 이름은 “오류를 심고 복구하는 대상”이라는 뜻이다. 저장된 기준선 자체의 상대경로와 대소문자는 정상이다.

## 실행

`examples` 폴더에서 다음을 실행한다.

```powershell
node server.mjs
```

브라우저에서 `http://localhost:8000/broken-site/`을 연다. 외부 package나 네트워크가 필요하지 않으며 종료는 `Ctrl+C`다. GitHub Pages에 push한 뒤에는 공개 URL로 다시 검증한다.


## 기준선

- title: `Campus Web Lab`
- image: `assets/campus-mark.svg`
- CSS와 JS는 모두 `./assets/...` 상대경로
- 버튼 클릭 뒤 `배포 자산 연결: 정상`

## 실습 변형

원본이 아닌 복사본에서 한 번에 하나만 바꾼다.

1. root-relative `/assets/styles.css`
2. 대소문자가 다른 `Campus-Mark.svg`
3. 존재하지 않는 `assets/apps.js`

각 변형은 별도 commit으로 만들고 공개 Network의 실패 URL을 기록한 뒤 복구한다.
