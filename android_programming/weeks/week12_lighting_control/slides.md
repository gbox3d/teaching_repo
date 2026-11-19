---
marp: true
theme: default
paginate: true
header: 모바일프로그래밍 · 12
footer: RoomControl · LAN
---

# 내 방 조명 선택과 밝기 제어

12주차

연결 화면에서 시작하고, 제어 화면에서 방의 조명을 바꾼다.

1일차: 책상·침대 조명 선택

2일차: 밝기 조절과 전체 끄기

---

# 1일차 · 0~5분 · 오늘의 화면

`내 방 제어`

- 책상 조명 · LED 0
- 침대 조명 · LED 1
- 조명 켜기 / 조명 끄기
- 조명 설정 결과

사용자는 조명 이름을 선택한다.

---

# 1일차 · 5~9분 · 연결 후 제어

1. PC에서 WlEno를 실행한다.
2. 앱에서 주소를 확인한다.
3. [제어 시작]을 누른다.
4. 연결에 성공하면 제어 화면이 열린다.

연결 화면과 통신 코드는 제공 파일을 사용한다.

---

# 1일차 · 9~13분 · 두 선택을 한 그룹으로

`RadioGroup` 안에 `RadioButton` 두 개를 둔다.

| ID | 화면 글자 | LED |
|---|---|---|
| deskRadio | 책상 조명 | 0 |
| bedRadio | 침대 조명 | 1 |

기본 선택은 책상 조명이다.

---

# 1일차 · 13~17분 · 선택을 번호로 바꾸기

```kotlin
private fun selectedLamp(): Int {
    return if (binding.deskRadio.isChecked) 0 else 1
}
```

책상 조명 선택: 0

침대 조명 선택: 1

---

# 1일차 · 17~21분 · 버튼에서 명령 만들기

```kotlin
binding.onButton.setOnClickListener {
    send("on ${selectedLamp()}")
}
binding.offButton.setOnClickListener {
    send("off ${selectedLamp()}")
}
```

침대 조명을 켜면 `on 1`을 보낸다.

---

# 1일차 · 21~26분 · 응답으로 결과 표시

```json
{"result":"ok","ms":"led(s) on"}
```

버튼을 누른 직후: `응답 대기 중`

서버가 `ok`로 답한 뒤: `조명 설정 완료`

아래 작은 글자에서 보낸 명령과 받은 JSON을 확인한다.

---

# 1일차 · 26~30분 · 실습 확인 순서

책상 조명 켜기, 침대 조명 켜기, 책상 조명만 끄기.

| 관찰 | 예상 |
|---|---|
| 마지막 책상 조명 | 꺼짐 |
| 마지막 침대 조명 | 켜짐 |
| 완료 표시 | 서버 응답 뒤 표시 |

이후 60분 동안 선택 UI와 버튼을 구현한다.

---

# 2일차 · 0~5분 · 밝기로 상황 만들기

공부 준비: 책상은 밝게, 침대는 끄기.

취침 준비: 책상은 끄고, 침대는 어둡게.

외출: 방 조명 모두 끄기.

같은 제어 화면에서 조명과 밝기를 선택한다.

---

# 2일차 · 5~10분 · 밝기 슬라이더

`brightnessBar`는 SeekBar다.

| 위치 | 값 | 결과 |
|---|---|---|
| 맨 왼쪽 | 0 | 꺼짐 |
| 시작 | 128 | 중간 밝기 |
| 맨 오른쪽 | 255 | 최대 밝기 |

XML: `max="255"`, `progress="128"`

---

# 2일차 · 10~15분 · 밝기 적용 버튼

```kotlin
binding.pwmButton.setOnClickListener {
    send("pwm ${selectedLamp()} " +
        "${binding.brightnessBar.progress}")
}
```

`pwm 0 128`: 책상 조명, 밝기 128

슬라이더 이동 후 [밝기 적용]을 눌러 한 번 전송한다.

---

# 2일차 · 15~19분 · 방 조명 모두 끄기

```kotlin
binding.allOffButton.setOnClickListener {
    send("off -1")
}
```

`-1`은 전체 LED를 뜻한다.

앱의 조명 선택과 관계없이 모든 원이 꺼진다.

---

# 2일차 · 19~23분 · 결과와 근거

큰 결과 글자: `조명 설정 완료`

작은 전송 글자: `보냄: pwm 0 128`

작은 수신 글자:
```json
{"result":"ok","ms":"pwm set"}
```

결과는 `WlenoMessage.result(line)`으로 구분한다.

---

# 2일차 · 23~27분 · 화면 종료와 재사용

[연결 화면]을 누르면 제어 연결을 해제한다.

다시 사용하려면 [제어 시작]을 누른다.

WlEno는 연결·해제 때 LED 상태를 유지한다.

홈 화면 이동이나 회전 뒤에도 다시 연결한다.

---

# 2일차 · 27~30분 · 실습 확인

1. 공부 준비와 취침 준비를 각각 만든다.
2. 앱과 WlEno를 함께 캡처한다.
3. `pwm 0 128`의 숫자를 설명한다.
4. 친구가 같은 순서를 재현하는지 확인한다.

이후 60분 동안 밝기 제어를 구현한다.

---

# 제출과 다음 수업

제출: `ControlActivity.kt`, `activity_control.xml`, 상황별 캡처 2장.

코드: 선택한 조명과 밝기가 명령에 들어가는 위치.

다음 수업: 제어 시나리오 점검과 계획안 발표.

자료: [따라하기](walkthrough.md) · [실습지](lab.md)
