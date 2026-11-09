# BLEuno type_m — BLE 모터·서보 제어 실습

**90분 동안 BLE 연결과 제어 준비를 구분하고, 모터 2개·서보 2개의 명령 및 정지 동작을 확인한다.**
실습 앱은 Kotlin·XML로 만든 독립 프로젝트 `bleunoApp/TypeMControl`이다. 기존 SmartIO·Fake와 LED/DHT11 실습은 [기존 안내](README.md)를 따른다.

## 준비와 확인 범위

| 항목 | 이번 실습 기준 |
|---|---|
| 하드웨어 | `bleuno/hardware/type_m/v1/`, EstarDyn ESP32-C3 SuperMini Plus V2.0 RGB 보드와 DRV8833 모듈. 설계대로 실장 완료는 사용자 확인 |
| 펌웨어 | `bleuno` 저장소의 PlatformIO 환경 `type_m`; `platform = espressif32@6.12.0`, Arduino-ESP32 2.0.17 |
| 소스 | `bleuno/src/type_m_main.cpp`, `bleuno/include/type_m_protocol.hpp` |
| 앱 | Android Studio에서 `bleunoApp/TypeMControl/` 폴더 열기; 컴파일 SDK 36.1, 실행 기기는 Android 7.0(API 24) 이상 |
| 상태 표시 | GPIO8 NeoPixel. 대기 빨강 점멸·준비 완료 파랑 고정은 사용자 실물 확인. 준비 전 파랑 점멸은 소스·상태 기준 |

이 문서는 실습 절차와 명령 규약이다. 호스트 파서·제어 상태399 checks, Android 단위 테스트17개·Lint, 펌웨어 빌드·업로드와 BLE 비구동 검사29개를 통과했다. Android IM_L101(API34)에서 보드 검색·CCCD/about/ready·STOP 응답·배경 진입 후 연결 해제·재연결 준비를 확인했다. 각 단계의 시리얼 상태에서 모터 출력과 서보 duty는 0이었다. **0이 아닌 모터 명령과 유효한 서보 각도 명령은 아직 전송하지 않았으며, 실제 부하 구동·핀 파형도 미검증이다.** 부하를 연결하는 단계는 조교가 실제 전원과 결선을 점검한 장비에서 진행한다.

학생은 사전 플래시 보드를 사용한다. 펌웨어 환경 설치나 `Config` 앱으로 핀을 바꾸는 과정은 이 실습에 포함하지 않는다. 기존 LED 명령 `on`, `off`, `pwm`과 `dht11`도 보내지 않는다.

## 1. 핀과 전원을 먼저 읽기

