# 15주차 — 기말 개인 실기

실습 페이지: https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week15_final_exam

## 이번 주 질문

> 2~13주에 배운 것을 처음 보는 starter 위에서 60분 안에 다시 만들고, 공개 주소로 제출할 수 있을까?

14주차에 최종 프로젝트를 발표했다. 이번 주는 개인 실기다.
1일차에는 시험과 **같은 구조의 리허설**을 공개 starter로 끝까지 해 보고, 시험용 저장소와 Pages를 오늘 안에 만들어 둔다.
2일차에는 비공개 문항으로 본시험 60분을 치른다. 문항은 리허설과 같은 형태이고 값과 화면 주제만 다르다.

## 학습 목표

1. 처음 보는 `index.html`·`styles.css`·`app.js`·`data/items.json` 네 파일의 역할을 읽고 어디를 고칠지 찾는다.
2. 폼 제출(`submit`)에서 값을 읽어 배열에 넣고 목록으로 그리고, 항목을 지운다.
3. 목록을 `localStorage`의 `final-items` 키에 저장하고 페이지를 열 때 복원한다.
4. `data/items.json`을 `fetch`로 불러와 목록으로 그리고, 실패하면 안내 문구를 남긴다.
5. 공개 주소(Pages URL)·저장소 주소·마지막 commit 번호(SHA) 세 가지로 제출한다.

## 이번 주 결과물

```text
[캡처 1] https://student01.github.io/web-final/
         제목을 넣고 [추가] → 목록에 한 줄, [지우기]로 사라짐
         새로고침해도 목록이 남아 있음
         추천 목록 3권이 보임
         ← 주소창이 함께 보이게 찍는다
```

`student01`은 예시 아이디다. 본인 GitHub 아이디로 바꿔 읽는다. 저장소 이름은 `web-final`이며 `my-web`과는 다른 새 저장소다.

## 2일 수업 흐름

| 일차 | 설명·안내 30분 | 직접 해결 60분 | 결과 |
|---|---|---|---|
| 1일차 | 시험 범위·starter 구조, 채점표, 제출 세 가지, 허용 자료·장애 대체 | 리허설: 저장소 `web-final` 만들기 → Pages 켜기 → TODO 1~4 | 리허설 공개 URL(확인용) |
| 2일차 | 오늘의 절차, 제출본의 뜻, 구술 1문항, starter 실행 확인 | 본시험 구현 60분 → push → 제출 | 캡처 1 · 제출 세 가지 |

각 수업은 `설명·안내 30분 + 직접 해결 60분`이다. 1일차 리허설은 점수에 들어가지 않는다.
점수는 2일차 본시험의 구현 15점과 시연 5점이다.

## 준비

- GitHub 계정과 2주차에 쓰던 PC 환경(VS Code, 브라우저, Git). 로그인은 1일차에 미리 끝낸다.
- 시험용 새 저장소 `web-final`. **1일차에 만들고 Pages까지 켠다.** 시험 당일에는 저장소를 만들지 않는다.
- 공개 starter 네 파일: [examples/rehearsal_starter](examples/rehearsal_starter) — 13주차 2일차에 공개했다.
- 자기 점검용 완성본: [examples/rehearsal_solution](examples/rehearsal_solution). 1일차 리허설에만 쓴다.
- 공개 저장소·공개 페이지·캡처에 실명·학번·전화번호·실제 이메일을 넣지 않는다. 예시는 `student01`, `student01@example.com`이다.

## 이번 주 용어

| 한국어 | English | 中文 |
|---|---|---|
| 기말 실기 | final practical exam | 期末实操考试 |
| 시작 파일 | starter | 起始文件 |
| 리허설(같은 형태의 연습) | rehearsal | 模拟练习 |
| 채점표 | rubric | 评分表 |
| 공개 주소 | GitHub Pages URL | 网页公开地址 |
| 커밋 번호 | commit SHA | 提交编号 |
| 구술 확인 | oral check | 口头提问 |
| 장애 대체 절차 | fallback procedure | 故障替代方案 |

## 이번 주 범위

