# 15주차 조사·검증

## 범위와 수정

기존 추적 파일 59개를 목록·텍스트·참조 관계로 조사했다. 개편 후 62개(문서 17·HTML 11·JS 10·CSS 12·PNG 3·HTTP 3·환경 예시 3·gitignore 3)를 확인했다. 1일차는 강의·시연 60분과 폼 저장 10·REST 12·확인 8분의 학생 실습 30분이다. 2일차는 안내 30분과 읽기 3·구현 40·재조회/주소 12·제출 5분의 시험 60분이다. 기존 A 3/B 3/C 4/D 2/E 3 + URL 3/구술 2 = 20점 구조를 유지했다.

- w09: 7~9주 최종 웹을 이어 받아 W3.CSS 방명록·홈 다크 모드·프로필·보조CSS를 동기화했다. 학생 README 시작 틀을 추가하고 실제 화면 캡처 두 장을 교체했다.
- w10: 목록 그리기·이벤트·빈값 검사·개수는 제공하고 push와 splice 두 곳만 학생 구현으로 줄였다.
- w11: 전체 객체배열 목록을 폼 한 객체의 JSON 저장·복원·키 하나 삭제로 교체했다. 손상 JSON의 실패 안내·복구 틀은 제공한다.
- w12: GET 함수 한 개만 구현한다. 화면·실패·재시도·설정 변경 처리는 제공한다.
- w13: POST 함수 한 개만 구현한다. 입력 검사·중복 방지·생성 ID 재조회·실패 시 입력 보존은 제공한다.
- w14: 공개 연습은 PATCH 함수 한 개를 구현하고 DELETE·응답 검사·같은 ID 재조회·키 삭제는 제공한다. 시험 DELETE 변형도 한 요청만 빈칸으로 배부하도록 명시했다.
- REST 세 폴더: canonical api-settings.js와 W3.CSS CDN 4.1.0·shared/examples.css, .env.example·.gitignore·requests.http를 제공한다. 동작은 app.js 한 파일로 합쳐 옛 view.js·config.example.js를 제거했다. 초기 GET은 선언·설정등록 뒤에 실행한다.
- w12_fetch_cards·w13_text_safe·w14_readme_images의 옛 주소는 짧은 변경 안내 HTML·README로 보존하고 사용하지 않는 구예제 소스·그림을 제거했다.

실제 편집키·DB 비밀번호·클라우드 비밀값은 파일에 넣지 않았다. .env 세 경로가 Git에서 제외됨을 확인했다. 공개 키와 태그는 실행 중 입력하며 새로고침 뒤 재입력한다.

## 실제 실행

[브라우저·요청 실행 기록](evidence/week15-browser.json). Chrome headless와 별도 임시 Node API를 사용했다. 시험 해답은 브라우저 응답에만 주입했고 저장소의 TODO는 남겼다. 시험 데이터와 키는 임시 폴더에 생성하고 종료 후 제거했다.

| 대상 | 실행 확인 |
|---|---|
| 시작 HTML 11개 | 375/1280px 총 22회, 설정 패널 펼침 포함, 가로 넘침·처리되지 않은 JS 예외 없음 |
| 임시 완성본 5개 | 375/1280px 총 10회, TODO만 채워 전체 동작 확인 |
| w09 | 인사·다크·카운터, W3 폼 두 글·긴 ASCII 120자·새로고침 초기화, 실제 캡처 2장 교체·육안 확인 |
| w10 | 세 글 등록·가운데 삭제·나머지 삭제·빈 목록·공백 검사·태그 문자·새로고침 초기화 |
| w11 | 값 없음·한 객체 JSON 저장·새로고침 후 불러오기·손상 JSON 안내·자기 키 삭제·other-key 보존 |
| GET | 실제 목록·Offline 실패·재시도 복구·빈 태그·설정 새로고침 초기화 |
| POST | 공백 차단·201 생성·같은 ID 확인·새로고침 유지·태그 문자·실패 입력 보존 |
| PATCH/DELETE | 틀린 키로 불변·정상 키 수정·키 입력 즉시 삭제·204 재조회·가운데 삭제와 이웃 글 유지 |
| .http 3개 | 원문 13요청을 파싱하여 about/help/GET/PATCH 200·POST 201·DELETE 204 확인 |

