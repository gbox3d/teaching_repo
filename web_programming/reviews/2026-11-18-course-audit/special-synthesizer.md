# 신시사이저 특강 조사·수정 결과

담당: `special_synthesizer_owner` · 검증일: 2026-11-18 · 소스 범위: `web_programming/specials/synthesizer/`

정규 12주차 fetch·JSON 이후의 선택 보강·방학 연구로 정리했습니다. 정규 시험에서 제외하고 시간 제한을 두지 않습니다. 코드와 문서 수정, 실제 Chrome 검증을 완료했습니다. 최종 통합 점수는 별도 평가자가 판정합니다.

## 수정 내용

| 발견 사항 | 수정 결과 |
|---|---|
| 비교 9개·연주기 6파일·멜로디 없음이라는 원고와 실제 파일 불일치 | 비교 10개, 연주기 7개·조합기 포함 실행 파일 9개로 정정. ex10·compose·song.js와 멜로디 포함을 반영 |
| walkthrough의 오래된 코드 전문과 행번호 | 실행 소스 링크·함수명·실제 변경 인수 중심으로 교체. 중복 전문 제거 |
| 일부 HTML의 긴 설명과 해라체 | README·사용 안내로 설명 이동. 화면은 조작·결과·짧은 상태 문구로 정리 |
| 비교 화면 스타일 분산, 375px에서 6화면 넘침 | `shared/examples.css` 추가, 캔버스·표·리듬 영역과 build의 16칸·파일 입력 반응형 수정 |
| 연주기의 늦은 JSON 응답이 최신 선택을 덮음 | 요청 번호로 마지막 요청만 반영. 실패도 해당 요청에만 반영 |
| 연주기 정지 뒤 이미 예약한 긴 음의 출력 지속 | 연주별 GainNode를 추가하고 정지 시 감쇠 후 연결 해제. RAF 취소·resume 대기 취소 |
| 연주기가 melody 데이터 형식을 검사하지 않음 | 기존 공용 `songToBars`를 재사용. JSON·코드·BPM 검사 후 재생 허용 |
| 조합기 초기 fetch가 사용자 파일을 덮음 | 파일·fetch를 같은 요청 순서로 관리하고 마지막 요청만 반영 |
| MIDI 옮김 결과가 0~127을 벗어나 저장 후 다시 읽을 수 없음 | 공용 transpose에서 범위 검사. 유효하지 않은 입력은 기존 값으로 복원 |
| ex07 무효 BPM·중복 실행, 예약 간격을 실측처럼 설명 | 범위 검사·실행 중 잠금. 호출 시각/예약 시각/실제 출력 구분 |
| ex09 HTTP 실패를 JSON 파싱으로만 처리 | `response.ok`, 이전 표 초기화, 버튼 복구 추가 |
| ex10 예약된 멜로디를 즉시 멈출 수 없음 | 정지 버튼 추가 |
| 정적 JSON 요청을 직접 비교할 자료 없음 | `requests.http`에 연결 확인·정상 데이터·404 요청. REST CRUD API와 구분 |
| score JSON이 연주기에 직접 맞지 않음 | 별도 README로 스키마 차이와 자동 변환 미구현 명시 |

기존 flat 예제·build 파일 경로는 보존했습니다. W3.CSS는 이 특강에 도입하지 않았으며 기존의 오디오 화면을 유지했습니다. 실제 키·비밀번호·환경 파일을 추가하거나 읽지 않았습니다.

## 실제 브라우저 검증

Chrome **157.0.8103.38**, Playwright, `http://localhost:8111/specials/synthesizer/examples/`에서 실행했습니다. AudioContext·오디오 노드는 브라우저의 실제 구현을 사용했습니다. 관찰 래퍼는 start/stop·연결 해제 호출을 기록하며 원래 메서드를 실행합니다.

| 항목 | 관찰 결과 |
|---|---|
| ex01~ex10·연주기·조합기 12화면 × 375/1280px | 24경우 모두 문서 가로넘침 0 |
| ex01 버튼 4개 | 오실레이터 시작 4회, AudioContext running |
| ex02 버튼 11개 | 오실레이터 시작 11회, 마지막 C5 523.3Hz 표시 |
| ex03 버튼 5개 | 오실레이터 시작 5회, 오류 없음 |
| ex04 버튼 9개 | 오실레이터 시작 27회, 오류 없음 |
| ex05 버튼 6개 | 오실레이터 시작 6회, 오류 없음 |
| ex06 버튼 6개 | oscillator/buffer source 시작 7회, 오류 없음 |
| ex07 BPM 0 | 오디오 시작 0회, 입력 검사로 차단 |
| ex07 109 BPM 예약 | 16회 시작, 15개 예약 간격 모두 반올림 138ms, 중복 시작 비활성 |
| ex07 CPU 부하 + 콜백 | 해당 실행에서 139~200ms. 환경 의존 관찰값이며 기준값으로 고정하지 않음 |
| ex08 | 비우기·록·디스코, 체크 변경, 재생·정지 동작 |
| ex09 | 정상 200 → 주입한 404에서 표 비움 → 정상 200 복구 |
| ex10 | 모드별 30음, 총 90회 시작. 모드 전환과 명시적 정지에 따른 stop 호출 총 180회 |
| 연주기 | 28마디 로드, 재생·정지 3회, 출력 GainNode 연결 해제 3회 |
| 연주기 요청 경쟁 | 450ms 지연한 이전 곡 응답이 최신 Only You를 덮지 않음 |
| 연주기 늦은 오류 | 400ms 지연한 이전 요청 404가 최신 성공 곡의 28마디를 지우지 않음 |
| 연주기 JSON 실패 | 문법 오류에서 악보 비움·재생 비활성, 정상 곡으로 복구 |
| 조합기 편집 | 잘못된 코드 C로 복원, MIDI 126에 +2 거부·0 복원, -2 적용 |
| 조합기 마디 | 2→3마디 복제, 좌우 이동, 삭제 후 2마디 |
| 조합기 JSON 왕복 | 다운로드 JSON의 MIDI 124 확인, 다시 열기 성공 |
| 조합기 잘못된 파일 | 기존 2마디·제목 유지 |
| 조합기 재생·정지 | 3회, 출력 GainNode 연결 해제 3회 |
| 조합기 초기 로드 경쟁 | 500ms 지연 초기 곡보다 사용자가 연 파일의 2마디·제목 유지 |
| resume 대기 중 정지 | 실제 resume 뒤 반환을 200ms 지연. 두 앱 모두 정지 후 오실레이터 예약 0 |
| JavaScript pageerror | 전체 검사 0건 |

