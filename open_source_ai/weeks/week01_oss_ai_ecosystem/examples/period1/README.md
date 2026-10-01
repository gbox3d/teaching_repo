# 1교시 — 실습환경 점검표 만들기

[실습지 1교시](../../lab.md#1교시-실습--실습환경-점검표-만들기)의 **점검 도구와 기록 양식**이다.
`env_check.ps1`과 `env_check_template.md`를 개인 폴더 `C:\classwork\osa-week01`로 복사한다.
원본 폴더에서 결과 파일을 만들지 않는다.

| 실습 단계 | 볼 파일 | 확인할 결과 |
|---|---|---|
| 준비·문제 1 | [env_check.ps1](env_check.ps1) | 도구 5개의 설치 상태·실패 이유 |
| 문제 1·2 기록 | [env_check_template.md](env_check_template.md) | 버전·경로·조치·계정 확인표 |

개인 폴더에서:
```powershell
powershell -ExecutionPolicy Bypass -File .\env_check.ps1 -OutFile env_check_raw.md
```
GPU·Ollama가 없는 PC는 해당 실패 행과 다음 조치를 기록하는 것이 정상이다.
다음 [2교시](../period2/README.md)에서 프로젝트 탐색표를 추가한다.

## uv 최초 설치와 최신 버전 업데이트

실습지 문제 2(11–19분)에서 `uv`가 없으면 **Windows PowerShell**로 설치한다. 버전을 지정하지 않은 아래 명령은 해당 설치 경로의 최신 버전을 설치한다. 수업에서 버전을 지정했다면 [환경 기준표](../../../../../environment_baseline_template.md)를 먼저 따른다.

```powershell
# 공식 설치 스크립트(기본)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

스크립트 실행이 학교·회사 정책으로 막혀 있으면 아래 방법을 쓴다. 두 방법을 중복 실행하지 않는다.

```powershell
winget install --id=astral-sh.uv -e
```

**PowerShell을 완전히 닫고 새 창을 연 뒤** 버전과 실행 경로를 확인한다. VS Code 터미널이면 VS Code도 종료 후 다시 연다.

```powershell
uv --version
Get-Command uv | Select-Object -ExpandProperty Source
```

이미 설치된 uv를 최신 버전으로 올릴 때는 **설치했던 방법에 맞는 명령 하나만** 실행한다. 수업 PC는 기준 버전을 확인한 뒤 갱신한다.

```powershell
# 공식 설치 스크립트로 설치했다면
uv self update
```

```powershell
# WinGet으로 설치했다면
winget upgrade --id=astral-sh.uv -e
```

갱신 후 새 창에서 `uv --version`과 실행 경로를 다시 확인해 점검표에 기록한다. uv 자체를 갱신해도 Python 버전과 프로젝트 패키지가 함께 최신으로 바뀌지는 않는다.

macOS·Linux 설치, 버전 지정, 오류 해결은 [uv 사용 가이드](../../../../uv_guide.md)를 참고한다. 명령 근거: [uv 공식 설치·업데이트 문서](https://docs.astral.sh/uv/getting-started/installation/).

## 실습 시간표

| 단계 | 시간 | 활동 |
|---|---:|---|
| 문제·예상 | 0–4분 | 도구 5개 중 무엇이 없을지 예상, 예제 복사, 템플릿 복사 |
| 도구 점검 | 4–11분 | `env_check.ps1` 실행, 실패 항목을 수동 명령으로 재확인 |
| 없는 도구 설치 | 11–19분 | `uv` 설치, 새 창에서 재확인, 설치 경로 확인 |
| 계정 확인 | 19–24분 | GitHub·Hugging Face 로그인과 공개 프로필 점검 |
| 검증·기록 | 24–30분 | `env_check.md` 완성, 실패 항목 조치 문장 |

시간은 설명·시연 20분 뒤 시작하는 **실습 30분 기준**이다. 휴식 10분은 별도다.
