[실습 페이지](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week15_final_exam)

# 15주차 따라하기 — 문제를 읽고 구현 확인하기

## 1. 연습 폴더 준비

현재 폴더: 새 `web-week15`. [정적 서버](../../tools/static-server/server.mjs)를 복사한다.

```powershell
node server.mjs
```

[문제은행](examples/README.md)에서 영역이 다른 세 문항을 선택해 폴더째 복사한다. 예를 들어 GET 문항은 `web-week15/w12_rest_get/`에 둔다. 브라우저 주소는 `http://localhost:8000/w12_rest_get/`다.

## 2. REST 설정 확인

현재 폴더: 선택한 문제 폴더. `config.example.js`의 API 주소·공개 키·BOOK_ID를 강의자 배부값으로 바꾼다. API 주소가 localhost이면 같은 PC에서 [리허설 API](../../tools/guestbook-api/README.md)가 실행 중이어야 한다. 공용 실습은 강의자가 검증한 HTTPS 주소를 사용한다.

문제 README의 시작 파일 → 할 일 → 확인할 것 → 이 문제의 값 순서로 읽는다. `view.js`의 제공 기능은 다시 작성하지 않는다. `app.js`의 TODO에 해당 요청만 구현한다. 이 따라하기에는 해답 코드가 없다.

## 3. 실제 결과 확인

- GET: 응답 배열이 화면에 표시되는지 본다.
- POST: 입력 → POST 201 → GET 재조회 → 새로고침 후 유지 순서로 확인한다.
- PATCH: 자기 ID를 수정 → 반환 배열 한 행 확인 → 같은 ID를 GET해 수정값 확인.
- DELETE: 자기 ID를 삭제 → 204 확인 → 같은 ID를 GET해 빈 배열 확인.
- 편집 키가 틀리면 HTTP 성공 번호만 보고 완료라고 쓰지 않는다.

키는 실행 화면에 입력하고 코드·URL·localStorage·캡처에 넣지 않는다. 화면에서 입력 칸이 비워졌는지 확인한 뒤 캡처한다.

## 4. 연습 저장소 공개

현재 폴더: `web-week15` 맨 위.

```bash
git init
git add .
git commit -m "15주 문제은행 연습"
git branch -M main
git remote add origin https://github.com/<아이디>/web-week15.git
git push -u origin main
```

GitHub Settings → Pages에서 main의 root를 고른다. 공개 URL의 목차 또는 문항 폴더를 연다. REST는 공용 HTTPS API 설정으로 확인한다. Node API를 GitHub Pages에 올리는 것만으로 서버가 실행되지는 않는다.

## 5. 시험 당일

현재 폴더: 기존 `web-week15`. 배부받은 `exam/`을 맨 위에 둔다. 안에는 목차와 A~E 시작 파일이 있다. 문제 값·API 공간·초기 글·편집 키는 시험 배부값을 사용한다. 연습 데이터와 섞지 않는다.

시작 commit을 남기고 구현한다. 종료 전 다시 commit·push한 뒤 공개 URL·저장소 URL·Commits 캡처를 제출한다. 편집 키는 채점자에게 제출하지 않는다. 구술은 강의자가 지정한 코드 한 줄을 설명한다.

시간표와 장애 처리는 [실습지](lab.md), 판단 기준은 [채점표](rubric.md)를 따른다.
