# 신시사이저 예제 안내

[특강 안내](../README.md)의 서버 명령으로 이 폴더를 연 뒤 ex01부터 진행합니다. 비교할 때는 같은 음량으로 듣고, 예상한 차이와 관찰한 차이를 별도로 적습니다. 화면에는 조작과 결과만 두며 설명은 이 문서에서 읽습니다.

## 소리 비교

| 예제 | 조작과 관찰 | 코드에서 바꿀 곳 |
|---|---|---|
| [ex01 파형](ex01_wave.html) | 같은 220Hz·1초·gain 0.2에서 네 파형 비교. 첫 클릭 뒤 AudioContext `running`과 파형 확인 | `play`의 `osc.type`, `frequency.value`, `amp.gain.value` |
| [ex02 높이](ex02_pitch.html) | A3 220.0Hz, A4 440.0Hz, A5 880.0Hz. C4~C5의 MIDI 번호 비교 | `midiToFreq`의 기준 440, 버튼 `data-midi` |
| [ex03 엔벨로프](ex03_envelope.html) | 같은 220Hz에서 5가지 크기 변화. 2번과 5번은 같은 시간, 다른 보간 곡선 | `play(attack, hold, release, curve)` 호출 인수 |
| [ex04 화음](ex04_chord.html) | Am은 57·60·64, C는 60·64·67, Cm은 60·63·67. 가운데 음 비교 | `SHAPES`의 장 `[0,4,7]`과 단 `[0,3,7]` |
| [ex05 필터](ex05_filter.html) | sawtooth 220Hz에서 cutoff 20000→3000→800→200. Q 15·주파수 이동 비교 | `playThrough`, 버튼 `data-cutoff`, `sweep` 처리 |
| [ex06 드럼](ex06_drums.html) | 킥의 고정/하강 주파수, 스네어의 잡음/톤, 하이햇의 짧은/긴 감쇠 비교 | `kick`, `snare`, `hat`의 주파수·decay |

ex01의 그림은 출력 파형입니다. ex03의 그림은 코드가 그린 크기 변화 곡선이며 마이크 측정치가 아닙니다. ex05의 그림은 왼쪽이 저주파, 오른쪽이 고주파인 주파수 성분입니다. cutoff 20000Hz도 필터를 거치며 '필터 없음'과 완전히 같지는 않습니다.

`exponentialRampToValueAtTime`의 목표값에는 0을 넣지 않습니다. 예제는 0.0001까지 낮춘 뒤 오실레이터를 종료합니다. 음색·크기의 체감은 이어폰과 청취 환경에 따라 달라집니다.

## 시간과 리듬

[ex07](ex07_timing.html)은 BPM 60~180을 입력받습니다. 109 BPM에서 한 박은 약 0.550초, 16분음표는 약 0.138초입니다.

1. `setTimeout` 실행 뒤 간격을 기록합니다. 출력은 콜백이 확인한 `ctx.currentTime` 간격입니다.
2. 오디오 예약 실행 뒤 간격을 기록합니다. 출력은 `start(time)`에 전달한 **예약 시각** 간격입니다.
3. CPU 부하를 켜고 반복합니다. 0.1초마다 0.06초 동안 메인 스레드를 점유합니다.

두 출력은 측정 대상이 다릅니다. 2번의 138ms 표시는 실제 스피커 출력 간격 측정이 아닙니다. 예약에 쓸 시간보다 메인 스레드 지연이 길면 소리도 늦을 수 있습니다. 실행 중에는 중복 시작과 BPM 변경을 막습니다.

[ex08](ex08_pattern.html)은 네 줄 × 16칸입니다. 디스코·록·비우기를 비교한 뒤 체크 하나를 바꿉니다. 아래 배열과 다음 반복의 해당 음이 바뀌는지 확인합니다. 좁은 화면에서는 리듬 표 안에서 가로로 스크롤합니다. 정지는 새 예약을 멈추며 이미 시작한 짧은 음의 감쇠는 남을 수 있습니다.

## JSON 연결 확인

[ex09](ex09_fetch_song.html)에서 불러오기를 누르면 다음 값이 표시됩니다.

| 식 | 값 |
|---|---|
| `song.track_info.title` | 연습곡 |
| `song.track_info.bpm` | 109 |
| `song.sections.length` | 2 |
| `song.sections[0].section` | A |
| 첫 마디 `chord` | Am |
| 두 번째 구간 마디 수 | 2 |

펼친 결과는 `A:Am A:F A:C A:G B:Dm B:Am`입니다. 잘못된 파일명은 HTTP 404, 잘못된 JSON은 파싱 오류로 나타납니다. 실패 후 이전 표는 비워지고 버튼을 다시 사용할 수 있습니다.

### VS Code REST Client

1. `humao.rest-client` 확장을 설치하고 [requests.http](requests.http)를 엽니다.
2. `@baseUrl`을 예제 폴더의 서버 주소로 지정합니다. 기본값은 `http://localhost:8000`입니다. 저장소 전체를 서버로 열었다면 예제 폴더 경로도 덧붙입니다.
3. 각 요청 위의 **Send Request**를 누릅니다. 인증·필수 헤더는 없으며 `Accept: application/json`은 원하는 응답 형식을 표시합니다.
4. 정상 두 요청은 200과 JSON, 없는 파일 요청은 404를 확인합니다. 404 응답은 HTML일 수 있습니다.

이 요청들은 **정적 JSON 파일 GET**입니다. 방명록 REST API가 아니므로 `/about`·`/help`·CRUD 주소를 만들지 않습니다. 키나 비밀번호도 넣지 않습니다.

## 멜로디와 조합기

[ex10](ex10_melody.html)은 같은 음 높이에서 시작 칸과 길이를 바꿉니다. 첫 이끔 마디를 포함한 9마디를 비교하며 세 버튼 모두 같은 30개 음을 사용합니다. 1번은 원래 시작·길이, 2번은 길이만 1칸, 3번은 순서대로 2칸 간격입니다. 정지 버튼은 예약된 음도 취소합니다.

`step`은 1~16, `midi`는 0~127, `duration_steps`는 1~64의 정수입니다. 화면의 결과는 두 번째 마디 음의 계산된 시작·종료 시각이며, 캔버스의 가로는 시간·세로는 MIDI 높이입니다.

[조합기 사용 안내](build/README.md)에서 마디 선택·복제·이동·삭제·옮김·JSON 왕복을 이어갑니다.

## 조립표

| 비교 예제 | 실제 연주기 소스 |
|---|---|
| ex01~ex05 | [synth.js](build/synth.js)의 `playTone`, `midiToFreq`, `chordToMidis` |
| ex06 | [synth.js](build/synth.js)의 `createNoise`, `playKick`, `playSnare`, `playHat` |
| ex07 | [index.js](build/index.js)의 `secondsPerStep`, `tick`, `scheduleStep` |
| ex08 | [index.js](build/index.js)의 `PATTERNS`와 `ROWS` |
| ex09 | [index.js](build/index.js)의 `loadSong`, [song.js](build/song.js)의 `songToBars` |
| ex10 | `scheduleStep`의 멜로디 처리, [compose.js](build/compose.js)의 편곡 |

실행 소스가 기준입니다. 원고에 전문을 다시 복사하거나 변하는 행번호를 붙이지 않습니다.
