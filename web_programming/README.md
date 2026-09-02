# 웹프로그래밍 공용 교재

## 목차

- [범위](#범위)
- [진입점](#진입점)
- [학교 적용](#학교-적용)
- [운영 주의](#운영-주의)

## 범위

Git·GitHub, HTML·CSS·JavaScript, GitHub Pages와 Supabase를 연결해 정적 웹에서
인증·데이터·권한이 있는 프로젝트까지 확장하는 공용 교재다.

## 진입점

- 15주 교재 색인: [`weeks/README.md`](weeks/README.md)
- 선택 특강: [`specials/README.md`](specials/README.md)
- 과목별 설치 프로그램: [`ta_setup_guide.md`](ta_setup_guide.md)
- 공통 설치 프로그램: [`../ta_lab_setup_guide.md`](../ta_lab_setup_guide.md)
- 환경 기준표: [`../environment_baseline_template.md`](../environment_baseline_template.md)

## 학교 적용

- 학교명·분반·실제 배점·시험·마감·LMS 정보는 학교 폴더에서 관리한다.
- 학교별 표지와 일정은 배포본에서 적용하고 공용 원고에 직접 넣지 않는다.

## 운영 주의

- Node.js는 LTS 계열을 사용하되 정확한 major/minor는 개강 전 환경 기준표에서 고정한다.
- ES Module 예제는 `file://`로 열지 않고 교재가 제공하는 로컬 HTTP 서버로 실행한다.
- Supabase 브라우저 예제에는 publishable key만 사용하고 secret, service-role, DB 비밀번호를 넣지 않는다.
- GitHub·Supabase·Deno의 화면과 무료 정책은 개강 전에 공식 문서와 새 실습 계정으로 다시 확인한다.
