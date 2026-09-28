# 웹프로그래밍 실습조교용 설치 프로그램 목록

## 목차

- [필수 설치](#필수-설치)
- [권장 설치](#권장-설치)
- [필요할 때만 설치](#필요할-때만-설치)
- [별도 설치가 없는 서비스](#별도-설치가-없는-서비스)
- [설치 확인](#설치-확인)
- [공용 PC 운영](#공용-pc-운영)
- [학기 중 점검 시기](#학기-중-점검-시기)

## 필수 설치

학생 실습에 필요한 것은 **Git · VS Code · Chrome** 셋이다.
확인과 캡처의 표준이 GitHub Pages 공개 URL이므로, 학생 PC에 서버나 런타임을 설치하지 않아도 15주가 그대로 성립한다.

| 프로그램 | 공식 경로 | 비고 |
|---|---|---|
| [Git for Windows](https://git-scm.com/install/windows) | Git 공식 사이트 | 1주차부터 사용. HTTPS + 브라우저 로그인(Git Credential Manager 포함) |
| [VS Code](https://code.visualstudio.com/docs/setup/windows) | VS Code 공식 사이트 | 코드 편집. **File › Open Folder**로 수업 폴더를 연다 |
| [Chrome](https://www.google.com/chrome/) | Chrome 공식 사이트 | DevTools(Elements·Console·Network·Application)와 기기 모드 375px |

브라우저를 Edge로 대체해야 하면 DevTools 탭 이름이 같은지 먼저 확인한다. 교재의 화면 이름은 Chrome 기준이다.

## 권장 설치

| 프로그램 | 조건 |
|---|---|
| [Node.js LTS](https://nodejs.org/en/download) | 수업용 정적 서버 [`tools/static-server/server.mjs`](tools/static-server/README.md) 실행용(`node server.mjs` → `http://localhost:8000/`). 5주차부터 쓴다. npm 패키지는 설치하지 않는다 |

**5주차 시작 전에 실습실 PC에서 `node -v`가 `v18` 이상으로 나오는지 확인한다.**
막히면 설치 승인을 담당 교수에게 받는다. 설치가 막혀도 4~11주차 예제는 파일을 두 번 눌러(`file://`) 열 수 있고,
12주차 `fetch`와 15주차 기말은 "한 번에 한 가지만 고쳐 push → Pages 확인"으로 진행한다(수정마다 1~3분 대기).
Live Server 확장·`python3 -m http.server`도 같은 일을 하지만, 수업 자료는 `server.mjs` 기준으로 쓴다.

## 필요할 때만 설치

| 프로그램 | 설치 조건 |
|---|---|
| Node.js 24 | 조교의 교재 사이트 빌드(`npm run build`)용. 학생 PC는 위 LTS면 된다 |
| Marp | 조교가 슬라이드 변환까지 담당하는 경우 |
| 그 밖의 VS Code 확장 | 학기별 환경 기준표에 지정된 확장만 설치 |

## 별도 설치가 없는 서비스

- GitHub와 GitHub Pages — 정규 15주에서 쓴다. 브라우저만 있으면 된다.
- Supabase, Kakao Developers — **선택 특강(`specials/`)에서만** 쓴다. 정규 주차 준비물이 아니며, 계정과 key 운영 방식은 담당 교수 안내를 따른다.

## 설치 확인

```powershell
git --version
code --version
```

Chrome 버전은 주소창에 `chrome://version`을 넣어 확인한다.
Node.js는 조교 빌드 PC에서만 `node --version`·`npm --version`으로 확인한다.

새 실습 계정으로 **GitHub 가입 → 저장소 생성 → Settings › Pages(main · /(root)) → 공개 URL 열기**까지 한 번 통과해 두면
2주차 수업에서 화면 이름이 바뀐 곳을 미리 찾을 수 있다.

정확한 Git·VS Code·Chrome 버전은 [학기별 환경 기준표](../environment_baseline_template.md)에서 담당 교수가 확정한다.

## 공용 PC 운영

### 자격 증명 삭제 (매 실습 끝 5분)

공용 PC에 GitHub 로그인이 남으면 다음 사용자가 push할 때
`remote: Permission to student01/my-web.git denied to <다른 아이디>` 오류가 난다. 학생이 직접 다음 순서로 지운다.

1. 시작 메뉴에서 **자격 증명 관리자**(Credential Manager)를 연다
2. **Windows 자격 증명** 탭을 고른다
3. 목록에서 `git:https://github.com`을 펼쳐 **제거**를 누른다
4. 다음 학생이 처음 push할 때 브라우저 로그인 창이 다시 뜨면 정상이다

로그오프 시 자동으로 지우는 배치 스크립트를 함께 쓸지는 담당 교수가 정한다.

### Pages 반영 지연

- push 뒤 공개 페이지 반영에 1~3분이 걸린다.
- 5분 안에 안 보이면 로컬 화면 캡처와 GitHub **Commits** 탭 캡처를 같은 점수로 인정하고, 다음 수업 시작 5분에 다시 확인한다.
- 조교는 실습 끝에 "push → 새로고침 → 캡처 → 자격 증명 삭제" 순서를 돌아다니며 확인한다. 4주차부터는 매주 새 저장소 `web-weekNN`이므로 1일차 끝(50–60분)에 저장소 만들기와 **Settings › Pages** 켜기까지 확인한다.

### clone·로그인이 막힌 학생

교재의 지난주 완성본(`examples/build/`, 3주차 이전은 `examples/day2/`)을 받아 그 폴더에서 작업하게 한다. 4주차부터는 매주 새 저장소라 실습 끝의 `git init` → `git remote add origin <URL>` → `git push -u origin main` 순서가 그대로 적용된다. 2일차에 clone이 막히면 1일차에 올린 저장소를 **Code › Download ZIP**으로 받아 작업하고, 끝에 조교와 함께 push한다.

### 개인 노트북

macOS·Linux 개인 노트북에서 `Username for 'https://github.com':`이 나오면 Git Credential Manager가 없는 경우다.
표준 대응(Credential Manager 설치 안내 / SSH 키 / 실습실 PC 사용)은 담당 교수가 하나로 정한다.

## 학기 중 점검 시기

| 시기 | 점검 항목 |
|---|---|
| 개강 전 | Git·VS Code·Chrome 설치와 버전, 새 실습 계정으로 GitHub 가입 → 저장소 생성 → Pages 켜기 화면 재확인 |
| 5주차 전 | 실습실 PC `node -v`(v18 이상). 막히면 Node.js LTS 설치 승인 요청 |
| 매 실습 끝 | 학생이 push·Pages 확인·자격 증명 삭제를 마쳤는지 |
| 14주차 전 | 발표 제출 URL 전수 확인(새 시크릿 창에서 열기) |
