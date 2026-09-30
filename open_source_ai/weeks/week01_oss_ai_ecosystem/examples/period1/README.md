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

## 실습 시간표

| 단계 | 시간 | 활동 |
|---|---:|---|
| 문제·예상 | 0–4분 | 도구 5개 중 무엇이 없을지 예상, 예제 복사, 템플릿 복사 |
| 도구 점검 | 4–11분 | `env_check.ps1` 실행, 실패 항목을 수동 명령으로 재확인 |
| 없는 도구 설치 | 11–19분 | `uv` 설치, 새 창에서 재확인, 설치 경로 확인 |
| 계정 확인 | 19–24분 | GitHub·Hugging Face 로그인과 공개 프로필 점검 |
| 검증·기록 | 24–30분 | `env_check.md` 완성, 실패 항목 조치 문장 |

시간은 설명·시연 20분 뒤 시작하는 **실습 30분 기준**이다. 휴식 10분은 별도다.
