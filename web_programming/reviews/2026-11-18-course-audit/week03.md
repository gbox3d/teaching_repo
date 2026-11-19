# 3주차 구현 및 실행 검토

C01의 3-1·3-2를 반영했다. 수정 범위는 `weeks/week03_semantic_html/`와 이 보고서다. 다른 주차·공통 문서·공통 빌드 파일은 수정하지 않았고 커밋·푸시는 하지 않았다.

## 전수 조사 범위

기존 17개 파일을 모두 읽거나 이미지로 확인했다. 두 차시의 실행 HTML 5개, 보존 CSS 2개·JS 2개, 그림 2개와 원고 6개다.

| 파일 (`weeks/week03_semantic_html/` 기준) | 조사·수정 |
|---|---|
| `README.md` | 60+30 시간표, 필수·제공·시연·선택, 준비·캡처·업로드 분리, 정적 폼 설명, 4주차 저장소 인계 수정 |
| `lab.md` | 차시별 30분 필수 수정량과 결과, label 세 쌍·이메일 검사, 로컬 캡처 안내. 기존 외부 링크의 `제출 — 캡처 한 장` 앵커 보존 |
| `walkthrough.md` | 전체 재입력을 시연·복습으로 표시, 사전 준비·학생 수정 순서 구분, 전체 코드와 실제 파일 일치 |
| `slides.md` | 강의 시간 구간·필수 수정·제출·인계를 수정하고 기존 16장 유지 |
| `slides_en.md` | 한글과 같은 시간·범위·준비·폼 동작·인계로 수정하고 기존 16장 유지 |
| `examples/README.md` | 모든 파일의 역할, 차시별 실행, 제공/필수/선택, 기본 검사·미저장 설명 |
| `examples/day1/index.html` | 구조·제목·문단·그림·취미·왕복 링크 확인. 자기소개 콘텐츠이므로 유지 |
| `examples/day1/about.html` | 2주차 소개 보존, CSS 연결과 홈 돌아가기 확인. HTML 유지 |
| `examples/day1/styles.css` | 완료된 2주차 CSS를 그대로 인계. `.card`의 `box-sizing: border-box`, `h1`의 `word-break: keep-all` 포함 |
| `examples/day1/app.js` | 2주차 JS 원문·구문 확인. 이번 주 연결하지 않는 보존 파일로 유지 |
| `examples/day1/images/profile.png` | 400×400 사람 모양 PNG를 직접 열어 확인. 정상 로드·alt 확인, 유지 |
| `examples/day2/index.html` | 세 메뉴·자기소개·그림·목록 확인. HTML 유지 |
| `examples/day2/about.html` | 2열 4행 표·세 메뉴·가상 정보 확인. HTML 유지 |
| `examples/day2/guestbook.html` | 세 입력·label·submit 유지. 긴 쓰는 순서와 후속 수업 설명을 문서로 옮기고 짧은 미저장 상태만 화면에 표시 |
| `examples/day2/styles.css` | day1과 같은 2주차 완료 CSS로 보존. HTML 연결 없음 |
| `examples/day2/app.js` | day1과 같은 보존 파일. HTML 연결 없음 |
| `examples/day2/images/profile.png` | day1과 같은 바이트의 PNG, 홈에서 정상 로드 |

## 차시별 반영

| 차시 | 강의·시연 60분 | 실습 30분 |
|---|---|---|
| 3-1 | 준비 5, 구조 15, 제목·문단 10, 링크·이미지 15, 목록 10, 안내 5 | 제공 뼈대 5, 제목·문단·alt·취미 15, 링크 2개 5, 확인 5 |
| 3-2 | 준비 5, table 10, form·label 20, 입력·submit 15, 왕복 링크 5, 안내 5 | 표 2행 5, label/입력 3쌍 15, 3페이지 이동 5, 캡처 5 |

제공 완성본의 세 `label for` 값을 잠시 비웠다가 다시 연결하여 포커스 차이를 확인하는 실습으로 만들었다. 전체 문서·표·폼의 빈 파일부터 조립은 시연·복습이다. `ul`/`ol` 비교와 표 추가는 선택이다. Git은 `main`에서 배운 업로드만 반복하며 3주차의 `switch -c guestbook`·merge 신규 학습을 제거했다.

파일 배부·저장소 준비는 수업 전, 첫 5분은 준비 확인, 공개 업로드는 수업 뒤다. 수업 안에는 로컬 캡처 한 장으로 완료한다. 다음 주에는 `my-web` 결과를 `.git` 없이 새 `web-week04`에 복사하며 공개 주소도 바뀐다고 명시했다. CSS 학습은 4주차, JS 문법은 5주차, W3.CSS와 방명록 글 추가는 7주차다.

