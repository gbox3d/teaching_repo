# 3주차 — 시맨틱 HTML과 form

실습 페이지: https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week03_semantic_html

2주차에 공개한 `my-web`의 홈과 소개를 바꾸고 정적 방명록을 추가한다. 제공된 HTML에서 제목·문단·그림 설명·목록을 고친 뒤, 표와 입력 칸을 확인한다. HTML 전체를 빈 파일부터 작성하는 일은 강의자 시연이다.

이번 주에는 HTML만 수정한다. `styles.css`와 `app.js`는 보존하며 홈의 연결을 해제한다. 1차시 `about.html`에는 지난주 CSS가 남아 있고, 2차시 끝에는 세 페이지 모두 CSS·JavaScript를 연결하지 않는다. CSS는 4주차, JavaScript 문법은 5주차, 방명록 글 추가는 7주차에 다룬다. W3.CSS도 7주차에 도입한다.

## 학습 목표

1. 제공 문서의 `header`·`nav`·`main`·`footer`와 제목 단계를 구별한다.
2. 제목·문단·`strong`·취미 목록을 자기 내용으로 바꾸고 `img`의 경로와 `alt`를 확인한다.
3. 상대 경로 링크로 홈·내 정보·방명록을 오간다.
4. 제공된 2열 4행 표의 내용 두 행을 고친다.
5. 이름·이메일·메시지의 `label for`와 입력 `id`를 연결하고 브라우저의 기본 이메일 검사를 확인한다.

## 차시별 운영

일반 차시는 강의·시연 60분과 학생 실습 30분이다. 파일 배부·저장소 준비는 수업 전에 마치고, 공개 업로드는 수업 뒤에 한다. Git 새 명령은 배우지 않으며 `main`에서 작업한다.

| 차시 | 강의·시연 60분 | 학생 실습 30분 | 확인 결과 |
|---|---|---|---|
| 1차시 | 준비 5, 시맨틱 구조 15, 제목·문단 10, 상대 링크·이미지 15, 목록 10, 안내 5 | 제공 뼈대 열기 5, 제목·문단·alt·취미 15, 링크 2개 점검 5, 확인 5 | 홈의 구조와 이미지 |
| 2차시 | 준비 5, table 10, form·label 20, input·textarea·submit 15, 왕복 링크 5, 안내 5 | 표 2행 변경 5, 이름·이메일·메시지 label/입력 연결 15, 3페이지 이동 5, 캡처 5 | 정적 방명록 폼 |

| 구분 | 범위 |
|---|---|
| 필수 | 위 표의 수정과 로컬 화면 확인·캡처 |
| 제공 | `examples/day1`·`day2`의 HTML과 그림, 2주차에서 보존한 CSS·JS |
| 강의자 시연 | 빈 문서에 시맨틱 뼈대 작성, 표·폼 조립, 잘못된 상대 경로와 label 비교, 이메일 기본 검사 |
| 선택 | 취미 목록의 `ul`/`ol` 비교, 표 한 행 추가. 필수 결과를 확인한 뒤 진행 |

## 사전 준비

- 2주차 `my-web`을 준비한다. 같은 PC에서는 기존 폴더를 열어 `git pull`, 다른 PC에서는 2주차에 배운 `git clone`을 수업 전에 한다. 2주차 merge가 끝난 `main`인지 확인한다.
- 강의자가 `examples/day1/`·`day2/` 전체를 미리 배부한다. 수업 중 파일별 Raw 다운로드를 하지 않는다. 각 폴더는 해당 차시의 완성 참고본이다.
- 1차시에는 배부한 `day1/index.html`과 `images/`를 `my-web`에 준비하고, `about.html`·CSS·JS는 2주차 파일을 보존한다. 제공 홈 뼈대에서 자기 내용만 수정한다.
- 2차시 전에 `day2/about.html`·`guestbook.html`을 준비하고, 내 홈의 메뉴에 방명록 링크를 추가한다. 자신의 제목·문단·그림 설명·취미를 완성 참고본으로 덮어쓰지 않는다.
- VS Code와 브라우저로 파일을 연다. 로컬 파일 주소 또는 강의자가 제공한 로컬 서버 주소로 확인한다.
- 공개 파일에는 수업용 별칭과 `student01@example.com` 같은 가상 주소를 쓴다. 실명·학번·전화번호·실제 이메일은 넣지 않는다.

## HTML 범위

