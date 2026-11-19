# WlEno LAN 제어 실습 도구

WlEno는 Python으로 실행하는 PC 시뮬레이터다. Android 앱은 TCP로 LED와 온습도를 제어하고, VS Code REST Client나 AI 프로그램은 HTTP API로 같은 상태를 읽고 바꾼다. Tkinter 창에는 LED 4개, 내장 LED 깜빡임, 온습도, 입력 버튼과 연결 상태를 표시한다.

Python 3.10 이상을 준비하고 저장소 루트에서 다음 명령을 실행한다. 추가 pip 패키지나 가상환경은 필요 없다.

```powershell
cd tools/wleno
python main.py
```

`python`은 설치된 Python을 실행하는 명령이다. Windows의 Store 실행 별칭만 등록된 경우에는 [준비](#2-준비)의 전체 경로 실행 방법을 따른다. 종료는 창 닫기 또는 `Ctrl+C`다.

| 자료 | 용도 |
|---|---|
| [Android AAR 설치](android/INSTALL.md) | 학생 앱에 통신 라이브러리 추가 |
| [Android 클라이언트 API](android/README.md) | `WlenoClient` 사용법 |
| [RoomControl 연결 실습](../../android_programming/iot_sim/lab.md) | 주소 입력과 연결 점검 |
| [HTTP 실습 예제](examples/README.md) | 연결 확인부터 LED·센서·입력 제어까지 실행하는 `.http` 요청 |
| [AI 제어 도구](../bleuno-control/README.md) | TCP 명령 실행과 상태 검증 |

## 1. 시뮬레이터가 대신하는 것

정규 Android 11~15주차의 RoomControl 앱은 실제 보드 대신 WlEno의 TCP 서버에 연결한다. 장치 이름은 기본 `WlEno_SIM1`이며, 정규 앱은 이름 접두사를 검사하지 않는다. UDP 검색은 선택 기능이고 수업은 IP 직접 연결만으로 진행한다.

| 서비스 | 기본 주소·포트 | 용도 |
|---|---|---|
| TCP | `0.0.0.0:8266` | 명령 한 줄과 JSON 응답·이벤트 한 줄 |
| UDP | `0.0.0.0:8267` | `bleuno?` 장치 검색 |
| HTTP | `127.0.0.1:8080` | API 도움말, 상태 조회, 제어 |

모든 연결과 화면은 보드 상태 하나를 공유한다. TCP 연결·해제는 LED나 센서 상태를 초기화하지 않는다. 상태를 처음 값으로 되돌릴 때는 화면의 초기화 기능 또는 `POST /reset`을 사용한다.

WlEno 프로토콜 버전은 `2.0.0`이다. 정상 `on`·`off`·`pwm`·`dht11`·`about`·`blink`·`stopblk` 명령과 기존 Android 응답 형식을 유지한다. 잘못된 정수·범위·필드는 요청 전체를 거부한다. 실제 BLEuno 보드와 보존 특강의 Fake 클라이언트에는 별도 동작 규칙이 있으므로 [보드 문서](../../android_programming/bleuno/README.md)를 구분해서 읽는다.

## 2. 준비

Python 3.10 이상과 이 폴더의 Python 모듈들이 필요하다. `main.py`가 나머지 모듈을 불러오므로 폴더를 함께 보관한다.

창을 사용하려면 해당 Python에 Tkinter와 Tcl/Tk가 있어야 한다. 실행에 사용할 명령으로 확인한다.

```powershell
python --version
python -m tkinter
```

시험 창이 열리면 닫고 `python main.py`를 실행한다. Windows에서 `python`이 Microsoft Store 안내만 출력하면 설치된 Python의 전체 경로를 사용한다. 아래 경로는 예시이므로 실제 설치 경로로 바꾼다. PowerShell의 `&`는 따옴표로 묶은 실행 파일을 호출한다.

```powershell
& 'C:\Python314\python.exe' --version
& 'C:\Python314\python.exe' -m tkinter
& 'C:\Python314\python.exe' main.py
```

`py` 실행기가 설치되어 있으면 `py main.py`도 사용할 수 있다. macOS·Linux에서는 보통 `python3 main.py`로 실행한다. Tkinter는 선택 표준 모듈이다. Linux 시스템 Python은 버전에 맞는 `python3-tk` 등의 운영체제 패키지가 필요할 수 있으며, `pip install tkinter`로 설치하지 않는다. 화면을 사용하지 않는 `--no-window` 실행에는 Tkinter가 필요 없다.

Windows에서 실행을 검증했다. macOS·Linux 실행은 아직 검증하지 않았다.

## 3. 실행과 끝내기

다음 명령은 `tools/wleno`에서 실행한다. 필요한 명령 하나를 선택한다.

```powershell
python main.py
python main.py --name WlEno_0423
python main.py --no-window
python main.py --no-tcp --no-udp
python main.py --no-http
python main.py --help
```

`--no-tcp --no-udp`는 HTTP와 화면만 사용한다. `--no-http`는 TCP·UDP와 화면을 사용한다. 모든 서비스를 끄고 화면만 실행할 수도 있다. `--no-window`를 사용할 때는 서비스를 하나 이상 활성화한다.

| 옵션 | 기본값 | 의미 |
|---|---|---|
| `--name` | `WlEno_SIM1` | 장치 이름 |
| `--tcp` | `8266` | TCP 명령 포트 |
| `--udp` | `8267` | UDP 검색 포트 |
| `--http` | `8080` | HTTP API 포트 |
| `--bind` | `0.0.0.0` | TCP·UDP 수신 주소 |
| `--http-bind` | `127.0.0.1` | HTTP 수신 주소 |
| `--no-window` | 사용 안 함 | Tkinter 창 없이 실행 |
| `--no-tcp` | 사용 안 함 | TCP 서버 비활성화 |
| `--no-udp` | 사용 안 함 | UDP 서버 비활성화 |
| `--no-http` | 사용 안 함 | HTTP 서버 비활성화 |

포트를 바꾸면 클라이언트 주소도 맞춘다. Android 공통 클라이언트의 선택 UDP 검색은 기본 8267을 사용하므로 UDP 포트를 바꾼 경우에는 IP로 직접 연결한다. 창을 닫거나 실행 터미널에서 `Ctrl+C`를 누르면 활성 서버와 연결을 정리하고 종료한다.

## 4. 코드 구조

실행 진입점은 `main.py` 하나다. 메시지 형식, 보드 상태 전이, 상태 소유권과 통신 처리를 다음과 같이 나눈다.

| 파일 | 책임 |
|---|---|
| [main.py](main.py) | 옵션 처리, 앱 구성, 서비스 시작·종료, Tkinter 화면 |
| [protocol.py](protocol.py) | `WlenoProtocol`: TCP 문법, HTTP 경로·필드, 응답·오류·이벤트·검색 JSON 규약 |
| [simulator.py](simulator.py) | 불변 `State`와 입력에 따른 순수 상태 전이 |
| [session.py](session.py) | 보드 상태 소유, 잠금, 원자적 변경, 입력 이벤트 기록 |
| [tcp.py](tcp.py) | TCP 연결, 줄 송수신, 이벤트 전달 |
| [udp.py](udp.py) | UDP 데이터그램 송수신 |
| [http_api.py](http_api.py) | HTTP 요청·본문 수신과 응답 전송 |

화면과 통신 처리는 세션을 거쳐 상태를 바꾼다. 요청 전체를 검증한 뒤 상태를 반영하므로 `on 0 9`처럼 일부만 유효한 명령도 LED 0을 먼저 바꾸지 않는다. 전송 모듈에서 LED 규칙이나 응답 JSON을 따로 정의하지 않는다.

## 5. 시뮬레이터 화면

LED 0~3은 밝기 `0~255`를 표시한다. `0`은 꺼짐, `255`는 최대 밝기다. 내장 LED의 깜빡임 상태는 `blink`·`stopblk` 명령으로 바꾼다. 온습도 초기값은 `24.5 °C`, `40.0 %`이며 화면이나 HTTP에서 바꾼 값이 다음 `dht11` 응답에 반영된다.

입력 버튼은 값 `0`과 `1`을 번갈아 반영하고 연결된 TCP 클라이언트에 이벤트를 보낸다. 연결 끊기 기능은 연결을 종료하며 보드 상태를 유지한다. 초기화 기능은 LED·깜빡임·센서·입력값을 처음 값으로 되돌린다. 연결 수와 로그는 통신 상태를 확인하는 자료다.

## 6. 앱에서 붙을 주소

| 앱과 WlEno 실행 위치 | 앱 주소 칸 |
|---|---|
| Android 에뮬레이터와 WlEno가 같은 PC | `10.0.2.2:8266` |
| 에뮬레이터와 WlEno가 다른 PC | WlEno PC의 LAN IPv4와 포트, 예: `192.168.0.10:8266` |
| Android 실기기 | WlEno PC의 LAN IPv4와 포트, 예: `192.168.0.10:8266` |

`10.0.2.2`는 Android 에뮬레이터에서 호스트 PC를 가리킨다. 앱의 `127.0.0.1`은 Android 자신이다. `0.0.0.0`은 서버 수신 설정이며 앱에 넣는 목적지 주소가 아니다. LAN 주소는 Windows `ipconfig`에서 현재 사용하는 유선·Wi-Fi 어댑터를 확인한다.

RoomControl의 [시뮬레이터 주소]에 주소를 넣고 [제어 시작]을 누른다. 11주차 1일차는 연결 상태를 확인하고, 2일차부터는 연결 후 제어 화면을 연다. 정규 화면에는 UDP 검색이 필요 없다. 외부 인터넷 접속은 이 LAN 실습의 범위에 포함하지 않는다.

선택 UDP 검색은 `bleuno?`를 보내 이름과 TCP 포트를 받는다. 기존 BLE 특강의 이름 필터를 사용하는 경우에만 `--name ESP32_BLE_0423`처럼 지정한다. TCP가 비활성화되어 응답의 `port`가 `null`이면 TCP 연결 대상이 아니다.

## 7. Windows 방화벽

다른 PC나 Android 실기기에서 연결하려면 WlEno PC의 TCP 8266 인바운드가 허용되어야 한다. UDP 8267은 선택 검색에만 필요하며 HTTP 8080은 기본적으로 이 PC에서만 사용한다.

주소와 실행 상태가 맞는데 접속되지 않을 때 조교가 방화벽 규칙을 확인한다. 수업용 규칙이 필요하면 관리자 PowerShell에서 다음 명령을 실행한다. `LocalSubnet`은 같은 서브넷에서 들어오는 연결로 범위를 제한한다.

```powershell
New-NetFirewallRule -DisplayName "WlEno SIM TCP 8266" -Direction Inbound -Protocol TCP -LocalPort 8266 -RemoteAddress LocalSubnet -Action Allow
```

선택 UDP 검색을 사용할 때만 다음 규칙도 추가한다.

```powershell
New-NetFirewallRule -DisplayName "WlEno SIM UDP 8267" -Direction Inbound -Protocol UDP -LocalPort 8267 -RemoteAddress LocalSubnet -Action Allow
```

수업이 끝나면 이번에 만든 규칙만 삭제한다. UDP 규칙을 만들지 않았다면 둘째 줄은 실행하지 않는다.

```powershell
Remove-NetFirewallRule -DisplayName "WlEno SIM TCP 8266"
Remove-NetFirewallRule -DisplayName "WlEno SIM UDP 8267"
```

학교 관리 PC는 조교·관리자에게 설정을 요청한다. 허용 규칙을 추가해도 명시적인 차단 규칙이나 Wi-Fi AP 격리 때문에 접속되지 않을 수 있다. 이때는 같은 PC에서 WlEno와 에뮬레이터를 실행하고 `10.0.2.2:8266`으로 연결한다.

## 8. 명령과 응답

TCP는 UTF-8 명령 한 줄(`\n`으로 종료)을 받고 JSON 한 줄로 응답한다. 연결 직후 hello 이벤트가 먼저 도착한다. 입력 이벤트는 명령 응답 사이에도 올 수 있으므로 `event` 키가 있는 줄을 구분한다.

| 명령 | 동작 | 성공 응답 |
|---|---|---|
| `on 0`, `on 0 2`, `on -1` | 지정 LED 또는 전체 밝기 255 | `{"result":"ok","ms":"led(s) on"}` |
| `off 0`, `off -1` | 지정 LED 또는 전체 밝기 0 | `{"result":"ok","ms":"led(s) off"}` |
| `pwm 1 128`, `pwm -1 128` | 지정 LED 또는 전체 밝기 설정 | `{"result":"ok","ms":"pwm set"}` |
| `dht11` | 온도와 습도 조회 | `{"result":"ok","value":"[24.5,40.0]"}` |
| `about` | 앱 정보 조회 | `{"result":"ok","app":"WlEno","version":"2.0.0","name":"WlEno_SIM1"}` |
| `blink`, `stopblk` | 내장 LED 깜빡임 시작·중지 | `result: "ok"`, `ms: "led blink"` 또는 `"led stop blink"` |

LED 번호는 정수 `0~3`, 전체 지정은 `-1`이다. 밝기는 정수 `0~255`다. `on abc`, `on 0 9`, `pwm -2 100`, `pwm -1 300`, `pwm 0 127.5`는 오류이며 보드 상태와 리비전은 바뀌지 않는다. 정수가 아닌 값을 `0`으로 대체하거나 범위 밖 밝기를 보정하지 않는다. 명령 이름은 소문자를 사용한다. 빈 줄에는 응답하지 않는다.

`dht11.value`는 JSON 배열이 아닌 문자열이며, 온도와 습도를 소수 첫째 자리까지 표현한다. 기존 Android의 `WlenoMessage.value()`가 이 문자열을 읽는다.

| 이벤트·검색 | 예시 |
|---|---|
| TCP 연결 직후 | `{"event":"hello","name":"WlEno_SIM1","app":"WlEno"}` |
| 입력값 변경 | `{"event":"input","index":0,"value":1,"sequence":1}` |
| UDP 검색, TCP 활성 | `{"name":"WlEno_SIM1","port":8266}` |
| UDP 검색, TCP 비활성 | `{"name":"WlEno_SIM1","port":null,"services":{"tcp":null,"http":8080}}` |

입력 이벤트의 `sequence`는 세션의 입력 변경 순서이며 초기화해도 0으로 돌아가지 않는다. 앱이 연결되지 않은 동안에도 입력값과 순서는 유지된다. 초기화할 때 입력값이 `1`이었다면 `value: 0` 이벤트가 발생한다. TCP 비활성 상태에서 HTTP도 꺼져 있으면 UDP 응답의 `services.http`도 `null`이다.

## 9. 수업에서 여럿이 쓸 때

학생 한 명당 자기 PC에서 WlEno 한 개를 실행한다. 이름을 구분하려면 `python main.py --name WlEno_0423`처럼 학번 뒤 네 자리를 붙인다. 같은 번호가 있으면 이니셜을 덧붙인다. 여러 앱이 한 WlEno에 연결하면 같은 보드 상태를 함께 바꾸므로 창 제목과 로그에서 접속 대상을 확인한다.

HTTP는 기본 `127.0.0.1` 바인드를 유지한다. `--http-bind 0.0.0.0`으로 바꾸면 LAN의 다른 프로그램도 HTTP 제어 요청을 보낼 수 있다. Android TCP 연결을 위해 HTTP 바인드를 바꿀 필요는 없다.

## 10. 막혔을 때

| 증상 | 확인 |
|---|---|
| `python` 실행 시 Microsoft Store 안내 | 설치된 Python 전체 경로 사용. `py`가 설치되었다면 `py --version` 확인 |
| `can't open file ...main.py` | 현재 폴더가 `tools/wleno`인지 확인 |
| `No module named tkinter` 또는 Tcl/Tk 오류 | 같은 Python의 `-m tkinter` 확인. 화면이 필요 없으면 `--no-window` 사용 |
| 포트 사용 중 오류 | 이미 실행 중인 WlEno 확인. 다른 프로그램의 포트라면 `--tcp`, `--udp`, `--http`로 변경 |
| 앱이 연결되지 않음 | `--no-tcp` 여부, 실행 위치별 주소, TCP 포트, 방화벽 확인 |
| 다른 PC·실기기만 연결되지 않음 | LAN 통신·AP 격리·TCP 인바운드 확인 |
| HTTP 요청이 연결 거부됨 | `--no-http` 여부, HTTP 포트, `.http` 파일의 `@baseUrl` 확인 |
| HTTP 400 | JSON 형식, 필드 이름, 숫자·불리언 타입과 범위 확인 |
| TCP 응답은 성공인데 예상한 LED가 아님 | 접속한 PC·포트와 LED 번호 확인. 자기 WlEno 로그와 대조 |

연결·해제는 보드 초기화 조건이 아니다. LED가 바뀌었다면 다른 연결의 명령, 화면 조작이나 HTTP 제어·초기화 기록을 확인한다.

## 11. 다른 프로그램에서 쓰기

HTTP는 JSON API다. [REST Client 예제](examples/README.md)는 연결·도움말 확인부터 제어까지 순서대로 실행할 수 있다. POST JSON 본문에는 `Content-Type: application/json`, 응답 선택에는 `Accept: application/json`을 사용한다.

| 요청 | JSON 본문 | 정상 상태·응답 |
|---|---|---|
| `GET /info` | 없음 | 200, `app`·`version`·`name`·`endpoints`·`services` |
| `GET /state` | 없음 | 200, 보드 상태와 실행 정보 |
| `POST /leds` | `{"indices":[0,1],"brightness":128}` | 200, `result: "ok"`와 `revision` |
| `POST /blink` | `{"enabled":true}` | 200, `result: "ok"`와 `revision` |
| `POST /set` | `{"temperature":30.5,"humidity":55}` | 200, `result: "ok"`와 `revision`. 온도·습도 중 하나만 보내도 됨 |
| `POST /input` | 빈 본문 또는 `{}` | 200, `{"result":"ok","value":1,"sequence":1,"revision":1}`. 숫자는 당시 상태에 따라 달라짐 |
| `POST /reset` | 빈 본문 또는 `{}` | 200, `result: "ok"`와 `revision`. LED·깜빡임·온습도·입력값 초기화 |
| `POST /drop` | 빈 본문 또는 `{}` | 연결 종료를 요청했으면 202, `{"result":"ok","requested":1}`. 대상이 없으면 200, `requested: 0` |

HTTP의 `indices`는 `0~3` 정수 배열이다. 전체 LED를 지정할 때는 `[0,1,2,3]`을 사용한다. `-1`은 TCP 명령에만 있는 전체 지정 표현이다.

`GET /state`는 `leds`, `blink`, `temperature`, `humidity`, `input_value`, `revision`, `input_sequence`와 실행 정보 `clients`, `log`, `services`를 반환한다. `revision`은 성공한 상태 변경 요청마다 1씩 증가하며 같은 값을 다시 설정해도 증가한다. 조회·연결·해제·거부된 요청으로는 증가하지 않는다. `input_sequence`는 입력 이벤트가 발생할 때만 증가한다.

`POST /input`의 200 응답은 실제 입력값 반영이 끝났음을 뜻한다. 반환된 값·순서·리비전으로 직후 상태를 대조한다. `POST /drop`의 202는 연결 종료 요청을 받았다는 뜻이므로 `GET /state`의 `clients`가 0이 되는지 확인한다. TCP가 꺼져 있거나 연결이 없으면 종료 요청 수는 0이다.

존재하지 않는 경로는 404, 해당 경로에서 허용하지 않는 메서드는 405, 잘못된 JSON·필드·타입·범위는 400이다. 오류 응답은 `result: "err"`와 원인을 설명하는 `ms`를 갖는다. 센서 값에는 유한한 JSON 숫자를 사용한다. 문자열 숫자, 불리언, NaN, Infinity는 허용하지 않는다. HTTP 전송 계층은 본문 크기 64 KiB 제한과 읽기 시간 제한을 적용한다.

화면 없이 HTTP만 검증하려면 다음 명령을 사용한다.

```powershell
python main.py --no-window --no-tcp --no-udp
```

## 개발 검증

`tools/wleno`에서 다음 명령으로 상태 전이, 프로토콜, 통신과 앱 통합 테스트를 실행한다.

```powershell
python -m unittest discover -s tests -v
```

실제 Tk 창을 사용하는 테스트는 디스플레이와 해당 Python의 Tkinter·Tcl/Tk가 있어야 수행한다. 실행 검증 환경은 Windows이며 macOS·Linux는 아직 검증하지 않았다.
