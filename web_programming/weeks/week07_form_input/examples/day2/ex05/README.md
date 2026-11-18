# ex05 W3.CSS 방명록

`index.html`을 열고 이름에 `student01`, 메시지에 두 줄짜리 글을 입력한 뒤 **남기기**를 누른다. 글 왼쪽의 원에는 이름의 첫 글자가, 오른쪽에는 작성자와 작성 시각이 보인다. 본문에는 입력한 줄바꿈이 남는다. 두 번째 글을 남기면 새 글이 맨 위에 나타난다. ex04 및 완성본도 같은 JavaScript를 쓴다.

| 클래스 | 적용 대상 |
| --- | --- |
| `w3-container w3-card w3-white` | 입력 카드와 목록 카드 |
| `w3-bar` | 메뉴 영역 |
| `w3-bar-item w3-button w3-mobile` | 반응형 메뉴 항목 |
| `w3-input w3-border` | 이름·이메일·메시지 입력 |
| `w3-button w3-teal` | 남기기 버튼 |
| `w3-text-red` | 빈칸 안내 |
| `w3-ul example-output feed-list` | 글 사이의 구분선과 여백, 원형 아바타, 긴 입력의 줄바꿈 |
| `w3-content w3-padding` | 본문 최대 너비와 여백 |
| `guestbook-page` | 방명록 본문 폭, 이름과 이메일 입력 칸의 배치 |

`class`는 모양을 정하고 `id`는 JavaScript가 요소를 찾을 때 사용한다. `guestbook-form`, `name`, `message`, `notice`, `list`의 `id`와 제공된 JavaScript를 유지한다.

빈칸 안내, 입력 중 안내 제거, 폼 초기화, 이름 칸 초점을 확인한다. 375px과 1280px에서 메뉴·입력 칸·피드를 비교한다. 공백 없이 긴 문자열을 본문에 붙여 넣으면 글 영역 안에서 줄이 바뀐다. 이메일은 피드에 표시하지 않으며 새로고침하면 빈 목록으로 돌아간다.

`createPost`는 게시글 한 건을 `li > article`로 만들고, `list.prepend(li)`는 그 글을 목록 맨 앞에 넣는다. 작성 시각은 `time` 요소의 `datetime`에 ISO 형식으로 기록하고 화면에는 한국어로 표시한다. 이름과 본문은 `textContent`로 넣는다.

이메일은 비워 두거나 `student01@example.com`을 입력한다. `abc`처럼 잘못된 이메일 형식은 브라우저가 submit 이벤트 전에 검사하여 제출을 막는다. ex04와 같은 동작이다.

- CDN: `https://cdnjs.cloudflare.com/ajax/libs/w3-css/4.1.0/w3.min.css`
- 추가 CSS는 `shared/examples.css`다. 공용 스타일 아래에 방명록의 입력 폼과 피드 스타일이 있다. 폴더를 복사할 때 `shared/`도 함께 가져온다.

CDN을 읽으려면 인터넷 연결이 필요하다. 라이브러리 로컬 사본은 사용하지 않는다. 메뉴의 홈·내 정보 링크를 쓰려면 `examples/day2` 내부의 상대 위치를 유지한다.

완성 사이트는 `../web-week07/`에 있다. 이 폴더 전체를 복사하면 홈, 내 정보, 방명록을 함께 정적 배포할 수 있다.
