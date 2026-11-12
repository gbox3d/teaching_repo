# 모바일프로그래밍 실습조교용 설치 프로그램 목록

## 목차

- [필수 설치](#필수-설치)
- [필요할 때만 설치](#필요할-때만-설치)
- [별도 설치하지 않는 항목](#별도-설치하지-않는-항목)
- [설치 확인](#설치-확인)
- [BLE 수업 전 보드 점검](#ble-수업-전-보드-점검)

## 필수 설치

**1주차 1일차부터 Android Studio를 사용한다.** 실습실 PC에 Android Studio가 설치되어 있어야 한다.
수업 전에 한 대에서 `Empty Views Activity`로 새 프로젝트를 만들어 첫 Gradle 동기화 시간을 재 보고,
`fun main()`이 있는 Kotlin 파일을 왼쪽 여백 ▶으로 실행해 Run 창에 출력이 나오는지 확인한다.
1주차에는 에뮬레이터를 쓰지 않으므로 AVD 준비는 2주차 전까지 끝내면 된다.

| 프로그램·구성요소 | 공식 경로 | 비고 |
|---|---|---|
| [Git for Windows](https://git-scm.com/install/windows) | Git 공식 사이트 | 수업 프로젝트 받기 |
| [Android Studio](https://developer.android.com/studio/install) | Android 공식 사이트 | 내장 JBR/JDK 사용 |
| Android SDK Platform | Android Studio의 SDK Manager | 정확한 버전은 TBD |
| Android SDK Build Tools | Android Studio의 SDK Manager | 정확한 버전은 TBD |
| Android SDK Platform Tools | Android Studio의 SDK Manager | ADB 포함 |
| Android Emulator·AVD system image | Android Studio의 Device Manager | 승인된 기기 profile과 image 사용 |

## 필요할 때만 설치

| 프로그램 | 설치 조건 |
|---|---|
| Android 제조사 USB 드라이버 | 실기기가 인식되지 않고 제조사 드라이버가 필요한 경우 |
| Windows 가상화 구성요소 | AVD 실행에 필요하며 전산실이 승인한 경우 |
| Python 3.9 이상 | 실습실 PC에서 Wi-Fi 시뮬레이터 실습([iot_sim](iot_sim/README.md))을 할 때. 표준 라이브러리만 쓰므로 추가 패키지는 없다. `py --version`으로 확인한다 |

시뮬레이터에 실기기로 붙일 때는 PC에서 TCP 8266·UDP 8267 인바운드를 허용해야 한다([iot_sim README 7절](iot_sim/README.md#7-windows-방화벽)). 학생 계정에 관리자 권한이 없으면 조교가 연다. 관리자가 아닌 계정에서는 Windows가 시뮬레이터를 돌리는 Python을 막는 규칙을 남길 수 있고, 막는 규칙은 포트 허용보다 앞선다. 그래서 조교는 포트 규칙만 만들지 말고, 시뮬레이터를 켜 둔 채로 같은 절의 네 줄로 막는 규칙도 확인한다. 수업이 끝나면 같은 절대로 포트 규칙 두 개를 지우고 **Python 규칙 지우기**를 한다.

## 별도 설치하지 않는 항목

- 별도 JDK: Android Studio의 내장 JBR을 우선 사용한다.
- Arduino IDE·ESP-IDF: ESP32-C3는 사전 플래시 보드를 사용하므로 조교 설치 대상이 아니다.
- 임의 SDK·Gradle·Kotlin 버전: 학기별 기준값이 정해질 때까지 설치하지 않는다.

## 설치 확인

```powershell
git --version
adb --version
adb devices
```

Android Studio의 **Help > About**, **SDK Manager**, **Device Manager** 화면에서 실제 버전을 확인한다.
정확한 Android Studio·SDK·AVD·기기 OS 값은 [학기별 환경 기준표](../environment_baseline_template.md)에서 담당 교수가 확정한다.

## BLE 수업 전 보드 점검

학생은 SmartIO 앱에 [교재의 `bleuno` 클래스](bleuno/README.md)를 넣어 수업을 이어 간다.
강의자·조교는 [별도 저장소의 `BleunoTest`](https://github.com/gbox3d/bleunoApp/tree/main/BleunoTest)를 Android Studio에서 열어 보드를 먼저 점검할 수 있다.
`bleunoApp` 루트가 아니라 `BleunoTest/`가 독립 Gradle 프로젝트의 루트다.

아래 절차는 기존 LED 실습 보드의 배선·설정이 확인된 경우에 사용한다.

1. Android 실기기의 BLE 권한을 허용하고 보드를 검색·연결한다.
2. `about` 응답으로 펌웨어를 확인한다. UUID·명령 규약은 교재의 `bleuno` 안내와 대조한다.
3. 보드의 실제 배선과 `ledpin` 설정을 확인한 뒤, 유효한 인덱스의 켜기·끄기를 시험한다. DHT11이 연결·설정된 경우에만 온습도도 확인한다.
4. 연결 해제·재연결을 확인한 후 학생용 SmartIO에서도 같은 동작을 확인한다.

type_m v1 마더보드의 KiCad 설계·핀맵은 [펌웨어 저장소](https://github.com/gbox3d/bleuno)의 `hardware/type_m/v1/`에서 관리한다.
EasyEDA 원본 확보와 KiCad 이전·원본 대조는 완료했다. 원본 설계의 전기적 미연결과 모듈 핀 표기 검토는 남아 있다.
원본은 모터·서보용이며 기존 LED 4개·DHT11 실습과 다르다.
[type_m v1 핀맵](https://github.com/gbox3d/bleuno/blob/main/hardware/type_m/v1/pinmap.md)에서 GPIO0=CHKBAT, GPIO7=SLEEP, SEN1의 MCU 미연결과 전원 헤더의 VIN 미연결을 확인한다.
기존 `ledpin=[4,3,1,0]`·`dht11pin=7`을 type_m v1에 적용하거나, 센서·모터 버튼을 기존 LED 점검 순서대로 누르지 않는다.
모터·서보 확장 수업은 [type_m 전용 90분 실습](bleuno/type_m_lab.md)으로 진행한다. 이때 여는 독립 프로젝트는 `bleunoApp/TypeMControl/`이며 Kotlin·XML, Android SDK 36.1 기준이다. 펌웨어는 `bleuno` 저장소의 `type_m` 환경(PlatformIO espressif32 6.12.0 / Arduino-ESP32 2.0.17)을 사용한 사전 플래시 보드를 준비한다. 기존 `BleunoTest`·`Config`의 LED 설정을 적용하지 않는다.

type_m 사전 점검은 CCCD 알림 구독 → `about`의 `type_m/1 fw=1.0.0` 확인 → `ready`/`ok ready` 순서다. RGB 상태 LED는 연결 대기에 빨강 점멸, BLE 연결 후 준비 전에는 파랑 점멸, 준비 완료에는 파랑 고정으로 표시하도록 구성한다. 사용자가 설계대로 실장했고 모듈은 EstarDyn ESP32-C3 SuperMini Plus V2.0 RGB 보드라고 확인했다. GPIO8 NeoPixel의 대기 빨강 점멸과 READY 파랑 고정은 사용자 실물 확인을 받았다. 준비 전 파랑 점멸은 소스·상태 기준이며 별도 색상 관찰 결과가 아니다.

이번 보드는 펌웨어 업로드·Flash hash 검증과 BLE 비구동 검사29개를 통과했다. IM_L101(API34)에서 검색·제어 준비·STOP 응답·배경 진입 후 연결 해제·재연결 준비를 확인했고, 시리얼의 모터·서보 duty는 각 단계에서 0이었다. 0이 아닌 모터 명령과 유효한 서보 각도 명령은 전송하지 않았으며 실제 부하 구동·파형 계측은 남아 있다.

처음에는 모터·서보를 분리한 채 명령·응답을 확인한다. 부하를 연결하기 전에는 원본 핀맵의 VCC·신호·GND 순서와 실제 외부 전원을 점검하고, USB만으로 큰 모터·서보 전류를 공급하지 않는다. 실습 자료의 확인표로 슬라이더 해제 정지, STOP, 배경 진입·연결 해제, 1500ms watchdog을 구분해서 검사한다. 펌웨어 업로드·Android 실기 연결·부하 구동의 결과는 확인된 범위만 기록한다. 검증 전 정규 SmartIO 수업은 기존 보드 또는 Fake 모드로 유지한다.

type_s v1 센서·입출력 커넥터 보드는 [별도 원본 핀맵](https://github.com/gbox3d/bleuno/blob/main/hardware/type_s/v1/pinmap.md)을 확인한다.
DHT·CDS·DS18B20 표기는 헤더 이름이며 센서 실장·펌웨어 지원·제작 검증을 뜻하지 않는다. 기존 LED 설정은 센서·분압 입력과 충돌하고 `dht11pin=7`은 D2에 해당한다.
원본 DHT 헤더 신호 GPIO3도 외부 센서·전원·펌웨어 설정의 실기 검증 전에는 수업의 확정 설정으로 사용하지 않는다.
