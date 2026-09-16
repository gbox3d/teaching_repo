# 9주차 — 1차 과제 발표와 브랜치 복습

실습 페이지: https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week09_architecture_project

## 이번 주 질문

> 3~7주에 한 주씩 쌓아 온 내 사이트를, 공개 주소를 열어 **2분 안에** 남에게 보여 줄 수 있을까? 그리고 그 설명을 저장소 첫 화면에 한 장으로 남길 수 있을까?

8주차 중간 실기는 `my-web/exam/` 폴더에서 혼자 만들었다. 이번 주에 보여 주는 것은 그 `exam/`이 아니라 3~7주에 만든 **`my-web` 본체**다.
홈·내 정보·방명록 세 페이지, CSS로 꾸민 화면, 버튼 하나, 폼 하나가 그 자리에 있다. 1일차에는 발표 순서를 정하고 저장소 `README.md` 1차판을 쓰며,
그 작업을 `readme` 브랜치에서 해 main에 합치는 것으로 2·3·6주에 배운 브랜치를 한 바퀴 복습한다. 2일차가 발표다.

## 학습 목표

1. 공개 주소 → 세 페이지 이동 → 버튼·폼 시연 → GitHub **Commits** 탭 순서로 2분 발표를 한다.
2. 화면에 보이는 것이 만들어지는 곳 세 군데(화면·브라우저 저장소·인터넷 서버)를 구분해 말한다.
3. `git switch -c readme`로 브랜치를 만들어 작업하고, `git merge`로 main에 합친다.
4. 합친 브랜치를 `git branch -d`와 `git push origin --delete`로 내 PC와 GitHub에서 각각 지운다.
5. 저장소 `README.md`를 마크다운 세 가지(`#`·`-`·`[링크](https://주소)`)만으로 5항목으로 쓴다.
6. 내 화면 두 장을 캡처해 `screenshots/` 폴더에 넣고 README에서 링크로 가리킨다.

## 이번 주 결과물

```text
[발표 2분] https://student01.github.io/my-web/
           홈 → 내 정보 → 방명록 → 버튼 한 번 → 폼 한 번 → Commits 탭

[레포트]   https://github.com/student01/my-web 의 첫 화면에 보이는 README.md
           제목 / 공개 주소 / 페이지 3개 / 기능 2개 / 화면 2장 / 이번에 배운 것 3줄
```

`student01`은 예시 아이디다. 본인 GitHub 아이디로 바꿔 읽는다.
이번 주는 주차별 실습 점수 대상이 아니라 **1차 과제 10점**(발표 5 + 레포트 5)이다.

## 2일 수업 흐름

| 일차 | 설명·함께 따라하기 30분 | 천천히 연습하기 60분 | 결과 |
|---|---|---|---|
| 1일차 | 2분 발표 형식, 데이터가 가는 세 곳, 오늘 Git 10분(기능 브랜치 한 바퀴), 좋은 시작·피할 시작, README 1차판 5항목 | `readme` 브랜치 → 화면 2장 캡처 → README 1차판 → push → merge → 브랜치 삭제 → 짝과 2분 리허설 | 저장소 첫 화면의 README |
| 2일차 | 오늘 순서와 준비, 채점표 10점, 2분 시연 한 번 보기, 공개 주소가 안 열릴 때 | **발표 2분 × 인원** — 공개 주소 → 세 페이지 → 버튼·폼 → Commits 탭 | 발표와 제출 |

각 수업은 `설명·함께 따라하기 30분 + 60분`이다. 2일차 60분은 연습이 아니라 **평가 시간**이다.

## 준비

