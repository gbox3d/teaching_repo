[실습 페이지](https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week15_final_exam)

# 15주차 따라하기 — 문제를 읽고 구현 확인하기

## 1. 연습 폴더 준비

수업 전 준비다. 현재 폴더: 새 `web-week15`. [정적 서버](../../tools/static-server/server.mjs)를 복사한다.

```powershell
node server.mjs
```

[문제은행](examples/README.md)에서 w11 폼 저장과 REST 한 문항, 두 폴더를 폴더째 복사한다. 예를 들어 GET 문항은 `web-week15/w12_rest_get/`에 둔다. 브라우저 주소는 `http://localhost:8000/w12_rest_get/`다.

## 2. REST 설정 확인

현재 폴더: 선택한 문제 폴더. `config.example.js`가 수업용 HTTPS 서버 주소와 방명록 번호를 정한다. `const BOOK_ID = 'student01';`의 `student01`을 배정받은 방명록 번호로 바꾼다. 공개 키는 파일에 적지 않는다. 문제 화면을 처음 열면 공개 키를 묻는 창이 뜬다. 배부받은 공개 키를 입력하면 이 브라우저의 localStorage에 저장되고, 같은 주소에서 연 다른 문항도 그 키를 함께 쓴다.

localStorage는 주소(출처)마다 따로다. 다른 브라우저, 포트가 다른 localhost, GitHub Pages 주소에서는 처음 열 때 다시 묻는다. 창을 취소하거나 빈 칸으로 두면 키가 저장되지 않는다. 키가 없거나 틀리면 서버가 HTTP 401을 돌려주고 화면에 목록 확인 실패가 보인다. 키 없이 새로고침하면 다시 묻는다. 잘못 넣었거나 학기마다 키가 바뀌면 화면 제목 아래의 [공개 키 지우기]를 누르고 새 키를 입력한다. 강의자가 [리허설 API](../../tools/guestbook-api/README.md)로 연습할 때는 `config.example.js`의 주소를 `http://127.0.0.1:8787`로 바꾸고 [공개 키 지우기]를 누른 뒤 묻는 창에 `classroom-local`을 입력한다. 이때 같은 PC에서 리허설 API가 실행 중이어야 한다. 자세한 설정은 [공용 설정 안내](../../shared/README.md)를 따른다.

문제 README의 시작 파일 → 할 일 → 확인할 것 → 이 문제의 값 순서로 읽는다. app.js 안의 제공 화면·재조회 기능은 다시 작성하지 않고 config.example.js에서는 BOOK_ID만 바꾼다. `app.js`의 TODO에 해당 요청만 구현한다. 이 따라하기에는 해답 코드가 없다.

## 3. 실제 결과 확인

- GET: 응답 배열이 화면에 표시되는지 본다.
- POST: 입력 → POST 201 → GET 재조회 → 새로고침 후 유지 순서로 확인한다.
- PATCH: 자기 ID를 수정 → 반환 배열 한 행 확인 → 같은 ID를 GET해 수정값 확인.
- DELETE: 자기 ID를 삭제 → 204 확인 → 같은 ID를 GET해 빈 배열 확인.
- 편집 키가 틀리면 HTTP 성공 번호만 보고 완료라고 쓰지 않는다.

편집 키는 실행 화면에 입력하고 코드·URL·localStorage·캡처에 넣지 않는다. 화면에서 편집 키 입력 칸이 비워졌는지 확인한 뒤 캡처한다.

## 4. 수업 뒤 연습 저장소 공개

현재 폴더: 사전에 만든 `web-week15` 맨 위. 이미 연결한 저장소에서는 commit·push만 수행한다. 아래 초기 연결 명령은 사전 준비 때 한 번 사용한다.

```bash
git init
git add .
git commit -m "15주 문제은행 연습"
git branch -M main
git remote add origin https://github.com/<아이디>/web-week15.git
git push -u origin main
```

GitHub Settings → Pages에서 main의 root를 고른다. 공개 URL의 목차 또는 문항 폴더를 연다. REST 문항은 `config.example.js`의 수업용 HTTPS 주소로 확인하며, Pages 주소에서 처음 열면 묻는 창에 공개 키를 입력한다. Node API를 GitHub Pages에 올리는 것만으로 서버가 실행되지는 않는다.

## 5. 시험 당일

현재 폴더: 기존 `web-week15`. 배부받은 `exam/`을 맨 위에 둔다. 안에는 목차와 A~E 시작 파일이 있다. 문제 값·API 공간·초기 글·편집 키는 시험 배부값을 사용한다. REST 문항 폴더의 `config.example.js`에는 시험용 주소가 들어 있다. `BOOK_ID`를 자기 시험 방명록 번호로 바꾸고 REST 문항 화면에서 [공개 키 지우기]를 누른 뒤 배부받은 시험용 공개 키를 입력한다. 같은 주소에 연습 때 넣은 키가 남아 있으면 묻는 창이 뜨지 않기 때문이다. 연습 데이터와 섞지 않는다.

시작 commit을 남기고 구현한다. 종료 전 다시 commit·push한 뒤 공개 URL·저장소 URL·Commits 캡처를 제출한다. 편집 키는 채점자에게 제출하지 않는다. 구술은 강의자가 지정한 코드 한 줄을 설명한다.

시간표와 장애 처리는 [실습지](lab.md), 판단 기준은 [채점표](rubric.md)를 따른다.
