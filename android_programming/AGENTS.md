# 모바일프로그래밍(Android) 작업 지침

모바일프로그래밍 교재를 맡은 에이전트가 작업을 시작하고, 고치고, 검증하고, 보고하는 기준이다. 이 저장소는 공개 저장소(GitHub Pages 슬라이드 도서관)이므로 학생과 외부인이 읽는다고 보고 쓴다.

## 범위

| 위치 | 내용 |
|---|---|
| `android_programming/` | 정규 15주(`weeks/`), 보존 특강(`specials/`), 특강용 BLE 자료(`bleuno/`), 수업 전 연결 점검(`iot_sim/lab.md`), 조교 설치 목록(`ta_setup_guide.md`) |
| `tools/wleno/` | 11~15주에 쓰는 PC 시뮬레이터 WlEno, 학생용 AAR을 만드는 `android/` Gradle 프로젝트 |
| `tools/bleuno-control/` | WlEno를 TCP로 제어·평가하는 Python 패키지. 오픈소스 AI 10~13주가 쓴다 |

`tools/wleno/`와 `tools/bleuno-control/`은 오픈소스 AI 과목과 함께 쓴다. 두 폴더를 바꿀 때는 [오픈소스 AI 지침](../open_source_ai/AGENTS.md)도 지킨다. `site/catalog.json`과 `scripts/*.mjs`는 전 과목 공용이므로 Android 항목만 고친다.

## 먼저 읽을 문서