| 태그·속성 | 관찰할 것 |
|---|---|
| `header`·`nav`·`main`·`footer` | 소개와 메뉴·본문·마무리의 의미. 이 예제의 `nav`는 `header` 안에 있다 |
| `h1`·`h2`·`h3` | 제목 단계. 예제는 페이지 제목 하나와 그 아래 묶음으로 구성한다. `h3`는 강의 비교 코드에서 본다 |
| `p`·`strong` | 문단과 문단 안의 중요한 말 |
| `a href="about.html"` | 같은 폴더의 파일로 이동하는 상대 경로 |
| `img src="images/profile.png" alt="…"` | 그림 경로와 그림의 내용을 설명하는 대체 텍스트 |
| `width="160"` | 제공 그림의 너비. 4주차에 CSS로 옮긴다 |
| `ul`·`ol`·`li` | 순서 없는 목록·순서 있는 목록·목록 항목 |
| `table`·`tr`·`th`·`td` | 표·행·제목 칸·내용 칸 |
| `form`·`button type="submit"` | 입력 묶음과 브라우저 기본 제출 |
| `label for="name"`·`input id="name"` | 일치하는 이름표를 누르면 입력 칸에 포커스가 간다 |
| `input type="text"`·`input type="email"`·`textarea rows="4"` | 한 줄·이메일·여러 줄 입력 |

`section`·`article`·`aria-*`·`required` 추가, CSS 작성, JavaScript 이벤트 처리는 이번 주 필수가 아니다.

## 정적 폼의 동작

이 폼에는 JavaScript, 서버 저장, `required`가 없다. 이름·메시지는 비어 있어도 되고, 이메일도 빈 값은 허용된다. 다만 이메일에 `abc`처럼 형식이 맞지 않는 값을 넣고 **남기기**를 누르면 브라우저가 제출을 막는다. `type="email"`이 제공하는 기본 검사이며 JavaScript 코드가 아니다.

이메일이 비어 있거나 `student01@example.com`처럼 형식이 맞으면 기본 GET 제출로 현재 페이지를 다시 연다. 주소 끝에 빈 쿼리 `?`가 붙을 수 있고 입력값이 초기화된다. `action`·`method`를 생략하면 현재 주소로 GET 제출하며, 입력에 `name` 속성이 없어 값이 쿼리로 실리지 않는다. 이 동작은 강의자가 설명하고 학생은 관찰한다. 글 추가와 저장은 일어나지 않는다.

`name`·`message` ID는 이후 방명록에서 이어 쓴다. `email`은 이번 주 입력 종류를 비교하는 예제이며 공용 API의 필드로 이어지지 않는다.

## 실습 결과와 제출

- [ ] 홈에서 제목·소개 문단·그림(`alt`)·취미 목록을 확인한다.
- [ ] 내 정보의 2열 4행 표에서 내용 두 행을 바꾼다.
- [ ] 세 입력 이름표를 누르면 각각의 칸에 포커스가 간다.
- [ ] 잘못된 이메일은 제출이 막히고, 정상 형식 또는 빈 이메일의 제출은 글을 저장하지 않는다.
- [ ] 세 페이지에서 홈·내 정보·방명록 링크가 열린다.
- [ ] 로컬 방명록의 메뉴·입력 칸·남기기 버튼과 주소창이 보이는 캡처 한 장을 제출한다.

공개 업로드는 수업 뒤 10분 이내의 반복 정리다. 배운 `git add`·`commit`·`push`로 `my-web`을 갱신하고 `https://<아이디>.github.io/my-web/guestbook.html`을 확인한다. 공개 주소 반영이나 계정 문제가 있어도 수업 중 로컬 캡처를 인정하며 다음 차시 첫 5분에 다시 확인한다.

## 수업 자료

- [슬라이드](slides.md) · [영문 슬라이드](slides_en.md)
- 교재 덱: https://gbox3d.github.io/teaching_repo/webprg/decks/week03_semantic_html/index.html
- [실습지](lab.md) · [따라하기와 전체 코드](walkthrough.md) · [파일별 역할](examples/README.md)
- [1차시 홈](examples/day1/index.html) · [그림](examples/day1/images/profile.png)
- [2차시 홈](examples/day2/index.html) · [내 정보](examples/day2/about.html) · [방명록](examples/day2/guestbook.html)

## 4주차 인계

이번 주 공개 주소는 `my-web`이다. 다음 주에는 이 완성본의 세 HTML·`images/`·보존한 CSS·JS를 새 `web-week04` 폴더로 복사한다. `.git`은 복사하지 않는다. 새 저장소 준비와 파일 배부는 4주차 수업 전에 한다.

4주차에는 제공된 CSS 시작 틀을 수정하여 세 HTML에 연결한다. 결과의 공개 주소도 `https://<아이디>.github.io/web-week04/`로 바뀐다. 이번 주의 HTML 구조를 CSS 선택 대상으로 사용하며, 이번 주에 반응형 규칙을 작성할 필요는 없다.

## 공식 참고 자료

- [HTML 문서 구조 — MDN](https://developer.mozilla.org/ko/docs/Learn_web_development/Core/Structuring_content/Structuring_documents)
- [HTML 이미지 — MDN](https://developer.mozilla.org/ko/docs/Learn_web_development/Core/Structuring_content/HTML_images)
- [HTML 표 — MDN](https://developer.mozilla.org/ko/docs/Learn_web_development/Core/Structuring_content/HTML_table_basics)
- [첫 HTML 폼 — MDN](https://developer.mozilla.org/ko/docs/Learn_web_development/Extensions/Forms/Your_first_form)
