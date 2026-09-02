# 학기별 실습환경 기준표 — 복사용 템플릿

## 목차

- [사용법](#사용법)
- [승인 정보](#승인-정보)
- [실습실 공통 기준](#실습실-공통-기준)
- [공통 소프트웨어](#공통-소프트웨어)
- [웹프로그래밍](#웹프로그래밍)
- [모바일프로그래밍](#모바일프로그래밍)
- [오픈소스 AI 응용](#오픈소스-ai-응용)
- [Java·App Inventor](#javaapp-inventor)
- [계정과 외부 서비스](#계정과-외부-서비스)
- [검증 결과](#검증-결과)
- [변경 통제](#변경-통제)

## 사용법

이 파일은 직접 확정본으로 쓰지 않는다. 학기 시작 전 `environment_YYYY_NN_<course>.md`로 복사하고,
`TBD`를 담당 교수가 승인한 값으로 바꾼다. **TBD가 남은 항목은 설치·업데이트·펌웨어 변경을 시작하지 않는다.**

버전 문자열은 다운로드 페이지의 이름이 아니라 설치 후 명령이나 프로그램의 About 화면에서 복사한다.
한 대의 기준 PC에서 수업의 첫 실습까지 통과한 뒤 나머지 PC에 같은 기준을 적용한다.

## 승인 정보

| 항목 | 값 |
|---|---|
| 학교·학기·과목·분반 | TBD |
| 강의실·PC 수·예비 PC 수 | TBD |
| 기준 PC 번호 | TBD |
| 작성 조교 | TBD |
| 최초 검증일 | TBD |
| 담당 교수 승인일 | TBD |
| 기준 Git commit 또는 교재 edition | TBD |
| 수업 중 업데이트 허용 창구 | 담당 교수 승인 후 기준 PC 검증 |

## 실습실 공통 기준

| 항목 | 기준 | 확인 결과 |
|---|---|---|
| Windows edition·build | TBD | TBD |
| CPU·가상화 지원 | TBD | TBD |
| RAM | TBD GB 이상 | TBD |
| 시스템 드라이브 여유 | TBD GB 이상 | TBD |
| GPU·VRAM·드라이버 | 해당 과목만 TBD | TBD |
| Bluetooth·USB 포트 | 해당 과목만 TBD | TBD |
| 인터넷·프록시·방화벽 | 공식 사이트, GitHub, 수업 서비스 접속 | TBD |
| 학생 저장 경로 | 예: `C:\classwork` — 최종 경로 TBD | TBD |
| 복원 정책 | 재부팅 복원 여부와 저장 예외 경로 TBD | TBD |
| 관리자 설치 담당 | 조교/전산실 중 TBD | TBD |

권장 저장 경로는 짧은 영문 경로다. OneDrive 동기화 폴더, 바탕화면, 네트워크 드라이브,
공백·한글이 매우 긴 경로는 Gradle·Node·Python 캐시와 압축 해제 문제를 늘릴 수 있으므로 기준 PC에서 먼저 검증한다.

## 공통 소프트웨어

| 도구 | 승인 버전 | 설치 방식·파일 | 설치 후 확인 | 자동 업데이트 정책 |
|---|---|---|---|---|
| Git for Windows | TBD | 공식 설치 프로그램 | `git --version` | TBD |
| VS Code | TBD | User/System Setup 중 TBD | `code --version` | TBD |
| Chrome 또는 Chromium 브라우저 | TBD | 학교 표준 배포 | About 화면 | TBD |
| PowerShell | TBD | Windows 기본 또는 PowerShell 7 | `$PSVersionTable.PSVersion` | TBD |

공유 PC에서 `git config --global user.name`과 `user.email`을 조교 이름으로 설정하지 않는다.
학생은 자신의 계정으로 로그인한 뒤 자신의 식별정보를 설정한다.

## 웹프로그래밍

| 항목 | 승인 값 | 검증 방법 |
|---|---|---|
| Node.js LTS major·minor | TBD | `node --version` |
| npm | Node와 함께 설치된 값 | `npm --version` |
| Marp 도구 | 사용 안 함 / VS Code 확장 / CLI — TBD | 슬라이드 1개 preview/export |
| GitHub Pages 기준 | branch·folder TBD | 새 실습 저장소 배포 |
| Supabase 기준 | 학생별/팀별 project, region TBD | publishable key로 읽기·RLS 교차검증 |
| Deno | 미사용/선택 — TBD | 선택 시 공식 smoke test |
| Kakao 특강 | 미사용/사용 — TBD | localhost 허용 도메인과 지도 1회 표시 |

## 모바일프로그래밍

| 항목 | 승인 값 | 검증 방법 |
|---|---|---|
| Android Studio release | TBD | Help > About |
| bundled JBR/JDK | TBD | About 화면 또는 Gradle JDK 설정 |
| Android Gradle Plugin | TBD | 기준 프로젝트 sync |
| Gradle wrapper | TBD | 기준 프로젝트의 wrapper |
| Kotlin plugin | TBD | 기준 프로젝트 build |
| `compileSdk` / `targetSdk` / `minSdk` | TBD / TBD / TBD | 기준 프로젝트 설정 |
| SDK Platform·Build Tools·Platform Tools | TBD | SDK Manager |
| 기준 AVD·system image | TBD | cold boot 후 앱 실행 |
| 기준 실기기·Android OS | TBD | `adb devices`와 앱 실행 |
| BLE UUID·GPIO·payload 규약 | TBD | fake와 실제 보드 계약 테스트 |
| ESP32-C3 펌웨어 이미지·해시 | TBD | 기준 보드 연결·입출력 확인 |
| 예비 장비 | 수업 수량의 10% 이상, 최종 수량 TBD | 라벨·체크리스트 대조 |

Android Studio가 제공하는 JBR을 기본으로 하며, 기준표가 요구하지 않으면 별도 JDK를 추가 설치하지 않는다.
BLE 실습은 에뮬레이터만으로 완료 판정하지 않고 승인된 실제 Android 기기와 사전 플래시 보드로 검증한다.

## 오픈소스 AI 응용

| 항목 | 승인 값 | 검증 방법 |
|---|---|---|
| uv | TBD | `uv --version` |
| Python major·minor·patch | TBD | `uv run python --version` |
| dependency/lock 파일 | TBD 경로 | 깨끗한 폴더에서 `uv sync` |
| Ollama | TBD | `ollama --version` 및 API health |
| PyTorch 또는 TensorFlow | TBD | CPU/GPU smoke test |
| GPU driver·CUDA runtime 관계 | TBD | 프레임워크 장치 인식 |
| 모델 ID·revision·quantization | TBD | 해시/ID 기록 후 1회 추론 |
| 모델 캐시 경로·필요 용량 | TBD | 다운로드 전 여유공간 확인 |
| 기준 RTX 4070 실행시간·VRAM | TBD | 같은 입력으로 측정 |
| CPU/소형 모델 대체안 | TBD | GPU 없는 PC에서 검증 |

전역 `pip install`은 사용하지 않는다. Python 버전과 패키지는 프로젝트의 manifest와 lock 파일로 재현한다.
현재 저장소에는 OpenSW용 확정 lock 파일이 없으므로, 이 항목이 마련되기 전에는 전체 PC 설치를 진행하지 않는다.

## Java·App Inventor

| 항목 | 승인 값 | 검증 방법 |
|---|---|---|
| Java JDK | TBD | `java -version`, `javac -version` |
| Java IDE | TBD | 기준 프로젝트 build/run |
| MIT App Inventor 로그인 | TBD | 빈 프로젝트 생성 |
| Companion·기기 연결 | Wi-Fi/USB 중 TBD | Hello 화면 실기기 표시 |
| 외부 서비스 장애 대체안 | TBD | mock 또는 저장 응답 실행 |

## 계정과 외부 서비스

| 서비스 | 학생/팀/수업 공용 | 준비 담당 | 완료 기준 | 비밀정보 취급 |
|---|---|---|---|---|
| GitHub | TBD | TBD | 이메일 인증, 저장소 생성·clone·push | 비밀번호·2FA 수집 금지 |
| Supabase | TBD | TBD | 수업용 project와 RLS 테스트 | secret/service-role 배포 금지 |
| Hugging Face | TBD | TBD | 필요한 공개 모델 접근 | token은 `.env`로만 |
| Kakao Developers | TBD | TBD | JS 키·허용 도메인 검증 | 실제 키 Git 기록 금지 |
| MIT App Inventor | TBD | TBD | 로그인·Companion 연결 | 개인 계정 비밀번호 수집 금지 |

학교 학사·행정 시스템 계정과 교수 개인 계정은 일반 실습환경 계정에 포함하지 않는다.

## 검증 결과

| PC/장비 ID | 일시 | 공통 | 과목 smoke test | 네트워크 | 담당자 | 결과·이슈 링크 |
|---|---|---|---|---|---|---|
| 기준 PC | TBD | TBD | TBD | TBD | TBD | TBD |
| 예비 PC | TBD | TBD | TBD | TBD | TBD | TBD |

완료 기준은 설치창의 “성공”이 아니라 **새 PowerShell에서 버전 확인 → 예제 실행 → 브라우저/기기 결과 확인 → 재실행**이다.

## 변경 통제

- 수업 중 자동 업데이트 알림이 떠도 즉시 전체 PC를 갱신하지 않는다.
- 보안상 긴급한 업데이트는 기준 PC와 예비 PC에서 교재 smoke test를 통과한 뒤 배포한다.
- 버전을 바꾸면 변경일, 이유, 이전/새 버전, 영향을 받은 실습과 복구 방법을 기록한다.
- 한 PC만 다른 버전이면 그 PC를 수업에서 제외하거나 기준 이미지로 복구하고 임의 땜질을 누적하지 않는다.