1. [과목 README](README.md): 11주차 이후 학습 흐름과 자료 목록
2. [주차 색인](weeks/README.md): 운영 기준, 주차 폴더 구성, 예제를 넣는 위치, 자료 작성 원칙, 문법 도입 표
3. 맡은 주차의 `README.md`
4. 11~15주나 도구를 맡으면 [WlEno 안내](../tools/wleno/README.md)와 [AAR 안내](../tools/wleno/android/README.md)
5. 특강을 맡으면 [특강 목록](specials/README.md)과 [bleuno 안내](bleuno/README.md)
6. [_forAI 안내](../_forAI/README.md)의 읽는 순서(inventory, memo, dev_log, plan)
7. 공개해도 되는 내용의 경계: [루트 README의 경계 표](../README.md#공용-교재와-학교-운영자료의-경계)

`_forAI/` 문서와 저장소 파일이 다르면 파일을 따르고 보고에 차이를 적는다.

## 과목 구성

15주, 주 2회 90분(설명·시연 30분과 실습 60분)이다. 1~3주는 `StudentCard`, 4~10주는 SmartIO(`com.example.smartio`), 11~15주는 새 앱 RoomControl(`com.example.roomcontrol`)을 만든다. 11~15주 앱은 학생이 `app/libs/`에 넣은 `wleno-android-0.1.0.aar`로 PC의 WlEno에 TCP로 연결한다. 학생은 연결 화면과 제어 화면을 작성하고, 소켓·스레드·검색은 AAR이 맡는다. 2026-11-18 이전의 11~15주(연락처·BLE)는 `specials/legacy_week11~15`에 특강 1~5로 보존했다.

## 폴더와 이름 규칙

주차 폴더의 파일 역할은 [주차 폴더 구성 표](weeks/README.md#주차-폴더-구성)가 정본이다. 여기에는 작업할 때 놓치기 쉬운 점만 적는다.

- 주차 폴더는 `weeks/weekNN_주제`(두 자리 번호), 보존 특강은 `specials/legacy_weekNN_옛주제`다. 폴더 이름이 사이트의 chapter id다. 이름을 바꾸면 `site/catalog.json`의 `id`를 고치고 옛 이름을 `formerIds`에 남긴다. 옛 주소가 새 덱으로 넘어간다.
- `slides.md`(한국어)와 `slides_en.md`(영어)는 장 구분 `---`의 수와 순서, 코드 블록 수가 같다. 코드 블록 안의 화면 그림·주석·문자열은 언어에 맞게 번역되어 있으므로 코드를 고치면 두 파일을 따로 고친다.
- 슬라이드 구간 제목 형식이 둘로 갈려 있다. 1~10주는 `## N일차 · A–B분 — 제목`, 11~15주는 `# N일차 · A~B분: 제목`(12·13주는 `· 제목`)이다. 고치는 덱의 기존 형식을 따른다. 통일 여부는 강의자가 비공개 대본과 대조한 뒤 정한다.
- `examples/dayN/`은 그날 수업이 끝났을 때의 완성본 전체 파일이다. 예외는 1주 문법 `.kt` 7개, 8주 `aNN_*/README.md`, 13주 `day1`만, 15주 `rehearsal_starter`·`rehearsal_solution`이다.
- 1~10주 `walkthrough.md`의 전체 코드 블록은 예제 파일과 글자 단위로 같게 유지한다. 11~15주 walkthrough와 슬라이드는 일부 줄만 인용한다. 인용한 줄은 예제에 그대로 있어야 하며, 슬라이드는 화면 폭 때문에 줄을 나눈 곳이 있다.
- `lab.md`에는 예상·관찰 표와 힌트만 둔다. 정답, 실측 기록, 강의 대본은 공개 폴더에 두지 않는다.
- 문서(`README.md`·`walkthrough.md`·`lab.md`)는 해라체로 쓴다. 슬라이드는 그 덱의 기존 말투를 따른다. 지금 1~10주 슬라이드는 합쇼체, 11~15주 슬라이드는 해라체이며 통일 여부는 강의자가 정한다. 앱 화면 문구(`strings.xml`, Toast, 상태 글자)는 명사형이나 합쇼체로 쓴다. 예: `응답 대기 중`, `IPv4 주소와 포트를 입력하세요.`

## 함께 고칠 곳

| 바꾼 것 | 같이 볼 곳 |
|---|---|
| 슬라이드 | 같은 주차의 다른 언어 슬라이드. 장 수가 바뀌면 `scripts/check-site.mjs`의 `EXPECTED.android`와 두 스크립트(`render-site.mjs`, `check-site.mjs`)의 `EXPECTED_DECKS`·`EXPECTED_SLIDES`. 구간 제목과 분 범위는 비공개 강의 대본과 같아야 한다 |
| 주차 제목·산출물 | `site/catalog.json`의 한·영 `title`·`description`, `weeks/README.md` 주차 목록, 과목 README 학습 흐름 표 |
| 11~15주 예제 파일 | 아래 사본 관계의 다른 주차, 그 줄을 인용한 walkthrough·slides·lab·`examples/README.md`, 다음 주차 README의 시작점 |
| WlEno 동작·명령·포트·실행 명령 | `tools/wleno/README.md` 1·8·11절, `tools/wleno/tests/`, `tools/wleno/examples/*.http`, `tools/wleno/android/README.md`·`INSTALL.md`, 11~15주 문서, `iot_sim/lab.md`, `ta_setup_guide.md`, `bleuno/README.md` 10절, `tools/bleuno-control/`(README·`src`·`tests`), 오픈소스 AI 10~13주 |
| AAR 소스(`tools/wleno/android/src`) | `gradle.properties`의 `wlenoVersion`을 올리고 AAR을 다시 만들어 GitHub Release에 올린다. 파일 이름이 나오는 문서(`git grep -l --untracked "wleno-android-0.1.0"`)도 고친다. 릴리스 없이 소스만 고치면 학생 앱은 바뀌지 않는다 |
| 특강 공통 클래스(`bleuno/src`) | `specials/legacy_week12~15`의 사본 7곳, 그 특강 walkthrough 부록의 전문, `bleuno/README.md`의 파일 표 |
| 학생 실습 범위·채점 기준 | 비공개 짝 저장소의 해답·대본. 직접 고치지 못하면 보고에 적는다 |

11~15주 예제 사본의 관계(2026-11-18 확인)는 다음과 같다.

- `MainActivity.kt`는 11주 `day2`부터 15주 두 폴더까지 8곳이 같고 11주 `day1`만 다르다.
- `activity_main.xml`, `strings.xml`, `res/values/themes.xml`은 9곳이 모두 같다. `AndroidManifest.xml`은 11주 `day1`만 다르다.
- `ControlActivity.kt`는 12주 `day2`와 13주 `day1`이 같고, 14주 `day2`와 15주 `rehearsal_solution`이 같다. `rehearsal_starter`는 TODO를 비워 둔 판이다. `activity_control.xml`도 12주 `day2`와 13주 `day1`이 같고, 14주 `day2`와 15주 두 폴더가 같다.

## 하지 말 것

- 정규 11~15주에 BLE, SmartIO, 연락처, Fake 모드를 다시 넣지 않는다. 그 자료는 특강이다(커밋 `738c81f`).
- 학생에게 통신 소스나 ZIP을 복사하게 하지 않는다. AAR 한 개를 압축을 풀지 않고 `app/libs/`에 넣는다(커밋 `df20c68`).
- UDP 검색을 필수 단계로 만들지 않는다. 수업은 IP 직접 연결로 한다. 정규 11~15주 예제에는 `INTERNET` 외의 권한(Bluetooth·Wi-Fi·위치)을 넣지 않는다. `targetSdk`는 36이며 37부터는 로컬 네트워크 권한 처리가 필요하다.
- `specials/legacy_*`를 새 수업에 맞춰 고치지 않는다. 본문의 주차 번호와 평가 일정은 원래 수업의 기록이다. 깨진 링크와 경로만 고친다.
- WlEno 동작을 보드나 Fake와 같다고 쓰지 않는다. WlEno의 동작은 `tools/wleno/README.md` 1·8절이 정본이고, 보드와 Fake의 규칙은 `bleuno/README.md`에 따로 있다.
- 없어진 실행 경로를 되살리지 않는다: `uv run main`, `pygame-ce`, `sim.py`, `tools/bleuno-sim`, `iot_sim/sim.py`.
- 10주차 권한 거절 흐름(처음 거절은 Toast, 다시 물을 수 없을 때만 설정 대화상자)을 되돌리지 않는다(2026-11-11 결정).
- 보고만 하기로 한 기존 문제는 강의자 결정 없이 고치지 않는다. 7·9·10주 `ConnViewModel`의 `catch (e: Exception)`이 취소를 삼키는 문제와 Switch 리스너가 회전 때 다시 불리는 문제다(`_forAI/plan.md` 10번).
- 학교명, 분반, 실제 날짜, 배점 비율, LMS 이름, 학생 정보, 실제 서버 주소, 키를 넣지 않는다. 채점표는 기존 배점 체계(8주 20점, 13주 계획안 10점과 최종 제출 20점, 15주 20점)를 유지한다.
- 실기기, 학교 Wi-Fi, macOS·Linux 실행처럼 확인하지 않은 결과를 확인한 것처럼 쓰지 않는다.
- 사용자 동의 없이 `_forAI/`를 고치거나 commit·push하지 않는다.
- `dist/`, `build/`, `__pycache__/`, `.venv/`, `local.properties`를 추적하지 않는다. 사이트 빌드는 여러 작업자가 동시에 돌리지 않는다(`dist/`가 충돌한다).

## 검증

저장소 루트에서 실행한다. `python`이 없으면 Windows는 `py`, macOS·Linux는 `python3`를 쓴다. 확인 칸은 2026-11-18 결과다.

| 명령 | 통과 기준 | 확인 |
|---|---|---|
| `python -B -m unittest discover -s tools/wleno/tests` | `OK`(35개). 창 시험에는 Tkinter와 디스플레이가 필요하다 | 실행함 |
| `uv run --frozen --project tools/bleuno-control python -B -m unittest discover -s tools/bleuno-control/tests` | `OK`(15개). `tools/bleuno-control/.venv`가 생긴다(Git 제외) | 실행함 |
| `python -B tools/wleno/main.py --help` | 옵션 목록 출력 | 실행함 |
| `git diff --check HEAD -- android_programming tools/wleno tools/bleuno-control` | 종료 코드 0, 공백 오류 줄 없음. `CRLF will be replaced by LF` 경고는 작업 트리 줄바꿈 안내라 오류가 아니다 | 실행함 |
| `npm run build` 뒤 `npm test` | 빌드 출력의 덱·장 수가 스크립트 상수와 같고 시험 통과 | 이 문서를 쓸 때는 실행하지 않았다. 같은 작업 트리에서 58개 덱·1,175장(Android 20개·378장)으로 통과한 기록이 있다 |
| `tools/wleno/android`에서 `.\gradlew.bat packageDistribution`(macOS·Linux는 `sh ./gradlew packageDistribution`) | `dist/wleno-android-0.1.0.aar` 생성 | 실행하지 않았다(Android SDK 필요) |
| 11~15주 예제 빌드 | Empty Views Activity 프로젝트에 예제와 AAR을 넣고 `assembleDebug` 성공 | 실행하지 않았다 |

전파 확인용 명령(Git Bash)은 다음과 같다. 주석에 통과 기준을 적었다.

```bash
# 한·영 슬라이드의 장 구분 수 비교. 출력이 없으면 통과
for f in android_programming/{weeks,specials}/*/slides.md; do
  k=$(grep -cE '^---\s*$' "$f"); e=$(grep -cE '^---\s*$' "${f%.md}_en.md")
  [ "$k" = "$e" ] || echo "장 수 다름: $f $k/$e"
done

# Android 장 수 추정. check-site.mjs의 EXPECTED.android(20개 덱, 378장)와 비교하고 확정 값은 빌드 출력으로 본다
for f in android_programming/{weeks,specials}/*/slides.md; do grep -cE '^---\s*$' "$f"; done \
  | awk '{s+=$1-1} END {print NR" decks", s" slides"}'

# 11~15주 예제 사본. 같은 해시 묶음이 위 사본 관계와 맞아야 한다(MainActivity.kt 8곳+1곳 등)
for n in MainActivity.kt activity_main.xml strings.xml AndroidManifest.xml; do
  echo "$n"; git hash-object android_programming/weeks/week1[1-5]*/examples/*/$n | sort | uniq -c
done

# 특강 bleuno 사본 7곳. 출력이 없으면 통과
for f in android_programming/bleuno/src/*.kt; do
  for c in android_programming/specials/legacy_week1*/examples/*/bleuno/$(basename "$f"); do
    [ "$(git hash-object "$f")" = "$(git hash-object "$c")" ] || echo "다름: $c"
  done
done

# 바꾼 문자열이 남은 곳 찾기(커밋 전 새 파일 포함)
git grep -n --untracked "찾을 문자열" -- android_programming tools open_source_ai
```

`git hash-object`는 줄바꿈을 LF로 맞춘 뒤 해시를 낸다. 작업 트리에 CRLF 파일이 있으면 `sha256sum`은 다른 값을 내므로 사본 비교에는 `git hash-object`를 쓴다. 링크·앵커 검사 스크립트는 저장소에 없으므로 바꾼 문서의 상대 링크와 `#앵커`는 직접 확인한다. 비공개 짝 저장소의 주차 검사 스크립트를 새 11~15주 구조에서 돌린 기록은 `_forAI/dev_log.md`에 아직 없다.

## 완료 기준

- 바꾼 내용이 위 '함께 고칠 곳' 표의 해당 자리에 모두 반영되어 있다.
- 바꾼 범위에 해당하는 검증 명령이 통과했고, 실행하지 않은 명령은 이유와 함께 보고에 남겼다.
- 슬라이드를 바꿨으면 빌드 출력의 장 수와 스크립트 상수가 같다.
- 작업 전 `git status --porcelain`과 비교해 맡은 파일 밖의 변경이 없다. 새 파일은 BOM 없는 UTF-8과 LF다(`git ls-files --eol -o --exclude-standard -- <경로>`의 `w/lf`로 확인. `-o` 없이는 새 파일이 출력되지 않는다).
- 공개하면 안 되는 정보가 없다.

## 보고 형식

한국어로 다음 순서에 따라 보고한다.

1. 바꾼 것: 수업 단위(주차·일차·도구)로 무엇을 왜 바꿨는지
2. 같이 고친 곳: '함께 고칠 곳' 표에서 확인하고 고친 자리
3. 검증: 실행한 명령과 결과(통과 수), 실행하지 않은 명령과 이유
4. 확인하지 못한 것: 실기기, 다른 OS, 비공개 자료 등
5. 발견했지만 고치지 않은 문제
6. 비공개 짝 저장소와 `_forAI/`에 반영할 내용의 초안

## 비공개 짝 저장소와의 경계

강의 대본, 실습 해답, 평가 자료, 주차 검사 스크립트는 비공개 짝 저장소 `univ_scoring_works/teaching_materials_private/`에 같은 주차 폴더 이름으로 둔다. 그 내용을 이 저장소로 복사하거나 그 안의 파일을 링크하지 않는다. 공개 슬라이드의 구간 제목·분 범위, 실습 문항, 채점 기준을 바꾸면 비공개 자료도 맞춰야 하므로 보고에 적는다. `_forAI/dev_log.md` 기록상 비공개 Android 자료의 12~15주 대본·해답과 시뮬레이터 시험은 2026-11-18 개편 이전 수업(BLE 보드, `sim.py`)을 기준으로 만들어졌다. 새 수업에 맞췄는지는 이 저장소에서 확인할 수 없으므로 보고에 확인 필요로 적는다.
