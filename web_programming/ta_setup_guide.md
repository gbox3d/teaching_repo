# 웹프로그래밍 실습조교용 설치 프로그램 목록

## 목차

- [필수 설치](#필수-설치)
- [권장 설치](#권장-설치)
- [필요할 때만 설치](#필요할-때만-설치)
- [별도 설치가 없는 서비스](#별도-설치가-없는-서비스)
- [설치 확인](#설치-확인)
- [공용 PC 운영](#공용-pc-운영)
- [학기 중 점검 시기](#학기-중-점검-시기)
- [REST 방명록과 홈 IoT 준비](#rest-방명록과-홈-iot-준비)

## 필수 설치

일반 차시는 강의·시연 60분과 학생 실습 30분이다. 설치와 예제 폴더 배부는 수업 전에 마치고 강의 첫 5분에 실행 상태를 확인한다. Git 자체를 배우는 1~2주를 제외하면 새 저장소 준비와 업로드 시간을 학생 실습에 넣지 않는다.

| 프로그램 | 사용 시점과 확인 |
|---|---|
| [Git](https://git-scm.com/install/windows) | 1주부터 사용. Windows는 Git Credential Manager를 포함한 배포본과 HTTPS 브라우저 로그인을 확인 |
| [VS Code](https://code.visualstudio.com/docs/setup/windows) | 코드 편집. File › Open Folder로 예제 폴더 열기 |
| [Chrome](https://www.google.com/chrome/) | Elements·Console·Network·Application과 375px 기기 모드 |
| [Node.js](https://nodejs.org/en/download) | 교재 실행 기준은 24 이상. 5주 전 정적 서버 실행 확인. 학생 예제의 npm 패키지 설치는 없음 |
| [REST Client](https://marketplace.visualstudio.com/items?itemName=humao.rest-client) | 12주 전 VS Code에 humao.rest-client 설치. .http의 Send Request로 JSONPlaceholder 할 일과 Open-Meteo 기온 확인 |

브라우저를 Edge로 대체할 때는 DevTools 이름과 예제 동작을 먼저 확인한다. Node 설치가 막힌 실습실은 담당 조교가 승인된 대체 정적 서버를 미리 준비한다. 수업 도중 매번 push하고 배포를 기다리는 방식을 30분 실습의 기본 환경으로 삼지 않는다.

## 권장 설치

Marp 확장은 조교가 슬라이드를 미리 볼 때 사용한다. 학생의 HTML·CSS·JavaScript 실습에 필수는 아니다. VS Code의 Markdown 미리보기는 별도 확장 없이 사용할 수 있다.

7주 전 cdnjs의 W3.CSS 4.1.0 연결을 확인한다. 라이브러리 파일은 별도로 설치하지 않는다. 7주 변환 이후와 9~14주 방명록은 같은 CDN을 사용한다. 11주 저장 기초와 배열 심화도 같은 CDN을 사용한다.

## 필요할 때만 설치

| 프로그램·준비 | 조건 |
|---|---|
| 교재 빌드 의존성 | 조교가 저장소 루트에서 npm ci와 npm run build를 실행할 때만 설치 |
| Marp 변환 도구 | PDF 등 별도 형식의 슬라이드를 생성할 때 |
| 특강별 설정 | 지도 API 키, Supabase 새 프로젝트 등 해당 특강의 안내를 따름 |

## 별도 설치가 없는 서비스

- GitHub·GitHub Pages: 2주부터 브라우저로 설정한다.
- Supabase: 13·14주 방명록은 강의자가 API를 준비하므로 학생 계정·SQL·SDK가 필요 없다. 구축 특강에서는 학생 또는 소그룹 담당자가 새 프로젝트를 준비한다.
- Kakao Developers: 지도 특강에서 계정·도메인·키 설정을 다룬다.

## 설치 확인

```powershell
git --version
code --version
node --version
```

Chrome은 `chrome://version`에서 확인한다. REST Client는 .http 요청 위에 Send Request가 나타나는지 확인한다. 정확한 버전은 [학기별 환경 기준표](../environment_baseline_template.md)에 기록한다.

저장소 루트 `teaching_repo`에서 전체 웹 예제를 열 때는 다음 명령을 쓴다.

```powershell
node web_programming/tools/static-server/server.mjs web_programming 8111
```

`http://localhost:8111/`에서 해당 주 폴더를 연다. 학생의 단독 주차 폴더에는 [server.mjs](tools/static-server/server.mjs)를 배부하고 `node server.mjs`로 `http://localhost:8000/`을 연다. Node 서버는 파일을 제공하며 Supabase 데이터베이스를 실행하는 서버가 아니다.

학기 전 실습 계정으로 GitHub 저장소 생성 → Settings › Pages의 main·/(root) → 실제 배포 주소 열기를 확인한다. 배포가 즉시 끝난다고 보장하지 않고 Pages·Actions의 배포 상태를 확인한다.

## 공용 PC 운영

### 자격 증명 삭제

공용 PC에서 업로드를 마친 뒤 GitHub 로그인과 저장된 Git 자격 증명을 정리한다.

1. Windows의 자격 증명 관리자를 연다.
2. Windows 자격 증명에서 `git:https://github.com` 항목을 제거한다.
3. 브라우저의 GitHub 계정도 로그아웃한다.

환경에 따라 GitHub 관련 항목 이름이 다를 수 있다. 반복적으로 다른 계정의 push 오류가 나면 [실습실 PC 로그인 정리 도구](../tools/github-classroom-pc-reset/README.md)의 절차를 따른다.

### Pages 반영 지연

수업 중에는 로컬 동작과 캡처를 확인한다. 3주 이후 push·Pages 확인은 수업 뒤 정리이며, 배포가 늦으면 로컬 결과와 Commits 탭을 남긴다. 다음 수업 준비 시간에 공개 주소를 다시 확인한다. 1~2주와 시험의 제출 형식은 해당 주차 안내를 따른다.

### clone·로그인이 막힌 학생

전 주 완성본 또는 강의자 배부 폴더로 시작한다. 교재 저장소 전체 ZIP에서 해당 예제 폴더를 복사하면 파일별 Raw 다운로드를 반복하지 않아도 된다. 공용 자산을 읽는 예제는 shared 폴더와 상대 경로도 유지한다. 로그인·저장소 복구는 수업 전후에 조교가 지원한다.

### 개인 노트북

macOS·Linux도 같은 Node 정적 서버와 브라우저 예제를 쓴다. Git 인증 방식은 분반 공지로 통일한다. 학생별 계정·편집 키·실제 개인정보를 실습 화면이나 요청 이력 캡처에 남기지 않는다.

## 학기 중 점검 시기

| 시기 | 점검 항목 |
|---|---|
| 개강 전 | Git·VS Code·Chrome, 배부 폴더, 실습 계정의 저장소·Pages 동작 |
| 매 차시 전 | 시작 폴더, 오늘 필수 예제, localhost 실행, 링크·공용 자산 |
| 5주 전 | Node.js 24 이상과 server.mjs 실행 |
| 7주 전 | W3.CSS CDN, 변환 전 파일·제공 JS, 375px 폼 동작 |
| 9주 전 | README 시작 틀·제공 SVG·캡처 폴더, 발표 인원·전환 시간 |
| 11주 전 | 같은 origin의 폼 저장·복원, 예제별 저장 키, 강의자 시연본 구분 |
| 12주 전 | REST Client, JSONPlaceholder와 Open-Meteo의 GET, 브라우저에서 응답 읽기 |
| 13주 전 | 수업용 주소·공개 키·태그 배부, POST·GET, 두 브라우저의 같은 글 |
| 14주 전 | 편집 키 배부, 올바른 키·틀린 키, PATCH·DELETE 뒤 대상 재조회 |
| 8·15주 전 | 문제은행 범위·시작 파일, 실제 제한시간, 로컬 대체 환경·시험 전용 태그 |
| 연구 특강 전 | 각 특강 README의 계정·포트·도메인·시작 파일과 실행 조건 |

## REST 방명록과 홈 IoT 준비

공용 API는 [강의자 준비 안내](tools/guestbook-api/README.md)에 따라 점검한다. 학생에게 HTTPS API 주소·공개 키·book_id를 배부한다. book_id는 글을 구분하는 태그이며 로그인이나 비밀 값이 아니다. 14주 편집 키는 별도로 배부한다.

12주 선택 방명록과 13·14주 방명록 예제는 제공 설정 패널에서 주소·공개 키·태그를 적용한다. 설정과 편집 키는 메모리에만 두므로 새로고침 후 다시 입력한다. .http의 .env는 REST Client가 읽으며 브라우저 설정을 자동으로 바꾸지 않는다. 상세 연결은 해당 주 예제 README를 따른다.

`http://127.0.0.1:8787`과 `classroom-local`은 선택 로컬 모의 API용 값이다. 이것으로 공용 서버나 다른 기기의 공유를 검증했다고 기록하지 않는다. 로컬 HTTP 화면에서 공용 HTTPS API를 호출할 수 있으며, Pages 화면과 공용 API는 모두 HTTPS를 사용한다.

[Supabase 특강](specials/supabase_guestbook/README.md)은 새 연습 프로젝트의 서버 구축을 다룬다. [홈 IoT 특강](specials/home_iot_http/README.md)은 학생 PC에서 Node.js 서버를 실행한다. 홈 IoT는 실제 보드나 npm 패키지 없이 `node examples/simulator/server.mjs`와 `http://localhost:8014/`로 실습한다. GitHub Pages는 이 Node 서버를 실행하지 않는다.

연구 특강의 전체 분량과 차시 수는 제한하지 않는다. 실습 준비와 API·정적 화면·시뮬레이터의 역할을 구분해 배부한다.