아래 GPIO는 [원본 회로·PCB 핀맵](https://github.com/gbox3d/bleuno/blob/main/hardware/type_m/v1/pinmap.md)에 따른다. 모듈 핀 번호와 ESP32 GPIO 번호를 혼동하지 않는다.

| 기능 | 연결 |
|---|---|
| 모터 1 입력 | GPIO1 → IN1, GPIO3 → IN2; 출력은 MT1 |
| 모터 2 입력 | GPIO4 → IN3, GPIO5 → IN4; 출력은 MT2 |
| 드라이버 nSLEEP | GPIO7 |
| Servo1 / Servo2 신호 | GPIO6 / GPIO10 |
| 배터리 감지 | GPIO0, 220kΩ 두 개의 분압 중간점 |

서보 커넥터 J5·J6은 **패드 1=VCC, 2=신호, 3=GND**다. 커넥터를 바라보는 방향에 따라 좌우가 바뀌므로 색이나 좌우 순서만으로 꽂지 않는다. VCC는 배터리·모터 드라이버·서보·MCU의 `+5V` 표기 핀이 공유하는 네트이며, 마더보드가 전압을 5V로 조절한다는 뜻은 아니다. USB 포트만으로 모터·서보의 큰 전류를 공급하지 않는다. 외부 전원과 USB를 함께 쓸 때의 전원 경로도 실물 보드에서 확인한다.

GPIO0을 출력으로 쓰는 기존 `ledpin=[4,3,1,0]`, GPIO7을 센서로 쓰는 `dht11pin=7`은 적용하지 않는다. `SEN1`은 MCU 미연결이고, 전원 헤더의 `VIN`도 다른 부하에 연결되지 않아 전체 전원 차단 스위치로 간주할 수 없다.

모터의 속도 명령은 회전수 측정값이 아니라 PWM 출력 비율이다. 부호는 두 입력의 구동 방향을 선택하며 실제 바퀴의 전진 방향은 결선에 따라 다르다. DRV8833에서 두 입력 LOW는 coast, 두 입력 HIGH는 brake이고 nSLEEP LOW는 출력을 비활성화한다. STOP을 기계적인 즉시 정지나 전원 차단으로 해석하지 않는다. [TI DRV8833 데이터시트 §7.3–7.4](https://www.ti.com/lit/ds/symlink/drv8833.pdf)

## 2. BLE 연결과 앱 준비의 차이

앱은 GATT client, 보드는 GATT server다. **Service**는 기능의 묶음, **Characteristic**은 명령을 쓰고 응답을 받는 항목, **CCCD**는 해당 연결에서 알림 수신을 켜는 descriptor다. GATT 연결 뒤에도 서비스 탐색과 알림 설정이 필요하다. [Android GATT 연결](https://developer.android.com/develop/connectivity/bluetooth/ble/connect-gatt-server), [서비스 탐색·알림 수신](https://developer.android.com/develop/connectivity/bluetooth/ble/transfer-ble-data)

| 항목 | UUID |
|---|---|
| Service | `c6f8b088-2af8-4388-8364-ca2a907bdeb8` |
| Characteristic | `f6aa83ca-de53-46b4-bdea-28a7cb57942e` |
| CCCD | `00002902-0000-1000-8000-00805f9b34fb` |

순서는 **검색 → GATT 연결 → 서비스·특성 확인 → CCCD 알림 구독 → `about`으로 type_m 확인 → `ready` → `ok ready` 수신 → 제어 활성화**다. UUID는 기존 펌웨어와 같으므로 UUID 발견만으로 모델 확인이 끝나지 않는다. `type_m/1 fw=1.0.0` 응답까지 확인한다.

| RGB 상태 LED | 뜻 |
|---|---|
| 빨강, 500ms 간격 점멸 | 앱 연결 대기 |
| 파랑, 250ms 간격 점멸 | BLE는 연결됐지만 앱 제어 준비 전 |
| 파랑 고정 | 알림 구독과 `ready` 절차를 마쳐 제어 가능 |

여기서 빨강·파랑은 **RGB 상태 LED의 색**이다. 별도 전원 표시 LED를 뜻하지 않는다. RGB 핀은 펌웨어 상수로 조정하며, 단색 GPIO LED의 HIGH/LOW 제어 예제를 대신 넣지 않는다. 실제 LED가 다르게 보이면 앱 로그와 펌웨어 핀 설정을 함께 확인한다.

## 3. 한 명령과 한 응답 읽기

한 번의 쓰기에 ASCII 명령 하나를 보내며 최대 20바이트다. 응답도 아래와 같은 짧은 텍스트다. 기존 SmartIO의 JSON 응답 파서를 재사용하지 않는다.

| 보내는 명령 | 받는 응답 | 뜻 |
|---|---|---|
| `about` | `type_m/1 fw=1.0.0` | 모델·프로토콜·펌웨어 확인 |
| `ready` | `ok ready` | 앱 제어 준비 요청 |
| `ping` | `ok ping` | 연결 상태 유지 확인 |
| `motor 1 -100` | `ok motor 1 -100` | 모터 1, 음의 방향 100% |
| `motor 2 0` | `ok motor 2 0` | 모터 2 출력 0 |
| `servo 1 90` | `ok servo 1 90` | 서보 1에 90도 명령 |
| `stop` | `ok stop` | 양 모터 정지 및 양 서보 펄스 끄기 |

모터 번호와 서보 번호는 각각 `1`, `2`다. 모터 값은 `-100..100`, 서보 각도는 `0..180`이다. `ok`는 펌웨어가 명령을 수락했다는 뜻이며 실제 축 위치·속도를 측정했다는 뜻은 아니다.

| 메시지 | 확인할 것 |
|---|---|
| `err syntax` | 명령 이름·인수 개수·ASCII 형식 |
| `err range` | 번호와 값의 범위 |
| `err not_ready` | `ok ready` 수신 전 제어 요청 여부 |
| `err subscribe` | CCCD 알림 구독 완료 여부 |
| `event timeout` | heartbeat 단절. READY가 해제되므로 연결을 정리하고 다시 준비 절차 수행 |

## 4. 90분 실습 순서

| 시간 | 할 일 | 남길 증거 |
|---|---|---|
| 0–10분 | 모델·펌웨어·핀맵·전원 확인. 처음에는 모터·서보 분리 | 사용 보드와 연결 계획 |
| 10–25분 | TypeMControl 실행, 권한 허용, 검색·연결. CCCD → about → ready 순서 관찰 | `type_m/1 fw=1.0.0`, `ok ready` 로그와 LED 상태 |
| 25–45분 | 모터 1·2 슬라이더를 낮은 크기에서 각각 움직이고 손을 뗀다. 양·음의 방향은 0을 거쳐 바꾼다 | 명령·응답 및 손을 뗐을 때 0으로 복귀하는 기록 |
| 45–60분 | 서보 1·2에 명시적으로 각도를 보낸다. 최초 연결만으로 중립 위치 이동이 발생하지 않는지 확인 | 첫 서보 명령 전후의 출력 차이 |
| 60–80분 | STOP, 앱 배경 진입, 연결 끊김 및 watchdog을 확인 | 아래 정지 확인표 |
| 80–90분 | 실패 원인을 분류하고 로그·확인표 제출 | 연결과 준비의 차이를 설명하는 문장 |

모터 슬라이더는 누르고 움직이는 동안 값을 보내며, **손을 떼면 해당 모터에 0을 보내고 중앙으로 돌아간다.** 전진·후진 여부는 낮은 출력에서 확인한다. 실물 부하 연결이 아직 검증되지 않은 장비에서는 표의 명령과 응답까지만 확인하고 축 동작을 확인했다고 기록하지 않는다.

서보는 최초 명령 전까지 펄스를 내보내지 않는다. 연결됐다는 이유로 자동으로 90도로 움직이지 않는다. 기본 변환은 50Hz에서 **0..180 → 1000..2000µs**이며 실제 기구 각도를 보장하지 않는다. 서보의 허용 범위에 맞춰 펌웨어 전용 상수를 조정한다. STOP 뒤에는 서보 신호 펄스가 꺼지지만 서보 전원은 남아 있으므로 축이 무조건 고정되거나 무전원이 된다고 가정하지 않는다.

모터 PWM과 서보 펄스는 주파수가 다르다. ESP32-C3의 LEDC는 6채널이므로 이 보드의 모터 입력 4개와 서보 2개에 배정한다. RGB LED는 별도 NeoPixel 구동을 사용한다. [Espressif ESP32-C3 LEDC 설명](https://docs.espressif.com/projects/esp-idf/en/stable/esp32c3/api-reference/peripherals/ledc.html)

## 5. 정지 확인표

앱은 READY 이후 500ms마다 `ping`을 보낸다. 펌웨어 watchdog은 1500ms 동안 유효한 제어 통신이 이어지지 않으면 출력을 정지하고 READY를 해제한다. 앱의 정지 명령은 통신이 끊기면 도착하지 않을 수 있으므로 보드 쪽 watchdog도 필요하다.

STOP은 기존 READY를 유지하므로 새로운 명시적 제어는 받을 수 있다. 연결 해제·구독 해제·timeout은 READY도 해제한다. 이 차이를 로그로 구분한다.

| 시험 | 기대 결과 | 관찰·통과 여부 |
|---|---|---|
| 최초 연결 / 재연결 | 모터 출력 0, 서보 자동 중립 이동 없음 | |
| 모터 슬라이더에서 손 떼기 | 해당 모터 0 명령, 슬라이더 중앙 복귀 | |
| STOP | 모터 둘 모두 정지, 서보 둘 모두 펄스 꺼짐 | |
| 앱을 배경으로 보내기 | 앱이 STOP을 요청하고 연결 해제 | |
| BLE 연결 해제 | 보드 출력 정지, 다시 연결·ready 하기 전 제어 불가 | |
| 링크를 유지한 채 heartbeat 중단 | 약 1500ms의 제한 후 정지, `event timeout`, READY 해제 | |
| timeout 뒤 재접속 | CCCD·about·ready를 다시 거쳐야 제어 활성화 | |

watchdog 시험은 **부하를 분리한 조교용 시험**으로 heartbeat 송신만 중단해 수행한다. 펌웨어 저장소의 `tools/type_m_smoke.py`는 비구동 명령으로 이 과정을 검사한다. 실행 방법은 [type_m 펌웨어 가이드](https://github.com/gbox3d/bleuno/blob/main/docs/type_m.md)를 따른다. 앱을 배경으로 보내면 연결 해제 경로가 동작하므로 그것만으로 watchdog을 검증했다고 적지 않는다. 스마트폰 알림 수신 시각에는 통신·스케줄링 지연이 있을 수 있으므로 1500ms를 기계적 정지 완료 시간으로 해석하지 않는다.

## 6. 막혔을 때와 제출 과제

| 증상 | 진단 순서 |
|---|---|
| 검색 결과 없음 | Bluetooth·런타임 권한·보드 전원·다른 앱의 기존 연결 확인 |
| BLE 연결 후 파랑 점멸만 계속됨 | 서비스·특성 UUID, CCCD 쓰기 완료, about 결과, ready 응답 순서 확인 |
| JSON 응답이 옴 | 기존 LED 펌웨어 또는 다른 보드에 연결했는지 확인 |
| 앱은 준비됨인데 모터가 움직이지 않음 | 명령·응답 → GPIO/드라이버 nSLEEP → 공통 GND·외부 전원 → 모터 출력 결선 순서로 조교 점검 |
| 서보가 처음에 움직이지 않음 | 최초 자동 중립 이동이 없는 것이 정상. 명시적 명령·전원·패드 순서 확인 |
| `event timeout` 반복 | 앱 heartbeat 주기·화면 생명주기·명령 큐 지연 확인 후 재연결 |
| RGB 색이 예상과 다름 | 실제 RGB 데이터 핀·펌웨어 상수·LED 종류 확인. GATT 로그의 READY 여부도 함께 확인 |

제출물은 연결부터 정지까지의 로그, 위 확인표, 다음 질문의 답이다.

1. GATT 연결 성공만으로 모터 슬라이더를 활성화하면 어떤 준비 단계가 빠지는가?
2. STOP 응답, 연결 해제에 의한 정지, watchdog timeout을 로그에서 어떻게 구별하는가?
3. `motor 1 -100`의 `-100`이 실제 모터 회전수와 같지 않은 이유는 무엇인가?
4. 서보의 초기 자동 이동을 없애고, 앱이 배경으로 갈 때 연결을 해제한 이유를 설명하라.
