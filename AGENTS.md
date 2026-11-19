# teaching_repo 에이전트 작업 지침

이 저장소에서 일하는 에이전트(Claude Code, Codex 등)가 가장 먼저 읽는 저장소 전체 지침이다. 과목 폴더 안의 일은 과목 지침이 정한다. 이 파일은 과목을 넘는 규칙, 사이트 빌드, 여러 에이전트를 함께 돌리는 방식을 정한다. Claude Code는 같은 폴더의 `CLAUDE.md`(`@AGENTS.md` 한 줄)로 이 파일을 읽는다.

이 저장소는 GitHub 공개 저장소이고 `site/`와 각 과목의 `slides.md`가 GitHub Pages 슬라이드 도서관으로 배포된다. 학생과 외부인이 읽는다고 보고 쓴다.

## 저장소 지도

| 위치 | 내용 | 따를 지침 |
|---|---|---|
| `android_programming/` | 모바일프로그래밍 15주, 옛 11~15주 보존 특강(`specials/legacy_week11~15_*`), 특강용 BLE 자료(`bleuno/`) | [android_programming/AGENTS.md](android_programming/AGENTS.md) |
| `web_programming/` | 웹프로그래밍 15주, 특강 6개, 공용 자산(`shared/`), 수업 도구(`tools/`), 개편 기록(`reviews/`) | [web_programming/AGENTS.md](web_programming/AGENTS.md) |
| `open_source_ai/` | 오픈소스 AI 응용 15주, 특강(`specials/`) | [open_source_ai/AGENTS.md](open_source_ai/AGENTS.md) |
| `tools/wleno/` | LAN 시뮬레이터 WlEno와 Android AAR Gradle 프로젝트(`android/`). Android 11~15주와 오픈소스 AI 10~13주가 함께 쓴다 | Android 지침과 오픈소스 AI 지침 둘 다 |
| `tools/bleuno-control/` | WlEno를 TCP로 제어·평가하는 Python 패키지(uv 프로젝트). 오픈소스 AI 10~13주가 쓴다 | 오픈소스 AI 지침(Android 지침도 범위에 넣는다) |
| `tools/github-classroom-pc-reset/` | 실습실 PC의 GitHub 로그인 정리 도구(모든 과목) | 폴더 `README.md` |
| `site/`, `scripts/`, `package.json` | 도서관 원본(`catalog.json`, HTML·CSS·JS)과 빌드·검사 스크립트 | 이 파일의 [사이트 빌드와 검증](#사이트-빌드와-검증) |
| `README.md`, `environment_baseline_template.md`, `ta_lab_setup_guide.md`, `_shared/` | 교재 색인과 공용 교재·학교 자료의 경계, 학기별 환경 기준표 양식, 조교 공통 설치 목록, 과목 공통 자산 승격 기준 | 이 파일 |
| `_forAI/` | 작업 문맥: 구조(inventory), 참고 메모(memo), 이력(dev_log), 할 일(plan), 강의 영상 인수인계 | [_forAI/README.md](_forAI/README.md) |
| `.github/workflows/pages.yml` | main에 push하면 `npm ci` → `npm run build` → `npm test` → Pages 배포 | 이 파일 |

`site/catalog.json`, `scripts/*.mjs`, 루트 `README.md`는 세 과목이 함께 쓰는 파일이다. 과목 작업에서 고칠 때는 자기 과목 항목만 고친다.

## 읽는 순서

1. 이 파일
2. 과목 폴더 안의 일을 맡으면 그 과목의 `AGENTS.md`. 공용 도구(`tools/wleno`, `tools/bleuno-control`)를 맡으면 Android와 오픈소스 AI 지침을 둘 다 읽는다.
3. [_forAI/README.md](_forAI/README.md)의 순서대로 `inventory.md` → `memo.md` → `dev_log.md`(최근 항목) → `plan.md`
4. 맡은 주차·특강·도구의 `README.md`

문서끼리 다르면 저장소 실물(파일, 코드, `git log`)로 판정한다. 과목 안의 일은 과목 지침을 따르고, 실물과 다른 지침 문장은 보고에 적는다. `_forAI` 서술은 커밋보다 늦을 수 있으므로 작업을 시작할 때 `git status --porcelain`과 `git log --since='<dev_log 최신 날짜> 00:00' --oneline`으로 그 뒤의 변경을 확인한다.

## 공개 저장소 규칙

- 추적 파일, 문서, 캡처, 보고서에 API 키·토큰·편집 키·DB 비밀번호, 실제 `.env`, `localfiles/`·`.local/`의 내용을 넣지 않는다. 브라우저용 공개 키를 둘 수 있는 자리는 [웹 지침](web_programming/AGENTS.md)이 정한다.
- 서버·장비의 IP와 호스트 이름, 실제 이메일, 학생 실명·학번, 작업 PC의 절대 경로(드라이브 문자나 사용자 홈으로 시작하는 경로)를 쓰지 않는다. 경로는 저장소 기준 상대 경로로 쓴다. 예시 계정은 `student01`, 예시 이메일은 `student01@example.com`이다. 루프백(`127.0.0.1`), 에뮬레이터의 호스트 별칭(`10.0.2.2`), 문서용 예시 LAN 주소는 써도 된다.
- 학교명·분반·학수번호·실제 날짜·성적 비율·LMS 이름은 공용 교재에 넣지 않는다. 과목 지침에 적힌 예외만 둔다.
- 강의 대본, 실습 해답, 평가 문항·정답, 주차 검사 스크립트는 비공개 짝 저장소 `univ_scoring_works/teaching_materials_private/`에 같은 주차 폴더 이름으로 둔다. 그 내용을 이 저장소로 옮기거나 링크하지 않는다. 공개 슬라이드의 구간 제목·분 범위, 실습 문항, 채점 기준을 바꾸면 비공개 자료도 맞춰야 하므로 보고에 적는다. 비공개 저장소는 사용자가 요청할 때만 열고 고친다.

바꾼 문서에 절대 경로가 남았는지는 다음 명령으로 찾는다. 출력이 없으면 통과다. 드라이브 문자로 시작하는 다른 경로는 직접 읽어 확인한다.

```bash
git grep -nIE --untracked '[A-Za-z]:[\\/](Users|works)|/(Users|home)/[A-Za-z]' -- <바꾼 경로>
```

## 공통 작성 규칙

- 모든 덱은 `slides.md`(한국어)와 `slides_en.md`(영어)를 같은 폴더에 둔다. 장 구분 `---`의 수와 순서, 코드 블록 수가 같아야 한다. 한쪽을 고치면 다른 쪽도 같은 작업에서 고친다.
- 한국어 문서(README, walkthrough, lab, `_forAI`, 보고서)는 `korean-copy-style` 문서 규칙을 따른다. 해라체로 쓰고, 질문형 제목과 꾸밈말을 쓰지 않는다. 슬라이드 말투는 덱마다 다르므로 과목 지침과 그 덱의 기존 말투를 따른다. 검사기가 있는 환경이면 바꾼 문서에 돌린다.
- 줄바꿈은 LF, 인코딩은 BOM 없는 UTF-8이다(`.gitattributes`의 `* text=auto eol=lf`). 작업 트리의 줄바꿈은 `git ls-files --eol -- <경로>`(추적 파일)와 `git ls-files --eol -o --exclude-standard -- <경로>`(새 파일)로 본다. 바꾸거나 만든 파일에 `w/crlf`·`w/mixed`가 없어야 한다.
- 사본이 같은지 볼 때는 `git hash-object <파일A> <파일B>`를 쓴다. 줄바꿈을 맞춘 뒤 해시를 내므로 작업 트리의 CRLF 때문에 결과가 어긋나지 않는다.
- 측정하지 않은 결과(실기기, 다른 OS, GPU 시간, 학생 소요 시간)를 확인한 것처럼 쓰지 않는다. 확인한 수치는 장비·버전·조건과 함께 쓴다.

## 사이트 빌드와 검증

저장소 루트에서 실행한다. Node.js 24 이상과 Git 체크아웃이 필요하다(`render-site.mjs`가 `git ls-files`로 웹 예제 파일을 고른다).

```bash
npm ci
npm run build   # site/catalog.json → dist/
npm test        # npm run check + scripts/deck-fit.test.mjs + npm run test:labs
```

| 명령 | 통과 기준 |
|---|---|
| `npm run build` | 마지막 줄 `교재 도서관 빌드 완료: N개 덱, M장 (영문판 N개 덱, M장), …`의 N·M이 스크립트 상수와 같다. `경고: 영문판 장수가 한국어판과 다릅니다`가 없다(이 경고는 빌드를 멈추지 않는다) |
| `npm test` | 종료 코드 0. 사이트 검사(`dist/`의 덱·장 수, 로컬 링크와 `#앵커`, 로컬 설정 유출), 슬라이드 맞춤 시험, 웹 실습 시험(`test:labs`, 지도 시험 `test:maps` 포함)이 모두 통과한다 |
| `npm run check` | `dist/` 검사만 다시 돌린다. 빌드 뒤에만 의미가 있다 |
| `npm run test:labs` | 웹 정적 서버·방명록 API·홈 IoT·Supabase 06 시험과 지도 시험. `dist/`가 필요 없어 과목 작업 중에 돌려도 된다 |

전체 덱과 슬라이드의 기대값은 `scripts/check-site.mjs`의 `EXPECTED_DECKS`·`EXPECTED_SLIDES`에 있고 과목별 값은 `EXPECTED`에 있다. 덱이나 장 수를 바꾸면 다음을 같은 작업에서 고친다.

- `scripts/render-site.mjs`와 `scripts/check-site.mjs`의 `EXPECTED_DECKS`·`EXPECTED_SLIDES`, `check-site.mjs`의 `EXPECTED[과목]`
- `site/catalog.json`의 과목 `summary`에 장 수가 적혀 있으면 그 수
- 덱을 더하거나 이름을 바꾸면 `catalog.json`의 `chapters`. 이름을 바꾸면 옛 id를 `formerIds`에 남겨 옛 주소를 새 덱으로 넘긴다. `sourcePath`는 세 과목 모두 `weeks/`와 `specials/`를 이미 매핑하므로 새 폴더 종류를 만들 때만 고친다.

공용 도구(`tools/wleno`, `tools/bleuno-control`)와 과목 예제의 시험 명령은 과목 지침의 검증 절에 있다. 링크·앵커를 자동으로 검사하는 것은 빌드된 덱 HTML뿐이다. README·lab·walkthrough의 상대 링크와 `#앵커`는 바꾼 곳을 직접 확인한다.

## 하지 말 것

- 사용자가 요청하지 않은 commit, push, 브랜치 변경, stash, reset, checkout, restore를 하지 않는다.
- 다른 세션이나 에이전트가 만든 커밋 안 된 변경을 되돌리거나 덮어쓰지 않는다. 작업을 시작할 때 `git status --porcelain` 결과를 저장소 밖에 저장하고, 끝낼 때 다시 비교해 맡은 파일만 바뀌었는지 본다.
- 사용자가 요청하지 않으면 `_forAI/` 문서를 고치지 않는다. 대신 보고에 dev_log·plan·memo·inventory에 넣을 초안을 붙인다.
- 공용 도구(`tools/wleno`, `tools/bleuno-control`)의 명령·응답·상태 규칙·모델 프롬프트를 한 과목 문서만 맞춰 바꾸지 않는다. Android 11~15주와 오픈소스 AI 10~13주 문서, 측정 기록을 같이 본다.
- 산출물을 커밋하지 않는다. `dist/`, `node_modules/`, `.venv/`, `__pycache__/`, `build/`(웹 예제 안의 `build/` 폴더는 예외), 실제 `.env`, `config.js`·`config.json`은 루트 `.gitignore`가 제외한다. Android `local.properties`는 `tools/wleno/android/.gitignore`만 제외하므로 다른 곳에서 만들었으면 커밋 전에 직접 뺀다.
- 검증하면서 저장소에 흔적을 남기지 않는다. Python 시험은 `python -B`로, uv 검증은 `uv run --frozen`으로 돌린다. 임시 스크립트와 캡처는 저장소 밖에 둔다(웹 빌드는 `examples/` 아래의 추적 안 된 파일도 사이트로 복사한다).

## 여러 에이전트로 작업하는 방식

교재개발 총괄 디렉터가 정한 운영 방식이다(2026-11-18). 과목을 나눠 동시에 고치거나, 문서·지침을 정비할 때 쓴다.

| 역할 | 하는 일 | 쓰는 파일 |
|---|---|---|
| 총괄(오케스트레이터) | 시작 상태 저장, 과목별 범위와 허용 파일 지정, 공유 명령(사이트 빌드) 실행, 결과 통합 지시 | 없음 |
| 과목 작업 에이전트 | 맡은 과목만 독립적으로 작업하고 과목 지침의 보고 형식으로 보고 | 지정받은 허용 파일 |
| 독립 검증 에이전트 | 작업에 참여하지 않은 에이전트가 저장소 실물과 대조해 채점 | 쓰지 않는다 |
| 통합 담당 | 과목 결과를 루트 문서와 `_forAI/`에 합친다. 그 결과도 같은 방식으로 검증받는다 | 지정받은 통합 파일 |

진행 순서는 다음과 같다.

1. 총괄이 `git status --porcelain`을 저장하고 과목별 범위와 허용 파일을 정한다.
2. 과목 작업 에이전트가 각자 작업한다. 다른 과목의 결과를 기다리지 않는다. 결과는 바꾼 파일, 갱신 정리(커밋·미커밋 구분), dev_log 초안, plan·memo·inventory 변경안, 발견했지만 고치지 않은 문제, 실행한 확인과 결과로 돌려준다.
3. 독립 검증 에이전트가 아래 루브릭으로 10점 만점 채점하고, 고쳐야 할 것(must_fix)과 사소한 것(minor)을 나눠 돌려준다. 검증 에이전트는 파일을 고치지 않고, 임시 파일은 저장소 밖에 둔다.
4. 7점 이상이면 통과다. 미달이면 작업 에이전트가 검증 피드백을 받아 다시 작업하고 다시 채점받는다. 다시 작업은 최대 3번이다. 그래도 미달이면 중단하고 사람에게 넘긴다. 넘길 때는 회차별 점수, 남은 must_fix, 바뀐 파일 목록을 함께 준다.
5. 통과했어도 고치지 않은 must_fix·minor는 통합 담당이 `_forAI/plan.md`나 보고의 발견 문제로 넘긴다.
6. 회차와 점수는 `_forAI/dev_log.md`에 남긴다. 검증자를 바꿔 회차를 처음부터 다시 세지 않는다.

| 채점 항목 | 배점 | 보는 것 |
|---|---|---|
| 정확성 | 3 | 문서에 적힌 경로·명령·숫자·사실을 15개 이상 표본으로 실물과 대조한다. 문서가 안내하는 가벼운 검증 명령은 직접 실행한다(사이트 전체 빌드는 제외) |
| 변경 정리 완전성 | 2 | `git log --since='YYYY-MM-DD 00:00'`, `git diff HEAD --stat`, 새 파일 목록과 비교해 빠진 주요 변경, 지어낸 변경, 커밋과 미커밋의 혼동이 있는지 본다 |
| 지침·결과물 실용성 | 3 | 처음 맡은 에이전트가 문서만 보고 시작·수정·전파·검증·보고할 수 있는지 본다. 범위, 구조, 함께 고칠 곳, 검증 명령, 하지 말 것, 완료 기준이 있어야 한다. 군더더기, 다른 문서와의 중복, 지금 구조와 맞지 않는 옛 내용은 감점한다 |
| 안전·경계 | 1 | 비밀정보·IP·호스트 이름·이메일·학생 정보·작업 PC 절대 경로가 없고, 시작 상태와 비교해 허용 파일 밖의 변경이 없다 |
| 문체 | 1 | `korean-copy-style` 문서 규칙과 문체 검사기 결과 |

치명 결함은 네 가지다. 존재하지 않는 경로·명령을 맞는 것처럼 안내한 것, 비밀정보 노출, 허용 파일 밖 수정, 지어낸 변경 이력이다. 하나라도 있으면 총점은 6점 이하다. 7점은 "그대로 써도 되고 남은 문제는 사소하다"는 뜻이다. 총점은 항목 점수의 합과 같아야 한다.

동시에 일할 때 지킬 것은 다음과 같다.

- 에이전트마다 서로 다른 파일만 쓴다. 공용 파일(`site/catalog.json`, `scripts/*.mjs`, 루트 `README.md`, `_forAI/`)은 한 에이전트에게만 맡기거나 통합 단계에서 고친다.
- `npm run build`처럼 공유 산출물(`dist/`)을 만드는 명령은 한 번에 하나만 돌린다. 과목 에이전트는 `npm run test:labs`나 단위 시험처럼 공유 산출물을 쓰지 않는 확인만 하고, 빌드 결과는 총괄이 한 번 돌려 나눠 준다.
- `uv run`은 대상 폴더에 `.venv/`를 만든다. 같은 폴더를 두 에이전트가 동시에 쓰지 않는다.

`_forAI/lecture-video.md`의 "독립 검토" 기준(7점 초과, 5번째 반려에서 중단)은 2026-11-16 강의 영상 문서 요청에 정한 기준이다. 다른 작업에는 위 방식을 쓴다.

## 완료 기준과 보고

다음을 모두 만족하면 완료다.

- 맡은 과목 지침의 완료 기준을 만족한다.
- 슬라이드·catalog·예제를 바꿨으면 `npm run build`와 `npm test`가 통과하고 빌드 출력의 덱·장 수가 상수와 같다. 직접 돌리지 못했으면 누가 언제 돌린 결과인지 밝힌다.
- 시작 상태와 비교해 허용 파일 밖의 변경이 없고, 공개 저장소 규칙을 어긴 곳이 없다.

보고는 한국어로 쓰고 과목 지침의 보고 형식을 따른다. 여러 과목에 걸친 작업은 과목별로 나눈다. 모든 보고에 다음을 넣는다.

- 바꾼 파일(저장소 기준 상대 경로)과 커밋 여부. 커밋된 변경과 커밋 안 된 변경을 나눠 쓴다.
- 실행한 확인과 결과, 실행하지 않은 확인과 그 이유
- 발견했지만 고치지 않은 문제
- 비공개 짝 저장소와 `_forAI/`에 반영할 내용의 초안