- 8주차까지 push한 `my-web` 저장소. 같은 PC면 `git pull`, 다른 PC면 `git clone https://github.com/<아이디>/my-web.git`
- VS Code, 브라우저, Git (`git --version`으로 확인)
- 3~7주에 만든 세 페이지(`index.html`·`about.html`·`guestbook.html`)와 `styles.css`·`app.js`·`guestbook.js`. 빠진 파일이 있으면 [따라하기 3~4단계](walkthrough.md#3-홈-화면-세-파일-확인하기)에서 채운다
- 화면 캡처 단축키: Windows **Win+Shift+S**, macOS **⌘+Shift+4**
- 과제 안내와 채점 기준을 미리 읽는다: [1차 과제 안내](project_brief.md) · [채점표](rubric.md)
- 공개 저장소·공개 페이지·캡처에 실명·학번·전화번호·실제 이메일을 넣지 않는다. 예시는 `student01`, `student01@example.com`이다

## 이번 주 용어

| 한국어 | English | 中文 |
|---|---|---|
| 1차 과제 | first assignment | 第一次作业 |
| 발표·시연 | presentation · demo | 演示 |
| 레포트 | report (README) | 报告 |
| 기능 브랜치 | feature branch | 功能分支 |
| 합치기 | merge | 合并 |
| 원격 브랜치 지우기 | delete remote branch | 删除远程分支 |
| 화면 캡처 | screenshot | 截图 |
| 저장소 설명 파일 | README | 说明文件 |

## 이번 주 범위

| 명령·용어 | 이번 주에 알아둘 뜻 |
|---|---|
| `git switch -c readme` | `readme` 브랜치를 만들면서 그 브랜치로 옮겨 간다. 6주차 `dark-mode`와 같은 명령이다 |
| `git push -u origin readme` | 처음 올리는 브랜치를 GitHub에 올린다. `-u`가 있어서 다음부터는 `git push`만 쳐도 된다 |
| `git merge readme` | 지금 있는 브랜치(main)에 `readme`의 commit을 가져와 합친다 |
| `git branch -d readme` | 합친 브랜치를 **내 PC에서** 지운다. commit은 main에 남는다 |
| `git push origin --delete readme` | 같은 브랜치를 **GitHub에서** 지운다. 두 곳은 따로 지운다 |
| `README.md` | 저장소 첫 화면 아래에 그대로 보이는 설명 파일. 이번 주 레포트가 이 파일이다 |
| `# 제목` · `## 작은 제목` | 마크다운 제목. `#` 개수가 크기다 |
| `- 항목` | 마크다운 목록 한 줄 |
| `[보이는 글](https://주소)` | 마크다운 링크. 같은 저장소 안의 파일은 `screenshots/home.png`처럼 파일 이름만 적는다 |
| `screenshots/` | 내 화면 캡처를 넣는 폴더. 저장소 루트에 새로 만든다 |
| GitHub **Commits** 탭 | 저장소에 쌓인 commit 목록. 발표 마지막 20초에 보여 준다 |

`--set-upstream-to`는 따로 배우지 않는다. `git push -u`가 그 일을 대신한다.
Pull Request로 합치기, 충돌(conflict) 해결, `rebase`는 이 과목에서 다루지 않는다.

## 수업 자료

- [슬라이드](slides.md) · 교재 사이트 덱: https://gbox3d.github.io/teaching_repo/webprg/decks/week09_architecture_project/index.html
- [순서대로 따라하기](walkthrough.md)
- [실습과 발표 안내](lab.md)
- [1차 과제 안내](project_brief.md) · [채점표 10점](rubric.md)
- [예제 설명](examples/README.md)
- README 1차판 예: [examples/day1/README.md](examples/day1/README.md)
- 화면 캡처 예: [home.png](examples/day1/screenshots/home.png) · [guestbook.png](examples/day1/screenshots/guestbook.png)
- 발표에서 보여 줄 파일: [index.html](examples/day1/index.html) · [about.html](examples/day1/about.html) · [guestbook.html](examples/day1/guestbook.html) · [styles.css](examples/day1/styles.css) · [app.js](examples/day1/app.js) · [guestbook.js](examples/day1/guestbook.js)
- 실습 페이지(GitHub 주소): https://github.com/gbox3d/teaching_repo/tree/main/web_programming/weeks/week09_architecture_project

## 완료 기준

- [ ] `https://<아이디>.github.io/my-web/`이 열리고 nav로 세 페이지를 오갈 수 있다.
- [ ] 홈에서 버튼을 누르면 문장이 바뀌고 `클릭 N회`의 숫자가 오른다.
- [ ] 방명록에서 이름·메시지를 넣고 **[남기기]**를 누르면 한 줄이 보이고, 비우고 누르면 안내가 보인다.
- [ ] 저장소 `my-web`의 첫 화면에 README 1차판 5항목이 보이고 캡처 2장이 화면에 나타난다.
- [ ] `readme` 브랜치를 만들어 작업하고 main에 합친 뒤 양쪽에서 지웠다.
- [ ] 저장소 첫 화면(README가 보이는 화면)을 캡처 1장으로 제출했다.
- [ ] 2일차에 2분 발표를 했다.

## 다음 수업 연결

지금 방명록은 두 번째 글을 남기면 앞 글이 사라진다. 10주차에는 배열에 글을 **쌓아** 목록으로 그리고 항목을 지운다.
11주차에는 그 목록이 새로고침해도 남게 하고, 12주차에는 JSON 파일에서 데이터를 불러온다.
오늘 쓴 README는 13주차에 최종판으로 다시 쓰고, 14주차 최종 발표의 레포트가 된다.

## 공식 참고 자료

- [README 정보 — GitHub Docs](https://docs.github.com/ko/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes)
- [기본 쓰기 및 서식 지정 구문 — GitHub Docs](https://docs.github.com/ko/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax)
- [리포지토리의 브랜치 보기 — GitHub Docs](https://docs.github.com/ko/repositories/configuring-branches-and-merges-in-your-repository/managing-branches-in-your-repository/viewing-branches-in-your-repository)
- [리포지토리 내에서 분기 관리(브랜치 삭제) — GitHub Docs](https://docs.github.com/ko/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-and-deleting-branches-within-your-repository)
- [리포지토리에서 새 파일 만들기 — GitHub Docs](https://docs.github.com/ko/repositories/working-with-files/managing-files/creating-new-files)
- [GitHub Pages 사이트 만들기 — GitHub Docs](https://docs.github.com/ko/pages/getting-started-with-github-pages/creating-a-github-pages-site)
