# 웹프로그래밍 공용 교재

## 목차

- [범위](#범위)
- [진입점](#진입점)
- [학교 적용](#학교-적용)
- [운영 주의](#운영-주의)

## 범위

프로그래밍 경험이 거의 없는 학생을 기준으로 한 **입문 웹** 교재다. HTML·CSS·JavaScript와 Git·GitHub Pages를 다루며,
저장소 하나(`my-web`)에 15주 동안 페이지를 쌓는다. 공개 주소는 `https://<아이디>.github.io/my-web/`이다.

1주차는 연습용 폴더 `week01`에서 URL·요청과 응답·DevTools와 로컬 Git(`init → add → commit`)을 익히고,
2주차에 `my-web`을 GitHub에 올려(push) Pages로 공개 주소를 만들고 브랜치와 merge까지 한다.
3~7주차에는 그 저장소를 세 페이지 자기소개 사이트로 키운다 — 시맨틱 HTML과 form(3주), CSS와 반응형(4주),
변수·`if`·함수(5주), DOM·이벤트(6주), 폼 입력 읽기와 결과 표시(7주).
10~13주차에는 방명록을 배열 목록 그리기(10주) → 객체와 `localStorage`(11주) → `fetch`로 JSON 카드(12주) →
보안·접근성·릴리스 점검(13주)으로 넓힌다.
8주 중간 개인 실기, 9·14주 과제 발표, 15주 기말 개인 실기가 들어 있다.

서버 데이터베이스·로그인(Supabase)과 인증·권한은 정규 15주에 넣지 않는다. 희망하는 경우에만 선택 특강(`specials/`)으로 운영한다.

## 진입점

- 15주 교재 색인: [`weeks/README.md`](weeks/README.md)
- 선택 특강: [`specials/README.md`](specials/README.md)
- 과목별 설치 프로그램: [`ta_setup_guide.md`](ta_setup_guide.md)
- 공통 설치 프로그램: [`../ta_lab_setup_guide.md`](../ta_lab_setup_guide.md)
- 환경 기준표: [`../environment_baseline_template.md`](../environment_baseline_template.md)
- 교재 사이트(HTML 슬라이드): <https://gbox3d.github.io/teaching_repo/webprg/>

각 주차 폴더에는 `README.md`, `slides.md`, `walkthrough.md`, `lab.md`, `examples/`가 있다.
강의 대본과 실습 해답은 강의자가 별도로 관리한다. 파일 세트와 실습 루틴은 [`weeks/README.md`](weeks/README.md#주차-폴더-구성)에 있다.

## 학교 적용

- 학교명·분반·실제 배점·시험·마감·LMS 정보는 학교 폴더에서 관리한다.
- 학교별 표지와 일정은 배포본에서 적용하고 공용 원고에 직접 넣지 않는다.

## 운영 주의

- **확인과 캡처의 표준은 GitHub Pages 공개 URL이다.** 매 실습 끝 5분에 `git push` → 공개 주소 새로고침 → 캡처 순서로 마친다.
  반영은 1~3분 늦으므로, 5분 안에 안 보이면 로컬 화면 캡처와 GitHub **Commits** 탭 캡처를 같은 점수로 인정한다.
- 3~10주차는 작업 중 미리 보기를 `file://`(파일 더블클릭)로 해도 된다. 이 구간에는 미리 보기에 서버가 필요한 기능이 없다.
- **11주차부터 확인·캡처는 공개 URL에서만 한다.** `localStorage`는 `file://`과 공개 주소가 서로 다른 저장소를 쓰므로
  "새로고침해도 남는다"가 로컬 화면으로는 재현되지 않는다.
- 12주차 `fetch`도 공개 URL이 표준이다. 로컬 미리보기가 필요하면 VS Code 확장 **Live Server**(상태줄 **Go Live** → `http://127.0.0.1:5500/`)를 쓰고,
  설치가 막힌 실습실에서는 `python3 -m http.server 8000`으로 대체한다. 둘 다 없어도 push → Pages 확인만으로 수업과 시험이 그대로 성립한다.
- Git 인증은 **HTTPS + 브라우저 로그인**이 기본이다. 비밀번호나 토큰을 명령에 적지 않는다.
  공용 PC는 실습 끝에 자격 증명 관리자에서 `git:https://github.com`을 지운다(절차는 [`ta_setup_guide.md`](ta_setup_guide.md#공용-pc-운영)).
- 학생에게 Node.js·npm·터미널 서버를 요구하지 않는다. Node.js는 조교의 교재 사이트 빌드 전용이다.
- 예제는 파일 하나 60줄 이하, 클래식 `<script src="…" defer>`만 쓴다. CDN·라이브러리·`type="module"`은 쓰지 않는다.
- 공개 저장소·캡처·예제에 실명·학번·전화번호·실제 이메일을 넣지 않는다. 예시는 `student01`·`student01@example.com`이다.
- GitHub 화면과 무료 정책은 개강 전에 공식 문서와 새 실습 계정으로 다시 확인한다.
