# 오픈소스 AI 응용 실습조교용 설치 프로그램 목록

## 목차

- [필수 설치](#필수-설치)
- [설치 절차 — uv](#설치-절차--uv)
- [설치 절차 — Ollama](#설치-절차--ollama)
- [승인 후 설치](#승인-후-설치)
- [별도 설치하지 않는 항목](#별도-설치하지-않는-항목)
- [설치 확인](#설치-확인)

## 필수 설치

| 프로그램 | 공식 경로 | 비고 |
|---|---|---|
| [Git for Windows](https://git-scm.com/install/windows) | Git 공식 사이트 | 수업 저장소 받기 |
| [VS Code](https://code.visualstudio.com/docs/setup/windows) | VS Code 공식 사이트 | 코드·Notebook 편집 |
| [uv](https://docs.astral.sh/uv/getting-started/installation/) | uv 공식 문서 | Python 격리환경 관리 |
| [Ollama](https://docs.ollama.com/windows) | Ollama 공식 문서 | 로컬 모델 실행 |
| 학교 승인 브라우저 | Chrome 또는 Edge 공식 사이트 | GitHub·Hugging Face 사용 |

아래 두 절은 실습실 PC에 설치할 때의 절차이며, 개인 노트북으로 수강하는 학생에게 그대로 안내해도 된다.
**uv와 Ollama는 둘 다 관리자 권한 없이 사용자 계정에만 설치된다.**
명령과 경로는 2026-09-10에 공식 문서로 확인한 값이다(uv 0.12.11, Ollama 0.33.3 기준). 버전이 올라가면 다시 확인한다.

## 설치 절차 — uv

```powershell
# 방법 1 · 공식 설치 스크립트 (기본)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# 방법 2 · 스크립트 실행이 정책으로 막힌 PC
winget install --id=astral-sh.uv -e
```

| 항목 | 값 |
|---|---|
| 관리자 권한 | 필요 없음 |
| 설치 위치 | `%USERPROFILE%\.local\bin\uv.exe` (winget으로 설치하면 다름) |
| PATH | 설치 프로그램이 사용자 PATH에 추가한다. **이미 열려 있던 창에는 반영되지 않는다** |
| Python | 따로 설치하지 않는다. `requires-python`을 보고 uv가 가져온다 |

확인은 **새 PowerShell 창**에서 한다. `Get-Command uv | Select-Object -ExpandProperty Source`로 실제 경로를 함께 남긴다.

## 설치 절차 — Ollama

```powershell
# 방법 1 · 공식 설치 스크립트 (기본)
powershell -ExecutionPolicy ByPass -c "irm https://ollama.com/install.ps1 | iex"

# 방법 2 · 스크립트 실행이 정책으로 막힌 PC
winget install --id=Ollama.Ollama -e

# 방법 3 · 설치 파일을 직접 받는 경우
# https://ollama.com/download/OllamaSetup.exe
```

> `Ollama.Ollama`와 `Ollama.Ollama.Portable`은 **다른 패키지**다. Portable은 트레이 앱이 없는 압축 해제형 CLI라 설치 위치도 동작도 다르다. 수업은 `Ollama.Ollama`를 쓴다.

| 항목 | 값 |
|---|---|
| 관리자 권한 | 필요 없음 ("The Ollama install does not require Administrator") |
| 실행 파일 | `%LOCALAPPDATA%\Programs\Ollama` — 설치 프로그램이 사용자 PATH에 추가한다 |
| 모델·설정 | `%USERPROFILE%\.ollama` (모델은 그 아래 `models`) |
| 로그 | `%LOCALAPPDATA%\Ollama` — `app.log`, `server.log`, `upgrade.log` |
| 서버 | 설치 후 백그라운드 상주. **로그인 항목으로 등록되어 부팅 때마다 뜬다** |
| API 주소 | `http://127.0.0.1:11434` (기본값. 로컬에서만 접근 가능) |
| 최소 사양 | Windows 10 22H2 이상(Home/Pro). NVIDIA 사용 시 드라이버 551.61 이상 |
| 디스크 | **바이너리만 4 GB 이상.** 모델은 별도 |
| 제거 | Windows 설정 → 앱 및 기능 |

방법 1의 스크립트는 현재 창의 PATH에도 값을 넣어 주므로 그 창에서 바로 `ollama`가 먹는다.
방법 2·3은 설치 프로그램만 PATH를 바꾸므로 **새 창**이 필요하다.

### 디스크가 부족한 PC

설치 위치와 모델 위치는 **각각 따로** 옮겨야 한다. 하나만 바꾸면 나머지는 C 드라이브에 남는다.

```powershell
# 설치 위치 — 설치할 때만 지정할 수 있다
OllamaSetup.exe /DIR="D:\Ollama"

# 모델 위치 — 언제든 바꿀 수 있다. .ollama 가 아니라 그 아래 models 에 해당하는 경로를 준다
[Environment]::SetEnvironmentVariable('OLLAMA_MODELS','D:\ollama\models','User')
```

- 환경변수를 바꾼 뒤에는 **트레이의 Ollama를 Quit 하고 시작 메뉴에서 다시 실행**해야 적용된다. 새 터미널만 열어서는 이미 떠 있는 서버에 반영되지 않는다.
- 공식 절차는 Windows 설정의 "계정의 환경 변수 편집" GUI다. 위 PowerShell 한 줄은 같은 결과를 내는 Microsoft 권장 방식이며 `setx`(1024자 잘림)보다 안전하다.
- 이미 받은 모델이 있으면 옛 경로의 `blobs`와 `manifests`를 **둘 다** 옮긴다. `manifests`를 빠뜨리면 다음 기동 때 `blobs`가 정리되어 사라진다. 실패하면 다시 `ollama pull` 한다.
- 로그와 임시 파일은 계속 C 드라이브를 쓴다. 완전히 비울 수는 없다.

### 수업 전 모델 사전 캐시

모델 ID가 [학기별 환경 기준표](../environment_baseline_template.md)에서 확정된 뒤에만 진행한다. 아래 용량은 2026-09-10 기준 `qwen3` 태그 값이다.

| 태그 | 내려받는 크기 | 용도 |
|---|---:|---|
| `qwen3:8b` | 5.2 GB | 기본 생성 모델 |
| `qwen3:0.6b` | 523 MB | CPU·소형 대체 |
| `bge-m3` | 확정 필요 | Ollama 임베딩(7주차) |

```powershell
ollama pull qwen3:8b
ollama pull qwen3:0.6b
ollama list
```

태그 용량은 재배포될 때 바뀐다. 배포 직전 <https://ollama.com/library/qwen3/tags>에서 다시 확인하고 확인 일자를 환경 기준표에 적는다.

## 승인 후 설치

| 프로그램·항목 | 설치 조건 |
|---|---|
| Python | 담당 교수가 정확한 버전과 uv 설치 방식을 확정한 뒤 |
| NVIDIA 드라이버 | 기존 드라이버가 승인 기준과 다르고 전산실이 변경을 승인한 경우 |
| Python 패키지 | 승인된 `pyproject.toml`과 lock 파일이 제공된 뒤 `uv sync`로 설치 |
| Ollama·Hugging Face 모델 | 정확한 모델 ID·revision·용량·라이선스가 확정된 뒤. 교재 검증용 기본값은 [`weeks/README.md`](weeks/README.md#교재-검증용-기본값) 참조 |
| 수업 전 모델 사전 캐시 | 확정된 모델을 기준 PC에서 먼저 받아 검증한 뒤 나머지 PC에 배분. 실습 시간에 내려받지 않는다 |

## 별도 설치하지 않는 항목

- 전역 `pip install`
- 임의 CUDA Toolkit
- 임의 PyTorch·TensorFlow 버전
- 검색해서 고른 대체 모델

**도구 설치와 모델 설치를 분리한다.** 위의 「설치 절차」 두 절(uv·Ollama)은 도구 설치이므로 기준 PC 한 대에서 먼저 확인한 뒤 진행한다.
아직 TBD로 묶여 있는 것은 **Python 패키지(manifest·lock)와 모델**이며, [학기별 환경 기준표](../environment_baseline_template.md)의 "TBD가 남은 항목은 설치를 시작하지 않는다"는 규칙은 그쪽에 적용된다.

## 설치 확인

```powershell
git --version
code --version
uv --version
ollama --version
nvidia-smi
```

**설치 프로그램의 "성공"이 아니라 새 PowerShell 창의 출력이 기준이다.**

`ollama --version`은 서버 상태에 따라 출력이 다르다. 둘 다 설치는 된 상태다.

| 서버 상태 | 출력 |
|---|---|
| 떠 있음(설치 직후의 정상) | `ollama version is 0.33.3` 한 줄 |
| 꺼져 있음 | `Warning: could not connect to a running Ollama instance` 와 `Warning: client version is 0.33.3` **두 줄. 버전 줄은 나오지 않는다** |

설치 프로그램이 설치 직후 앱을 바로 띄우고 로그인 항목으로도 등록하므로, 보통은 첫 줄 형태가 나온다.
꺼진 상태를 재현하려면 트레이 아이콘에서 Quit 한 뒤 실행한다.

정확한 Python·uv·Ollama·GPU·모델 값은 [학기별 환경 기준표](../environment_baseline_template.md)에서 담당 교수가 확정한다.
