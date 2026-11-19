# 2주차 구현·검증 기록

2026-11-18에 C01의 2-1·2-2 차시를 기준으로 조사·수정했다. 담당 범위는 `weeks/week02_github_pages/`와 이 보고서다. 강의자의 요청에 따라 다른 주차·공통 도구·다른 과목·기존 동시 변경은 수정하지 않았다. 실제 계정 생성, 원격 push, commit은 실행하지 않았다.

## 조사 범위

주차 폴더의 파일은 13개다. 원고·안내 6개, 실행 파일 7개를 모두 읽고 비교했다. 별도 이미지·폰트·CDN 자산은 없다.

| 파일 | 조사와 처리 |
|---|---|
| `README.md` | 60+30 시간표, 사전 준비·필수·시연·선택, merge 전후 완료 기준, 4장 캡처 예외, 3주 인계, 공식 문서 근거 수정 |
| `lab.md` | 두 차시의 30분 실습 분해, 제공 파일 사용, Pages 지연 증거, 저장소 삭제를 요구하던 오류 복구 안내 수정 |
| `walkthrough.md` | 모든 명령·기대 결과·전문 코드 확인. 제공 파일과 전체 재입력 구분, CSS 전문 동기화, 인증·배포·commit 개수 단정 완화 |
| `examples/README.md` | 7개 실행 파일과 변경표 조사. 차시별 수정량, 모바일 CSS 설명, JS 제공 범위, 3주 인계 추가 |
| `slides.md` | 기존 21장 유지. 두 차시 60+30, 필수/선택, 4장 제출, Pages 지연, main 인계 및 장문 슬라이드 조정 |
| `slides_en.md` | 기존 21장 유지. 한국어판과 같은 시간·수정·확인 범위로 조정. HTML 문자열·commit 메시지를 실제 예제와 맞춤 |
| `examples/day1/index.html` | 완성 제목·버튼·상태·CSS/JS 경로 확인. 사이트 소개 본문은 짧고 목적에 맞아 보존 |
| `examples/day1/styles.css` | 카드의 border-box와 제목 단어 단위 줄바꿈 추가. 기초 CSS 유지 |
| `examples/day1/app.js` | 클릭마다 1 증가, 새로고침 0, DOM ID·실제 실행 확인. 변경 불필요 |
| `examples/day2/index.html` | day1에서 소개 링크 한 줄이 추가된 상태 확인. 왕복 탐색 실행. 변경 불필요 |
| `examples/day2/about.html` | 소개 한 줄과 돌아가기 링크, CSS만 연결한 구조 확인. 사이트 소개 본문 보존 |
| `examples/day2/styles.css` | day1과 같은 모바일 수정. 두 CSS 파일 내용 일치 확인 |
| `examples/day2/app.js` | day1과 같은 코드·동작 확인. 변경 불필요 |

## 차시별 학생 작업

| 차시 | 강의·시연 60분 | 학생 실습 30분 |
|---|---|---|
| 2-1 | 준비 5, GitHub·remote 15, 첫 push 15, Pages 15, 공개 경로 5, 안내 5 | my-web 준비 5, push 10, 제목 변경·push 5, Pages·캡처 10 |
| 2-2 | 준비 5, branch·switch 15, 파일 추가 10, merge 15, Pages 비교 10, 안내 5 | about 브랜치 5, 제공 HTML의 소개·왕복 링크 10, commit·push·merge 10, 확인 5 |

사전 준비는 도구 설치·계정/이메일 확인·배부 파일 확보다. Git 자체를 배우는 주이므로 새 저장소·push·branch·merge는 수업 안에 남겼다. 학생이 HTML/CSS/JS 전체를 처음부터 입력한다는 요구를 제거했다. 첫날 h1 한 줄, 둘째 날 제공 소개 한 줄과 왕복 링크가 코드 수정 범위다. 브랜치 삭제·추가 페이지·SSH·clone/pull은 수업 뒤 선택이다.

캡처 네 장은 저장소·공개 홈·merge 전 브랜치·공개 소개다. 배포가 늦으면 로컬 화면과 GitHub commit 증거로 먼저 확인하고 공개 화면을 보완한다. 배포 지연 상태를 공개 검증 완료로 표시하지 않는다.

## 실행·대조 결과

Chrome DevTools MCP는 두 호출 모두 기존 chrome-profile 사용 중 오류였다. 공유 브라우저를 재설정하지 않고 이미 설치된 Playwright와 독립 headless Chrome을 사용했다. 실행 주소는 기존 로컬 서버의 `http://localhost:8111/weeks/week02_github_pages/examples/`다.