JS 10개 구문, 문서 17개의 로컬 링크 79개, 한국어 UI·문서 검사를 통과했다. .env는 브라우저 설정과 구분하여 설명했다. 코드 전문을 문서에 중복하지 않고 실제 시작 파일을 링크했다. 한영 슬라이드는 각 13장(구분선 14개)으로 동일하며 시간·필수 범위·배점을 함께 수정했다.

실제 학생의 8분 문항 수행 시간·30분 실습 시간, Pages 게시, 공용 Supabase 쓰기, VS Code 확장 UI 직접 조작은 미검증이다. 실제 시험은 강의자가 사전 배부·서버 초기 데이터·감독 인원을 준비하며 학생 집단 시간은 추후 관찰한다. 전체 빌드·배포 덱 레이아웃·교차 주차 링크는 총괄 통합 검증에 남긴다. 자체 통과 점수는 붙이지 않는다.

## 최종 파일 목록

- README.md
- examples/README.md
- examples/w09_readme_links/README.md
- examples/w09_readme_links/README.start.md
- examples/w09_readme_links/about.html
- examples/w09_readme_links/app.js
- examples/w09_readme_links/guestbook.html
- examples/w09_readme_links/guestbook.js
- examples/w09_readme_links/images/profile.png
- examples/w09_readme_links/index.html
- examples/w09_readme_links/screenshots/guestbook.png
- examples/w09_readme_links/screenshots/home.png
- examples/w09_readme_links/shared/examples.css
- examples/w09_readme_links/styles.css
- examples/w10_list_delete/README.md
- examples/w10_list_delete/app.js
- examples/w10_list_delete/index.html
- examples/w10_list_delete/shared/examples.css
- examples/w10_list_delete/styles.css
- examples/w11_local_storage/README.md
- examples/w11_local_storage/app.js
- examples/w11_local_storage/index.html
- examples/w11_local_storage/shared/examples.css
- examples/w11_local_storage/styles.css
- examples/w12_fetch_cards/README.md
- examples/w12_fetch_cards/index.html
- examples/w12_rest_get/.env.example
- examples/w12_rest_get/.gitignore
- examples/w12_rest_get/README.md
- examples/w12_rest_get/api-settings.js
- examples/w12_rest_get/app.js
- examples/w12_rest_get/index.html
- examples/w12_rest_get/requests.http
- examples/w12_rest_get/shared/examples.css
- examples/w12_rest_get/styles.css
- examples/w13_rest_post/.env.example
- examples/w13_rest_post/.gitignore
- examples/w13_rest_post/README.md
- examples/w13_rest_post/api-settings.js
- examples/w13_rest_post/app.js
- examples/w13_rest_post/index.html
- examples/w13_rest_post/requests.http
- examples/w13_rest_post/shared/examples.css
- examples/w13_rest_post/styles.css
- examples/w13_text_safe/README.md
- examples/w13_text_safe/index.html
- examples/w14_readme_images/README.md
- examples/w14_readme_images/index.html
- examples/w14_rest_edit/.env.example
- examples/w14_rest_edit/.gitignore
- examples/w14_rest_edit/README.md
- examples/w14_rest_edit/api-settings.js
- examples/w14_rest_edit/app.js
- examples/w14_rest_edit/index.html
- examples/w14_rest_edit/requests.http
- examples/w14_rest_edit/shared/examples.css
- examples/w14_rest_edit/styles.css
- lab.md
- rubric.md
- slides.md
- slides_en.md
- walkthrough.md
