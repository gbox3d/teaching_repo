# 신시사이저 따라하기

정규 12주차 이후 선택하는 연구 실습입니다. [예제 안내](examples/README.md)에서 소리 부품을 비교한 다음 진행합니다. 필요한 만큼 시간을 사용합니다.

## 1. web-synth 폴더와 서버

저장소 루트에서 다음 명령으로 모든 비교 예제를 엽니다.

```powershell
node web_programming/tools/static-server/server.mjs web_programming/specials/synthesizer/examples 8000
```

브라우저 주소는 `http://localhost:8000/`입니다. `ex01_wave.html`부터 `ex09_fetch_song.html`까지 실행합니다. ex09의 JSON을 [REST Client 요청](examples/requests.http)으로도 받아 봅니다. JSON은 정적 파일이며 Supabase 연결을 사용하지 않습니다.

## 2. 연주기 폴더와 재생

`examples/build` 전체를 자기 작업 폴더 `web-synth`로 복사합니다. 실행 파일 9개와 사용 안내가 포함됩니다. 특히 `song.js`가 빠지면 ES 모듈을 불러오지 못합니다.

기존 서버를 종료한 뒤 저장소 루트에서 아래 명령의 경로를 자기 폴더로 바꿉니다.

```powershell
node web_programming/tools/static-server/server.mjs C:/Users/student01/web-synth 8000
```

`http://localhost:8000/`에서 첫 곡의 28마디가 보이는지 확인합니다. 재생 후 마디와 16칸 표시가 움직이고, 정지 후 표시가 멈춰야 합니다. 곡을 `my_song.json`으로 바꾸면 8마디와 제목 `내 노래`가 표시됩니다.

## 3. 실제 소스 읽기

| 소스 | 먼저 읽을 함수·데이터 | 연결할 예제 |
|---|---|---|
| [synth.js](examples/build/synth.js) | `midiToFreq`, `chordToMidis`, `playTone`, 드럼 함수 | ex01~ex06 |
| [index.js](examples/build/index.js) | `PATTERNS`, `scheduleStep`, `tick`, `loadSong`, `stop` | ex07~ex10 |
| [song.js](examples/build/song.js) | `songToBars`, `transpose`, `barsToSong` | JSON 검사와 변환 |
| [compose.js](examples/build/compose.js) | `setupEditor`, `useSong`, `exportSong` | 편집과 저장 |

오디오 노드는 JavaScript 모듈에서 만듭니다. `main.css`는 두 화면의 모양을 정합니다. 실행 파일이 항상 전문의 기준이며 이 문서에 중복된 전문이나 고정 행번호를 두지 않습니다.

## 4. my_song.json 고치기

1. `track_info.title`을 자기 제목으로 바꾸고 `bpm`을 118에서 124로 바꿉니다.
2. `sections`의 한 마디 `chord`를 `C`에서 `Am`으로 바꿉니다. 실제 파일에서 해당 마디를 먼저 찾습니다.
3. 저장 후 새로고침하고 `my_song.json`을 선택합니다. 제목·재생 BPM·마디 코드를 확인합니다.
4. 쉼표를 지워 JSON 오류를 만들었다가 복구합니다. 실패 때 재생 버튼이 막히고, 복구 후 다시 재생되는지 확인합니다.

JSON의 따옴표·쉼표 오류와 코드 이름 오류를 구분합니다. 멜로디 없는 마디는 `melody`를 생략합니다. 공개 결과물에는 직접 만든 진행·멜로디 또는 사용 권한이 있는 자료를 사용합니다.

## 5. 리듬 배열 고치기

`index.js`의 `PATTERNS.disco.kick`에서 두 번째 박인 5번째 원소를 1에서 0으로 바꿉니다. 배열 인덱스는 4입니다. 저장하고 새로고침한 뒤 디스코와 록을 비교합니다. 원소 수는 16을 유지합니다.

연주기의 bass 배열은 0(쉬기), 1(낮은 근음), 2(한 옥타브 위)입니다. 다른 리듬 줄은 0/1로 연습합니다. `checkPattern`은 줄 존재와 길이를 검사하며 모든 음악적 오류를 판단하지는 않습니다.

## 6. 소리 하나 고치기

`playTone`의 호출 인수 중 하나만 바꿉니다. 예를 들어 `scheduleStep`의 코드 층 `release: 0.15`를 `0.3`으로 바꾸고 종료 뒤의 감쇠를 비교합니다. `synth.js` 기본값보다 호출자가 준 값이 우선하므로 **실제 호출 인수**를 찾습니다.

BPM을 109에서 124로 바꾸면 한 칸의 길이는 `60 / BPM / 4`에 따라 짧아집니다. 길이·높이·음량을 동시에 바꾸지 말고 먼저 하나의 변수로 차이를 확인합니다.

## 7. 멜로디 조합과 JSON 왕복

[ex10](examples/ex10_melody.html)의 세 가지 예약 규칙을 비교한 뒤 [조합기](examples/build/compose.html)를 엽니다. 라이브러리 이름으로 미리 듣고, `+`로 편곡에 추가합니다. 한 마디를 복제·이동·삭제하고 옮김을 +2로 바꿉니다.

내보낸 JSON을 `내 파일로 열기`로 다시 엽니다. 제목·마디 순서·음 높이가 유지되는지 확인합니다. 잘못된 JSON을 열어 현재 편곡이 보존되는지도 확인합니다. `score/` JSON은 형식이 달라 직접 열 수 없습니다.

## 8. 공개와 연구 기록

GitHub Pages에는 `web-synth` 안의 실행 파일을 함께 올립니다. `index.html`이 게시 루트에 있으면 주소는 `https://사용자명.github.io/web-synth/`입니다. 하위 폴더에 올렸다면 그 경로를 덧붙입니다. 로컬 파일의 `.env`나 비밀번호는 필요하지 않습니다.

공개 주소에서 새로고침하고 모든 JS·CSS·JSON 요청이 200인지 확인합니다. 제목·BPM·변경한 마디를 포함한 캡처와 변경 전후 코드를 연구 기록에 남깁니다. 화면 캡처는 소리 검증을 대신하지 않으므로 학생은 이어폰으로 청취한 관찰을 별도로 적습니다.
