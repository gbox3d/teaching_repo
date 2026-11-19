# WlEno HTTP 실습

VS Code REST Client 확장(`humao.rest-client`)으로 WlEno의 HTTP API를 실행한다. 연결과 API 도움말을 먼저 확인한 뒤 LED, 센서, 입력, 초기화·연결 종료를 차례로 다룬다.

## 실행 준비

저장소 루트의 터미널에서 다음 명령을 실행한다. 설치된 Python 명령과 Tkinter 준비는 [WlEno 실행 안내](../README.md#2-준비)를 따른다.

```powershell
cd tools/wleno
python main.py
```

창이 필요 없으면 `python main.py --no-window`를 사용한다. HTTP만 사용하려면 `--no-tcp --no-udp`를 추가한다. HTTP 실습 중에는 `--no-http`를 사용하지 않는다.

각 `.http` 파일 맨 위의 `@baseUrl = http://127.0.0.1:8080`을 확인한다. `--http 8081`로 실행했다면 값을 `http://127.0.0.1:8081`로 바꾼다. VS Code와 WlEno를 같은 PC에서 실행하는 구성이 기본이다.

## 요청 실행과 응답 확인

VS Code에서 `.http` 파일을 열고 원하는 요청 바로 위의 **Send Request**를 누른다. `###`가 요청을 나누므로 위에서 아래로 한 요청씩 실행한다. 응답 창의 HTTP 상태 코드와 JSON 본문을 함께 확인한다.

모든 요청에 `Accept: application/json`을 넣었다. JSON을 보내는 POST 요청에는 `Content-Type: application/json`도 넣었다. `/input`, `/reset`, `/drop`의 `{}`는 추가 필드가 없는 JSON 객체이며 빈 본문으로 보내도 된다. 이 로컬 실습 API에는 인증 정보가 필요 없다. 실제 자격 증명을 요청 파일에 넣지 않는다.

| 순서 | 파일 | 확인할 결과 |
|---|---|---|
| 01 | [연결·도움말](01_connection/requests.http) | 200, `app: "WlEno"`, `version: "2.0.0"`, API 경로·현재 상태 |
| 02 | [LED·깜빡임](02_leds/requests.http) | 200, `result: "ok"`; 상태의 LED 밝기와 `blink` 확인 |
| 03 | [센서](03_sensors/requests.http) | 200, 설정한 온도·습도 확인; 문자열 숫자는 400 |
| 04 | [입력](04_input/requests.http) | 200, 반영된 `value`·`sequence`·`revision`과 직후 상태 일치 |
| 05 | [초기화·연결 종료](05_reset_drop/requests.http) | 초기화 200; 연결 종료 대상이 있으면 202, 없으면 200 |

`revision`은 성공한 상태 변경 요청마다 증가한다. 같은 값으로 설정해도 증가하며, 400 오류 요청과 조회·연결 종료 요청은 바꾸지 않는다. `input_sequence`는 입력 이벤트에만 증가한다. 화면이나 다른 앱도 같은 상태를 변경하므로 숫자 자체를 고정값으로 비교하지 않고 전후 차이를 확인한다.

오류 예제는 의도적으로 잘못된 요청을 보낸다. 400은 JSON·필드·값 검증 오류, 404는 없는 경로, 405는 해당 경로의 메서드 오류다. 오류 예제 전후 `GET /state`를 실행하면 거부된 요청이 보드 상태와 리비전을 바꾸지 않았는지 확인할 수 있다.

`POST /drop`은 TCP 연결 종료 요청이다. 연결된 앱이 있을 때 202와 양수 `requested`를 받은 뒤 `GET /state`의 `clients: 0`을 확인한다. 종료 완료를 기다리지 않는 응답이므로 필요하면 상태 조회를 한 번 더 실행한다. 연결이 없거나 TCP가 꺼져 있으면 200과 `requested: 0`이다. LED·센서 상태는 유지된다.
