# 9주차 전수 조사와 수정 기록

담당: week09_owner. 기준일: 2026-11-18. [C01](proposal-C01.md)과 [구현 지시](implementation.md)를 적용했다. 이 문서는 구현·검증 기록이며 독립 평가 점수가 아니다.

## 조사 범위

최종 주차 파일 36개를 조사했다. Markdown 21개, HTML 4개, JavaScript 2개, CSS 2개, PNG 4개, SVG 3개다. 기존 profile.jpg는 실제 인계 파일인 profile.png로 교체하여 제거했다.

| 묶음 | 조사 내용 |
|---|---|
| 주차 문서 7개 | README·lab·walkthrough·project_brief·rubric·한영 slides 전체 |
| 예제 안내와 Markdown 11개 | examples/README, ex01 제목부터 ex11 Mermaid까지 모든 정상·오류 비교 |
| 도표·그림 | day1 profile.png와 SVG 2개, 완성본 profile.png·site-map.svg·캡처 2장 |
| 완성 웹 | index·about·guestbook·guestbook.before, app.js·guestbook.js, styles.css·shared/examples.css |
| README 자료 | 완성 README와 새 README.start.md |

기존 파일을 먼저 읽고 7주 담당자의 최종 인계를 받아 웹 파일 9개를 그대로 복사했다. 이전 작업에서 이미 적용한 W3.CSS 변경과 이번 C01 시간·자료 보완이 함께 작업 트리에 있다. 공통 파일과 다른 주차는 수정하지 않았다.

## 차시와 평가 수정

1차시는 강의·시연 60분과 실습 30분으로 맞췄다. 강의는 준비 5, 제목·목록·링크 15, 그림·코드·표 20, 제공 SVG 사용 10, 발표 순서 5, 실습 안내 5분이다. 필수 실습은 제공 README.start.md를 채우는 활동이다. 제목·주소·표 10분, 캡처·코드 인용·기능 두 줄·배운 것 세 줄 10분, 제공 SVG 글자·미리 보기 5분, 확인 5분으로 맞췄다.

11개 비교 예제를 모두 수정하던 요구를 없앴다. ex01·02·03·05·06·07은 강의와 작성 참고, ex10은 제공 SVG 글자 변경이다. 강조·인용·SVG 좌표·Mermaid는 선택이며 정규 필수 평가에서 제외한다. 파일·저장소는 수업 전에 준비하고 공개 업로드는 수업 뒤에 한다.

2차시는 안내 5분·발표 75분·피드백 10분이다. 30명까지 시연 2분+전환 30초로 계산했다. 구술은 시연 마지막 10초, 기존 20초 유예는 전환 시간 안에 포함한다. 31명 이상은 전원 사전 2분 영상, 현장 표본 5명 시연 12분 30초, 전원 개인 설명 최대 min(60, 3600/N)초씩으로 75분 안에 배정한다. 40명 예시는 12분 30초+40분+질문 22분 30초다. 사전 영상도 같은 발표 5점, README 5점으로 평가한다.

## 파일과 기술 설명 수정