## 실제 실행 결과

2026-11-18, 설치된 Chrome을 Playwright headless로 실행했다. HTTP 기준 경로는 `http://localhost:8111/weeks/week03_semantic_html/examples/`다. 별도 설치·새 의존성·추적 테스트 파일은 추가하지 않았다.

| 실행·검사 | 결과 |
|---|---|
| 수정 전 day1 소개 375px | `scrollWidth=391`, 카드 x=-16·width=407로 넘침 재현 |
| 수정 후 HTML 5개 × 375/1280px | 10개 경우 모두 HTTP 200, `scrollWidth`가 각각 375/1280. 가로 넘침 없음 |
| day1 홈→소개→홈 | 실제 링크 클릭으로 왕복 확인 |
| day2 세 페이지 × 메뉴 세 링크 | 실제 클릭으로 아홉 경로 모두 확인 |
| 그림 두 개 | naturalWidth·naturalHeight 400×400, 로드 완료, 비어 있지 않은 alt |
| 표 | 브라우저 DOM에서 행 4개, 각 행 칸 2개 |
| HTML 구조 | 각 문서 doctype·h1 1개·main 1개, ID 중복·태그 닫힘/중첩 오류 없음. 외부 HTML 적합성 인증은 아님 |
| JS 연결 | HTML 5개 모두 script 0개. day1 소개만 CSS 연결 |
| label 클릭 | 이름→name, 이메일→email, 메시지→message에 실제 포커스 이동 |
| label 연결 제거·복원 | 로컬 파일에서도 빈 for 상태에는 입력 포커스가 없고 name 복원 뒤 name으로 이동 |
| 잘못된 이메일 `abc` | `validity.typeMismatch=true`, form 유효성 false, 이동 차단, 입력 유지 |
| 빈 이메일·정상 가상 이메일 | 기본 GET로 현재 문서 재탐색, URL 끝 `?`, 세 입력 모두 빈 값, 목록 추가 없음 |
| 새로고침 | 메시지 저장·복원 없음 |
| `file:///` 실행 | 같은 이메일 기본 검사와 정상 제출 후 초기화 확인. 로컬 파일 캡처 안내와 일치 |
| 브라우저 오류 | 검사 중 pageerror·requestfailed 0건 |
| 상대 링크 | HTML·Markdown의 로컬 대상/앵커 58개 검사, 끊어진 대상 없음 |
| 원고 전체 코드 | walkthrough의 완전한 HTML·CSS·JS 블록과 실제 소스 9개 일치 |
| 보존 파일 | day1/day2 CSS·JS 동일, 2주차 완료본과 내용 동일. 그림 두 개 바이트 동일 |
| JavaScript 구문 | 보존 app.js 2개 `node --check` 통과. 새 JS 동작 실행으로 간주하지 않음 |
| 한영 슬라이드 | 기존 Marp·teaching 테마로 각각 16장 임시 렌더. Chrome 레이아웃 검사에서 본문/가로 넘침 없음, 최소 글자 크기 29px |
| 문구·공백 | 한국어 문서·화면 문구 검사와 `git diff --check` 통과 |

375px 소개와 방명록 화면을 캡처하여 직접 확인했다. 캡처와 임시 렌더 파일은 저장소 밖 임시 폴더(`week03-*.png`, `week03-slides-*.html`)에 두었으며 교재 배포 자산으로 추가하지 않았다.

## 남은 제한과 통합 전달

- 학생이 30분 안에 수행하는지는 실제 분반에서 실측하지 않았다. C01의 필수 수정량을 기준으로 구성했다.
- 개인 GitHub 업로드·실제 Pages 게시·다른 학생 계정은 실행하지 않았다. 로컬 파일과 localhost의 동작을 검증했다.
- 전체 과목 빌드·전체 테스트는 총괄 단계다. 여기서는 3주 소스·보존 JS 구문·실제 브라우저·한영 덱 임시 렌더를 검증했다.
- 4주차의 정적 방명록도 3주차의 짧은 미저장 안내와 실제 native 검사를 이어 받도록 총괄에게 전달했다. 4주차 파일은 수정하지 않았다.
- 외부 공식 참고 링크의 실시간 접속 확인과 전면 HTML 표준 검증기 실행은 하지 않았다. 구조 검사와 실제 Chrome 해석 결과를 구분한다.
