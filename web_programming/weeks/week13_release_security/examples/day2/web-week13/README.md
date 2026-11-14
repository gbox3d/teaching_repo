# 13주차 온라인 방명록

## 목차

- [실행](#실행)
- [설정](#설정)
- [파일](#파일)

## 실행

이 폴더를 정적 서버로 열고 `guestbook.html`로 이동한다. `file://`로 열지 않는다.
강의자가 제공한 HTTPS API를 사용할 때 GitHub Pages에서도 같은 파일을 연다.

## 설정

`config.example.js`의 API 주소·공개 키·방명록 번호를 강의자 안내값으로 바꾼다.
기본값은 내 PC의 로컬 API `http://127.0.0.1:8787`이다. 공용 서비스 주소가 아니다.
HTTPS 페이지에서 이 로컬 API를 호출하지 않는다. 로컬 연습은 HTTP 정적 서버를 함께 사용한다.
공용 HTTPS API가 준비되기 전에는 로컬 실습으로 진행하며, 다른 기기 공유는 공용 API 설정 후 확인한다.

## 파일

- `guestbook.html`: 온라인 방명록 화면
- `config.example.js`: 공개 설정 세 줄
- `guestbook.js`: GET과 목록 표시
- `submit.js`: POST와 폼 처리
- `index.html`·`about.html`·`app.js`·`styles.css`·`images/profile.png`: 11주차에서 이어 쓰는 파일
