# 12주차 따라하기 · 책상 조명과 침대 조명

RoomControl은 11주차부터 시작한 독립 앱이다. 새 Empty Views Activity에서 시작한다. 연결 화면과 설치한 WlEno AAR은 유지하고 `ControlActivity.kt`, `activity_control.xml`을 수정한다.

## 1일차

### 1. 내 방 제어 화면 열기

저장소의 `tools/wleno`에서 `uv run main`을 실행한다. 앱의 연결 화면에서 에뮬레이터 주소 `10.0.2.2:8266`을 입력하고 [제어 시작]을 누른다. 휴대전화는 PC의 LAN IPv4를 사용한다. 제어 화면이 열리면 준비가 끝난다.

### 2. 조명 선택 UI 배치

[1일차 레이아웃](examples/day1/activity_control.xml)의 `lampGroup` RadioGroup을 확인한다. 안에 `deskRadio`, `bedRadio` 두 RadioButton이 있다. 글자는 `책상 조명 · LED 0`, `침대 조명 · LED 1`이다. 기본 선택은 책상 조명이다.

화면에서 두 항목 중 하나만 선택되는지 먼저 확인한다. 사용자는 방의 조명 이름을 선택한다. 코드에서 그 선택을 시뮬레이터 LED 번호로 바꾼다.

### 3. 선택을 LED 번호로 바꾸기

[1일차 ControlActivity](examples/day1/ControlActivity.kt)에 다음 함수를 넣는다.

```kotlin
private fun selectedLamp(): Int {
    return if (binding.deskRadio.isChecked) 0 else 1
}
```

책상 조명이 선택되어 있으면 0, 침대 조명이면 1을 돌려준다. 이 두 값이 WlEno 창의 첫 번째와 두 번째 LED에 대응한다.

### 4. 켜기·끄기 버튼 연결

```kotlin
binding.onButton.setOnClickListener { send("on ${selectedLamp()}") }
binding.offButton.setOnClickListener { send("off ${selectedLamp()}") }
```

책상 조명이 선택되어 있으면 `on 0`, 침대 조명이 선택되어 있으면 `on 1`을 보낸다. `send()`와 클라이언트는 제공 코드를 사용한다. 줄바꿈은 클라이언트가 붙이므로 학생 코드에 추가하지 않는다.

### 5. 조명과 결과 확인

책상 조명을 켜고 이어서 침대 조명을 켠다. WlEno 창에서 첫 번째와 두 번째 원이 켜진다. 책상 조명만 끄면 침대 조명은 켜진 채로 남는다.

응답은 다음 모양이다. 화면 아래 작은 글자에서 전송과 수신을 확인한다.

```json
{"result":"ok","ms":"led(s) on"}
```

`onMessage`에서 `WlenoMessage.result(line)`가 `ok`이면 큰 결과 글자에 `조명 설정 완료`를 표시한다. 버튼을 누른 직후에는 `응답 대기 중`이다. 결과 표시 코드는 제공 예제에서 읽고 확인한다.

## 2일차

### 6. 밝기 슬라이더 배치

[2일차 레이아웃](examples/day2/activity_control.xml)에 있는 `brightnessBar` SeekBar, [밝기 적용] 버튼, [방 조명 모두 끄기] 버튼을 추가한다. SeekBar의 `max`는 `255`, `progress`는 `128`이다.

| 슬라이더 위치 | 값 | 조명 |
|---|---|---|
| 맨 왼쪽 | 0 | 꺼짐 |
| 처음 위치 | 128 | 중간 밝기 |
| 맨 오른쪽 | 255 | 최대 밝기 |

### 7. 선택한 조명에 밝기 적용

```kotlin
binding.pwmButton.setOnClickListener {
    send("pwm ${selectedLamp()} ${binding.brightnessBar.progress}")
}
binding.allOffButton.setOnClickListener { send("off -1") }
```

책상 조명과 처음 밝기를 선택하면 `pwm 0 128`이다. 슬라이더를 움직이는 동안에는 전송하지 않는다. [밝기 적용]을 눌렀을 때 한 번 전송한다. `off -1`의 `-1`은 전체 LED를 뜻한다.

### 8. 공부 준비와 취침 준비

공부 준비는 책상 조명을 밝게 켜고 침대 조명을 끄는 순서다. 취침 준비는 책상 조명을 끄고 침대 조명을 약하게 켜는 순서다. 두 순서를 직접 실행하고 원하는 조명만 바뀌는지 확인한다.

### 9. 연결 화면으로 돌아가기

[연결 화면]을 누르면 제어 연결이 해제된다. 다시 [제어 시작]을 눌러 제어 화면을 연다. 제어 화면에서 홈 화면으로 이동하거나 회전한 경우에도 연결을 닫으므로 다시 연결한다. 앱은 화면 밖에서 제어를 계속하지 않는다.

## 선택 읽기 · TCP와 UDP

앱의 제어 명령은 TCP 8266으로 보낸다. 제공 클라이언트는 UDP 8267 검색도 지원한다. UDP 검색 결과는 주소를 찾는 데 사용하며 제어는 TCP가 담당한다. 정규 실습에서는 주소를 직접 입력한다. 검색 버튼이나 소켓 코드는 이번 과제로 구현하지 않는다.
