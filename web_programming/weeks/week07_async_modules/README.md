# 7주차 — ES Module과 비동기 처리

한 파일에 섞여 있던 데이터 요청, 변환, DOM 출력을 ES Module로 나눈다. `fetch` 결과를 기다리는 동안 loading·empty·success·error 상태를 구분하고, HTTP 오류와 데이터 모양 오류를 재현해 사용자에게 설명 가능한 UI를 만든다.

## 학습 목표

1. `export`/`import`와 module graph를 설명한다.
2. 로컬 서버에서 `<script type="module">`을 실행하고 Network 탭으로 의존 파일을 추적한다.
3. Promise 상태와 `async`/`await`의 실행 순서를 예측한다.
4. `fetch`의 HTTP 응답과 네트워크 실패를 구분한다.
5. 비동기 UI의 loading·empty·success·error 상태를 각각 검증한다.

## 1·2일차 흐름

| 일차 | 설명·시연 30분 | 직접 해결 실습 60분 |
|---|---|---|
| 1일차 | module graph, import/export, 관심사 분리 | 데이터·UI·진입점 모듈화와 검색 통계 |
| 2일차 | Promise, fetch, `response.ok`, UI 상태 | 네 종류 결과와 재시도·오래된 응답 방어 |

## 자료

- [PT 원고](slides.md)
- 강의 대본: 강의자 별도 관리(비공개)
- [실습 문제](lab.md)
- [실행 예제 안내](examples/README.md)
- [module/fetch starter](examples/starter/index.html)

## 실행

ES Module과 `fetch`는 로컬 파일 URL이 아니라 HTTP 서버에서 확인한다.

```bash
cd examples/starter
python -m http.server 8000
```

`http://localhost:8000`을 열고 DevTools의 Console과 Network 탭을 함께 사용한다.

## 완료 기준

- 모듈별 책임과 import 방향을 그림으로 설명한다.
- 정상 JSON을 카드 목록으로 출력한다.
- 빈 배열은 오류가 아니라 empty 안내로 표시한다.
- 없는 URL, 배열이 아닌 JSON을 서로 다른 관찰 근거와 함께 처리한다.
- 빠른 연속 요청에서 오래된 응답이 최신 화면을 덮지 않게 한다.
- 기능 commit, Network 증거, 오류 상태 캡처를 남긴다.

## 다음 주 연결

8주차 중간 실기에서는 GitHub Pages, 시맨틱 HTML·CSS, DOM과 event를 개인이 통합한다. 7주차의 module/fetch는 시험 핵심 범위와 프로젝트 심화 경계를 강의 시간에 별도 고지한다.