| 항목 | 이번 주에 알아둘 뜻 |
|---|---|
| 범위 2~13주 | Pages 배포·HTML·CSS·DOM 이벤트·폼·목록·`localStorage`·`fetch`까지다. 14주 발표 내용은 시험 범위가 아니다 |
| `web-final` | 시험용 새 저장소. `my-web`은 그대로 두고 건드리지 않는다 |
| `data/items.json` | 추천 목록 데이터 파일. `fetch('data/items.json')`처럼 **상대 경로**로 부른다 |
| `final-items` | 이번 시험의 `localStorage` 키 이름. `my-web`의 `guestbook` 키와 섞이지 않게 다른 이름을 쓴다 |
| TODO 1~4 | starter의 `app.js`에 주석으로 표시된 네 자리. 시험에서는 문항이 이 자리를 가리킨다 |
| 제출 세 가지 | 공개 주소(Pages URL) · 저장소 주소 · 마지막 commit 번호(SHA) |
| `git log -1 --format=%H` | 마지막 commit 번호를 한 줄로 본다. 제출 양식에 붙여 넣는다 |
| 구술 1문항 | 시험 후반에 좌석에서 1분. "이 줄이 하는 일"을 본인 코드에서 답한다 |
| 장애 대체 | Pages 반영이 늦으면 로컬 화면 캡처 + SHA로 인정한다(자세한 규칙은 `rubric.md`) |

새 문법·새 API는 이번 주에 없다. 13주차까지 배운 것만 나온다.

## 수업 자료

- [슬라이드](slides.md) · 교재 사이트 덱: https://gbox3d.github.io/teaching_repo/webprg/decks/week15_final_exam/index.html
- [순서대로 따라하기](walkthrough.md)
- [실습과 제출 안내](lab.md)
- [예제 설명](examples/README.md)
- [채점표](rubric.md)
- 공개 starter: [index.html](examples/rehearsal_starter/index.html) · [styles.css](examples/rehearsal_starter/styles.css) · [app.js](examples/rehearsal_starter/app.js) · [data/items.json](examples/rehearsal_starter/data/items.json)
- 리허설 완성본: [app.js](examples/rehearsal_solution/app.js)
- 실습 페이지(GitHub 주소): https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week15_final_exam

## 완료 기준

- [ ] 저장소 `web-final`이 있고 공개 주소 `https://<아이디>.github.io/web-final/`이 열린다(1일차에 확인).
- [ ] 제목을 넣고 **추가**를 누르면 목록에 한 줄이 생기고, **지우기**로 그 줄만 사라진다.
- [ ] 새로고침해도 목록이 그대로 남아 있다.
- [ ] 추천 목록 3권이 보이고, 파일 이름을 틀리게 하면 `불러오지 못했습니다.`가 보인다.
- [ ] 공개 주소·저장소 주소·마지막 commit 번호(SHA)를 제출했다.
- [ ] 주소창이 함께 보이는 캡처 1장을 제출했다.

## 다음 수업 연결

이번 주로 15주 수업이 끝난다. `my-web`(`https://<아이디>.github.io/my-web/`)과 `web-final` 두 저장소는 지우지 않는다.
방학에 이어서 할 것은 `my-web`의 README에 적어 둔 "어려움과 해결" 세 줄이다. 그 세 줄이 다음에 볼 주제다.

## 공식 참고 자료

- [JavaScript 첫걸음 — MDN](https://developer.mozilla.org/ko/docs/Learn_web_development/Core/Scripting)
- [이벤트 입문 — MDN](https://developer.mozilla.org/ko/docs/Learn_web_development/Core/Scripting/Events)
- [Window.localStorage — MDN](https://developer.mozilla.org/ko/docs/Web/API/Window/localStorage)
- [Fetch API 사용하기 — MDN](https://developer.mozilla.org/ko/docs/Web/API/Fetch_API/Using_Fetch)
- [JSON 다루기 — MDN](https://developer.mozilla.org/ko/docs/Learn_web_development/Core/Scripting/JSON)
- [GitHub Pages 사이트 만들기 — GitHub Docs](https://docs.github.com/ko/pages/getting-started-with-github-pages/creating-a-github-pages-site)
- [새 리포지토리 만들기 — GitHub Docs](https://docs.github.com/ko/repositories/creating-and-managing-repositories/creating-a-new-repository)