- 7주 최종 HTML·JS·CSS·프로필 등 9개를 바이트 단위로 대조했다. 9주에서는 웹 동작을 추가하지 않는다. guestbook.before.html도 비교본으로 인계하되 발표 메뉴는 세 페이지만 사용한다.
- 방명록은 고정 W3.CSS 4.1.0 CDN과 제공 shared/examples.css를 사용한다. 홈·소개는 기존 직접 작성 CSS를 유지한다. 긴 ASCII 입력 줄바꿈과 다크 모드 대비는 6·7주 수정본에서 이어받았다.
- 누락된 profile.png를 복구하고 쓰지 않는 profile.jpg를 제거했다. 홈 버튼 클릭과 방명록 두 글을 실제 실행한 뒤 [홈 캡처](../../weeks/week09_readme_presentation/examples/day2/web-week09/screenshots/home.png)·[방명록 캡처](../../weeks/week09_readme_presentation/examples/day2/web-week09/screenshots/guestbook.png)를 갱신했다.
- ex05의 잘못된 profil.png는 코드 블록의 선택 실험으로 옮겼다. 배포 문서에 실제 깨진 그림을 남기지 않으며 학생은 임시로 코드 밖에 붙여 넣어 오류를 재현한다.
- 현재 VS Code의 기본 Mermaid 지원을 [공식 문서](https://code.visualstudio.com/docs/languages/markdown#_mermaid-diagram-rendering)와 대조해 한영 슬라이드·실습 안내·예제를 고쳤다. [GitHub 공식 안내](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-diagrams)도 mermaid 언어 이름의 코드 블록을 설명한다.
- 공개 SVG 한 줄을 GitHub Markdown 렌더 API에 보내 200과 `<p></p>`를 받았다. 인라인 SVG가 제거됨을 확인했다. 실제 학생 파일이나 인증 정보를 전송하지 않았고 저장소를 변경하지 않았다.
- 13주 README 최종판 요구를 제거했다. 11주는 폼 한 객체 저장이 필수이며 전체 저장 방명록은 제공 시연본이라고 연결했다.

## 실행 검증

검증 환경은 Node.js 24.18.0, 설치된 Playwright의 Chrome headless, localhost 정적 서버다. 자동 입력은 실제 HTML·JS를 사용했다. 시험 답안을 추적 파일에 채우는 작업은 없다.

| 검증 | 결과 |
|---|---|
| HTML 4개 × 폭 375/1280 | 8개 화면에서 초기 오류·가로 넘침 없음. 이미지 정상, W3.CSS 로드 확인 |
| 홈 기능 | 인사 클릭·횟수 1, Enter로 다크 모드·횟수 2, 새로고침 초기화 확인. 다크 제목 rgb(167,197,255), 배경 rgb(34,34,34) |
| 방명록 전후 2개 | 빈값·공백 안내, 무효 이메일 native validation, 유효 이메일, 두 글 순서, 입력 초기화·라벨 포커스, 태그 문자열의 textContent 표시 확인 |
| 긴 입력과 저장 범위 | ASCII 120자도 가로 넘침 없음. 새로고침하면 목록 0개. 이메일은 목록에 포함되지 않음 |
| 메뉴·주소 | 세 페이지의 nav 9회 직접 클릭, 뒤로·앞으로·직접 진입·새로고침 확인. file URL에서도 홈 버튼과 방명록 입력 동작 |
| Markdown 11개 | markdown-it 렌더 결과를 Chrome에서 확인. 제목·목록·링크·강조·그림·코드·표·인용·SVG를 검사. Mermaid는 코드 블록과 연결 원문을 대조 |
| 시작 틀 | TODO를 메모리에서 채워 5개 항목·표·코드·그림 3개가 정상 렌더됨을 확인. 제공 틀은 TODO 상태 유지 |
| 정적 검사 | 로컬 파일 참조 215건 누락 0, JS 2개 구문 검사 통과, README 전문·SVG 전문·app.js 인용 3개 일치 |
| 인계 | 7주 전체 웹 파일 9개 동일. 10주 담당자에게 동기화 완료 통보 |
| 문서·덱 | 한국어 UI·문서 문체 검사 0건. Marp 렌더 한영 각각 기존 20장 유지. 시간·선택 범위·다음 주 연결을 함께 수정 |

## 남은 검증과 제한

실제 초보 학생이 30분 안에 완성하는지는 실측하지 않았다. GitHub Pages 업로드와 실제 VS Code 앱 화면·GitHub의 Mermaid 도표 렌더는 이번 실행에서 확인하지 않았다. Markdown 비교는 로컬 markdown-it/Chrome 검사이며 GitHub의 sanitization·확장 처리와 같은 것으로 간주하지 않는다. 최신 Mermaid 지원은 공식 문서로 확인했다.

전체 교재 빌드, 사이트 링크와 렌더된 덱 배치, 독립 심사 3명의 통과 여부는 총괄 통합 단계에서 확인한다. 커밋·푸시는 하지 않았다.