| 검증 | 실제 결과 |
|---|---|
| 모바일 원인 재현 | 세 HTML에서 기존 content-box를 브라우저 CSS로 재현하니 viewport 375px, scrollWidth 391px였다 |
| 수정 후 모바일 | day1 홈·day2 홈·소개 모두 viewport 375px, scrollWidth 375px, 카드 폭 343px. 캡처를 열어 제목·버튼·링크를 확인했다 |
| 데스크톱 | 세 HTML 모두 viewport/scrollWidth 1280px, 카드 폭 576px |
| HTTP 자산 | 세 HTML 200, 각 CSS/JS 요청 200. 외부 자산 없음 |
| 홈 버튼 | 두 홈에서 키보드 Enter·Space 입력 후 `클릭 횟수: 2`, 새로고침 후 `클릭 횟수: 0` |
| 페이지 탐색 | day2 홈→소개→홈 링크, 소개 직접 주소·새로고침, 브라우저 뒤로·앞으로 실행 성공 |
| 브라우저 오류 | 검사 중 pageerror 0건 |
| JS 구문 | day1/day2 `app.js` 각각 `node --check` 통과 |
| 전문 코드 | walkthrough의 HTML/CSS/JS 전문 6개를 실파일과 대조하여 일치. 시작 HTML만 의도한 h1 변경 전 값으로 비교 |
| 차시 파일 인계 | day1/day2 CSS·JS 각각 내용 일치. day2 홈의 추가는 소개 링크 한 줄 |
| 로컬 문서 링크 | Markdown 상대 경로·heading anchor 57개 확인, 누락 0건 |
| 한영 덱 | 기존과 수정 후 모두 각 21장. 설치된 Marp와 교재 테마로 렌더하여 720px 높이에서 section scrollHeight 넘침 0장 |
| 문체·공백 | UI 문구 검사, 한국어 문서 검사, 담당 경로 `git diff --check` 통과 |

브라우저 반복 검사와 문서 대조는 임시 실행 스크립트로 수행했다. 새 테스트·의존성·공통 스크립트는 추가하지 않았다. 제목 줄바꿈 수정 뒤 모바일 캡처도 다시 확인했다.

## 공식 자료 확인

GitHub UI·인증·배포 설명은 2026-11-18에 다음 공식 문서를 읽고 반영했다. UI 문구의 버전 차이를 허용하고, 공개 반영 시간을 1분으로 보장하던 표현을 제거했다.

- [Pages 게시 원본 설정](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site): branch 배포, main과 root 선택.
- [Pages 사이트 생성·게시 확인](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site): Visit site와 push 후 최대 10분 반영 안내.
- [GCM 인증 저장](https://docs.github.com/en/get-started/git-basics/caching-your-github-credentials-in-git): 브라우저 인증과 저장된 자격 증명에 따른 동작.
- [빈 저장소 생성](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-new-repository): 기존 로컬 기록을 올릴 때 README 등의 자동 초기화를 선택하지 않음.
- [브랜치 목록](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-branches-in-your-repository/viewing-branches-in-your-repository): dropdown의 View all branches.
- [commit 이메일](https://docs.github.com/en/account-and-profile/how-tos/email-preferences/setting-your-commit-email-address): 저장소별 설정과 GitHub noreply 사용.

## 인계와 남은 제한

3주에는 main에 합친 `index.html`·`about.html`·`styles.css`·`app.js`를 이어 쓴다. CSS·JS 파일은 보존하고 HTML 연결만 해제한다. 새 브랜치 학습을 반복하지 않으며 3주부터 파일 준비는 사전, 업로드는 수업 뒤 정리다. 이 내용과 2주 캡처 네 장 예외를 총괄에 전달했다.

교재 테마만 적용한 EN 14장 캡처에서 표 본문 글자가 검정이고 행 배경이 어두운 대비 문제를 발견해 총괄에 전달했다. 공통 테마 범위이므로 이 담당에서 수정하지 않았다. 전체 사이트 렌더의 추가 CSS로 해결되는지도 통합 검사에서 확인해야 한다.

실제 학생의 30분 수행 시간, GitHub 계정·GCM 인증, 실제 push·merge·공개 Pages 배포 지연은 실측하지 않았다. 브라우저 검사는 로컬 파일 내용과 로컬 HTTP 서버 기준이다. Git 명령은 원고의 흐름·기대 결과를 대조했으며 직접 commit하거나 push한 것으로 기록하지 않는다. 전체 npm build/check/test와 공개 배포·독립 심사 판정은 총괄 통합 단계에 남아 있다.