375px 스크린샷 4개를 직접 확인했습니다. ex08은 표 내부 가로 스크롤을 사용하며 문서 전체는 넘치지 않습니다. ex03은 표 셀 안에서 줄바꿈합니다.

## 정적 검사와 데이터 정합

- 기존 29파일 전부 조사, 새 안내 2개·공용 CSS·HTTP 요청을 더해 최종 **33파일**입니다.
- build JavaScript 4개 및 HTML의 인라인/모듈 스크립트 14개, 총 **18개** `node --check` 통과입니다.
- 로컬 Markdown 링크의 대상 파일 누락 **0건**입니다. fragment 전수 자동 검사는 이 검사에 포함하지 않았으며 슬라이드가 참조하는 `lab.md#실습-60분`은 보존했습니다.
- JSON 6개 모두 파싱했습니다. ex09는 2구간 6마디, my_song은 2구간 8마디, only_you는 4구간 28마디·136음입니다. score 3개는 `score` 기반의 별도 스키마로 실행기에서 사용하지 않습니다.
- KO/EN 슬라이드 각각 **16장**을 보존했습니다. 비교 개수·실행 파일·멜로디·행번호·시간 측정 설명을 갱신했습니다. 슬라이드 최종 빌드와 넘침 검사는 총괄의 통합 검사 대상입니다.
- `check_ui_copy.mjs`, `check_doc_style.py` 모두 종료 코드 0, 경고 출력 없음입니다.
- `.http`와 같은 세 요청을 실제 HTTP로 실행했습니다. `ex09_song.json`, `build/my_song.json`은 200/application-json, `missing-song.json`은 404/text-html입니다. VS Code 확장 UI의 Send Request 클릭 자체는 실행하지 않았습니다.

## 전체 파일 목록

| 분류 | 조사 파일 |
|---|---|
| 특강 문서 5 | `README.md`, `lab.md`, `walkthrough.md`, `slides.md`, `slides_en.md` |
| 예제 안내·요청·CSS 3 | `examples/README.md`, `examples/requests.http`, `examples/shared/examples.css` |
| 소리 예제 6 | `examples/ex01_wave.html`, `ex02_pitch.html`, `ex03_envelope.html`, `ex04_chord.html`, `ex05_filter.html`, `ex06_drums.html` |
| 시간·데이터 예제 5 | `examples/ex07_timing.html`, `ex08_pattern.html`, `ex09_fetch_song.html`, `ex09_song.json`, `ex10_melody.html` |
| build 10 | `examples/build/index.html`, `index.js`, `compose.html`, `compose.js`, `main.css`, `synth.js`, `song.js`, `only_you.json`, `my_song.json`, `README.md` |
| 참고 악보 4 | `score/README.md`, `hyunjinyoung_sexy_woman_quantized_score.json`, `kiiikiii_pop_off_pop_off_full_melody_score.json`, `savage_only_you_full_score.json` |

## 증거와 재현

- [브라우저 검사 스크립트](evidence/synth-browser-check.mjs) · [실행 결과](evidence/synth-browser-result.json)
- [요청 경쟁·resume·HTTP 경계 검사](evidence/synth-edge-check.mjs) · [실행 결과](evidence/synth-edge-result.json)
- [소스 문법·로컬 링크·전체 목록 검사](evidence/synth-source-check.mjs)
- 375px 화면: [ex03](evidence/synth-envelope-375.png), [ex08](evidence/synth-pattern-375.png), [연주기](evidence/synth-player-375.png), [조합기](evidence/synth-composer-375.png)

스크립트는 이 작업 환경의 Playwright 모듈 절대 경로와 8111 서버를 사용합니다. 다른 PC에서는 해당 두 경로를 바꿉니다. 검사 중 잘못된 응답·지연은 Playwright route로 브라우저 세션에만 주입하며 소스 JSON을 변경하지 않습니다.

## 검증하지 않은 범위

스피커·이어폰으로 **소리를 직접 듣지는 않았습니다**. 실제 오디오 노드 생성·running·예약 시각·정지 연결 해제만 확인했습니다. 음질·청감·하드웨어 지연을 검증 완료로 표시하지 않습니다.

GitHub Pages의 공개 배포, OS별 오디오 장치, Safari·Firefox, 실제 교실 동시 재생은 이 담당 검사의 범위 밖입니다. 참고 악보의 음악적 정확도나 재배포 권한도 판정하지 않았습니다. score 원본은 변경하지 않았고 파일 형식과 파싱만 확인했습니다.
