# 오픈소스 AI 응용 실습조교용 설치 프로그램 목록

## 목차

- [필수 설치](#필수-설치)
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

## 승인 후 설치

| 프로그램·항목 | 설치 조건 |
|---|---|
| Python | 담당 교수가 정확한 버전과 uv 설치 방식을 확정한 뒤 |
| NVIDIA 드라이버 | 기존 드라이버가 승인 기준과 다르고 전산실이 변경을 승인한 경우 |
| Python 패키지 | 승인된 `pyproject.toml`과 lock 파일이 제공된 뒤 `uv sync`로 설치 |
| Ollama·Hugging Face 모델 | 정확한 모델 ID·revision·용량·라이선스가 확정된 뒤 |

## 별도 설치하지 않는 항목

- 전역 `pip install`
- 임의 CUDA Toolkit
- 임의 PyTorch·TensorFlow 버전
- 검색해서 고른 대체 모델

현재 manifest·lock·모델 기준이 없으므로 전체 실습환경 설치는 아직 TBD다.

## 설치 확인

```powershell
git --version
code --version
uv --version
ollama --version
nvidia-smi
```

정확한 Python·uv·Ollama·GPU·모델 값은 [학기별 환경 기준표](../environment_baseline_template.md)에서 담당 교수가 확정한다.
