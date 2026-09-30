# uv 프로젝트를 GitHub로 배포하기

## 목차

- [무엇을 함께 배포하는가](#무엇을-함께-배포하는가)
- [예제에 적용하는 gitignore](#예제에-적용하는-gitignore)
- [복사와 ZIP 배포 시 주의할 점](#복사와-zip-배포-시-주의할-점)
- [배포자와 받는 사람의 실행 순서](#배포자와-받는-사람의-실행-순서)
- [커밋 전에 제외 규칙 확인하기](#커밋-전에-제외-규칙-확인하기)
- [이미 추가한 파일 처리하기](#이미-추가한-파일-처리하기)
- [모델과 데이터 배포하기](#모델과-데이터-배포하기)
- [5분 확인 실습](#5분-확인-실습)

GitHub에 공유할 것은 **소스와 환경을 다시 만드는 데 필요한 기록**이다. 받는 사람은 그 기록으로 자기 PC의 `.venv/`를 만든다. uv 설치·환경 관리 명령은 [uv 사용 가이드](uv_guide.md)를 함께 본다.

## 무엇을 함께 배포하는가

| 파일·폴더 | Git에 포함 | 이유 |
|---|---|---|
| `pyproject.toml` | 예 | Python 지원 범위, 의존성, 실행 명령, 빌드 설정 |
| `uv.lock` | 예 | 검증한 패키지 해석 결과를 다른 PC에서도 사용 |
| `.python-version` | 예 | 프로젝트에서 사용할 Python 버전 힌트. 수업 기준에 맞춰 생성 |
| 소스, 테스트, `README.md`, 라이선스 | 예 | 실행·검증 방법과 재사용 조건 |
| `.gitignore`, `.env.example` | 예 | 제외 규칙과 비밀 값이 없는 설정 양식 |
| 작고 공개 가능한 입력 예제 | 예 | 네트워크·토큰 없이도 실습을 시작하는 재료 |
| `.venv/` | 아니요 | 각 PC에서 재생성할 가상환경. OS와 경로에도 의존 |
| Python·uv·모델 다운로드 캐시 | 아니요 | 다시 받을 수 있는 파일. 환경 명세가 아님 |
| 실제 `.env`, `.env.local`, `.env.production` | 아니요 | 토큰·개인 경로·PC별 설정이 들어갈 수 있음 |
| 실행 결과, 다운로드한 모델, 학습 산출물 | 보통 아니요 | 용량·개인정보·재배포 권한을 검토해 별도 배포 |

`uv.lock`은 캐시가 아니다. `.venv/`와 캐시는 지워도 다시 만들 수 있지만, lock 파일을 빼면 받는 시점에 다른 패키지 조합이 선택될 수 있다. `*.lock`을 통째로 제외하지 않는다. uv도 프로젝트의 `uv.lock`을 버전 관리하도록 안내한다. [uv 프로젝트 파일 설명](https://docs.astral.sh/uv/guides/projects/)

이 교재의 예제는 환경 기준표 확정 후 기준 PC에서 `uv.lock`을 생성하는 정책이다. **현재 lock 파일이 없는 원본과, 검증한 lock 파일을 포함한 배포본을 구분한다.** 배포본을 준비할 때는 해당 예제 폴더에서 lock을 만들고 실행을 확인한 뒤 포함한다. `.python-version`만으로 모든 패키지 버전이 고정되지는 않는다.

## 예제에 적용하는 gitignore

독립 Python 예제 폴더의 `.gitignore`에는 다음 항목을 둔다. 이미 있는 규칙은 유지하고 빠진 항목만 추가한다.

```gitignore
# 각 PC에서 다시 만드는 환경·캐시
.venv/
__pycache__/
*.pyc
.uv-cache/
.cache/
.ruff_cache/
.pytest_cache/

# 실제 설정은 제외하고 비밀 없는 양식만 공유
.env
.env.*
!.env.example

# 실행·학습·빌드 산출물
outputs/
models/
adapters/
build/
dist/
*.egg-info/
```

`!.env.example`은 앞의 `.env.*` 규칙에서 양식 파일만 다시 포함시키는 예외다. `.env.example`에는 `HF_TOKEN=`처럼 빈 값이나 명백한 예시만 적는다. **이름에 example이 붙었다고 실제 토큰이 안전해지는 것은 아니다.** [Git 제외 패턴 규칙](https://git-scm.com/docs/gitignore)

캐시 위치를 직접 바꿨다면 실제 경로도 확인한다. 예를 들어 프로젝트 안에 `hf-cache/`를 만들었다면 그 디렉터리를 별도로 제외한다. 위 규칙이 사용자 지정 캐시 경로를 모두 찾아 주지는 않는다.

`*.json`, `*.csv`, `data/`를 일괄 제외하지 않는다. 이 교재에는 `data/sample_qa.jsonl`, `data/sample_sft.jsonl`, `data/eval_prompts.json`, 평가용 JSON 등 **배포해야 하는 입력 자료**가 있다. 비공개 원자료는 `private_data/`처럼 별도 경로로 분리해 그 경로만 제외하고, 공유 가능한 작은 샘플은 소스와 함께 둔다.

## 복사와 ZIP 배포 시 주의할 점

- 이 저장소 안에서는 상위 `teaching_repo/.gitignore`도 적용된다. 예제 폴더만 다른 곳에 복사하면 그 상위 규칙은 따라오지 않는다. 그래서 각 Python 예제에도 독립 `.gitignore`를 둔다. [Git 제외 규칙의 적용 범위](https://git-scm.com/docs/gitignore)
- `.gitignore`, `.env.example`, `.python-version`, `.github/`처럼 점으로 시작하는 파일·폴더를 빠뜨리지 않는다. macOS·Linux에서 `cp source/* target/`은 일반적으로 숨김 파일을 빼므로 폴더 전체를 복사하고 목록을 확인한다.
- Windows PowerShell에서는 `Get-ChildItem -Force`, macOS·Linux에서는 `ls -la`로 숨김 파일을 확인한다. 파일 탐색기의 표시 설정도 확인한다.
- 전체 폴더를 복사하거나 직접 ZIP으로 묶으면 `.gitignore`가 제외하는 `.env`, `.venv/`, 모델, 출력까지 들어갈 수 있다. **`.gitignore`는 복사·압축 도구의 필터가 아니다.** 직접 만든 압축 파일은 내용 목록을 검사한다.
- GitHub의 **Download ZIP / Source code (zip)**은 선택한 커밋의 소스 스냅샷이다. Git 이력과 `.git/`는 없으며, 로컬에서 아직 커밋하지 않은 `uv.lock`도 들어가지 않는다. 커밋된 숨김 파일은 포함 대상이다. ZIP을 받은 사람은 Git 명령보다 파일 확인과 `uv sync`부터 진행한다. [GitHub 소스 압축 파일](https://docs.github.com/en/repositories/working-with-files/using-files/downloading-source-code-archives)
- 개인 PC의 전역 ignore와 `.git/info/exclude`는 clone으로 공유되지 않는다. 팀에 필요한 규칙은 저장소의 `.gitignore`에 적는다.

독립 저장소를 만들 때는 수업 자료 저장소 **밖의 별도 폴더**로 예제를 복사한다. 이미 Git 저장소 안에서 작업 중이면 `git rev-parse --show-toplevel`로 실제 저장소 루트를 확인한다. 예제마다 무심코 `git init`해 중첩 저장소를 만들지 않는다.

## 배포자와 받는 사람의 실행 순서

아래 예시는 3주차 [`period3`](weeks/week03_reproducible_python/examples/period3/)을 독립 폴더로 복사해 배포하는 경우다. 모든 명령은 **그 폴더의 `pyproject.toml` 옆에서** 실행한다. 현재 예제는 Python 3.12 이상을 요구하므로, 수업 기준이 3.12일 때 다음과 같이 준비한다.

### 배포자: 실행을 확인하고 환경 파일을 포함한다

```sh
uv python pin 3.12
uv lock
uv sync --locked
uv run --locked oss-tool greet --name student01
```

`uv lock`은 의존성을 해석하고, `uv sync --locked`는 lock 파일이 현재 설정과 맞는지 확인하며 설치한다. 배포할 lock 파일이 이미 있으면 먼저 `uv sync --locked`로 검증한다. 일상적인 배포 준비에 `uv lock --upgrade`를 섞으면 의도치 않은 패키지 갱신이 될 수 있다. [uv lock·sync 동작](https://docs.astral.sh/uv/concepts/projects/sync/)

README에는 다음 내용을 적는다.

1. 검증한 Python·uv 버전, OS와 GPU 조건
2. 설치 위치와 실행 명령, 기대 결과
3. 필요한 환경변수와 `.env.example`에서 `.env`를 만드는 방법
4. 모델 ID·리비전·다운로드 크기·라이선스와 CPU 대체 경로
5. lock 파일 포함 여부와 재현에 필요한 외부 서비스

이제 개인 배포 폴더가 아직 Git 저장소가 아니라면 그곳에서만 `git init`한다. 이 3교시 프로젝트를 기준으로 다음 파일을 지정해 추가하고, 아래의 점검 절을 마친 뒤 커밋한다.

```sh
git add .gitignore .env.example .python-version pyproject.toml uv.lock README.md src
git diff --cached --stat
git diff --cached
git commit -m "uv 실행 환경과 예제 소스 추가"
```

다른 프로젝트의 `tests/`, 공개 샘플, 라이선스 파일도 필요한 경로를 지정해 추가한다. `uv.lock`은 자동 생성 파일이라도 리뷰한다. 저장소 URL 등에 자격증명이나 공유할 수 없는 내부 주소가 들어갔는지 살핀다.

### 받는 사람: lock 파일로 자기 환경을 만든다

clone 또는 압축 해제 후 배포된 예제 폴더로 이동한다.

```sh
uv sync --locked
uv run --locked oss-tool greet --name student02
uv run --locked oss-tool sysinfo --json
```

가상환경 활성화는 필요 없다. `.env`가 필요한 기능은 `.env.example`을 복사해 자기 값을 넣는다. PowerShell에서는 `Copy-Item .env.example .env`, macOS·Linux에서는 `cp .env.example .env`를 쓴다. `uv run` 자체가 모든 프로젝트의 `.env`를 자동으로 읽는 것은 아니다. 이 예제는 코드가 `python-dotenv`로 읽으며, 다른 예제는 README의 로딩 방법을 따른다.

lock 파일이 없는 **교재 원본**은 `uv sync`로 처음 해석한다. 이는 배포자가 검증한 패키지 조합을 복원하는 것과 다르다. `--locked` 실패를 무조건 옵션을 빼서 해결하지 말고, lock 누락인지 `pyproject.toml`과의 불일치인지 먼저 확인한다. 자세한 차이는 [uv 사용 가이드](uv_guide.md)를 본다.

## 커밋 전에 제외 규칙 확인하기

예제 폴더가 Git 저장소 안에 있을 때 다음 명령으로 **원인 규칙, 추적 상태, 커밋 후보**를 각각 확인한다. PowerShell과 macOS·Linux에서 동일하게 쓸 수 있다.

```sh
# 어떤 파일의 몇 번째 규칙이 적용되는가?
git check-ignore -v .venv/ .env .env.local outputs/ .uv-cache/

# 이미 추적 중인 파일도 포함해 규칙 자체를 진단
git check-ignore -v --no-index .env.example uv.lock .python-version

# 현재 추적하거나 새로 스테이징한 경로 확인
git ls-files

# 추적 중인데 제외 규칙에도 걸리는 파일: 실수로 올린 환경·비밀 확인
git ls-files -ci --exclude-standard

# 이번 커밋에 들어갈 내용 확인
git status --short
git diff --cached --stat
git diff --cached
```

`git check-ignore -v` 출력의 `!.env.example`은 **제외 해제**를 뜻한다. 출력이 있다는 이유만으로 모두 무시된다고 해석하지 않는다. 기본 명령은 이미 추적하는 파일을 건너뛰므로 규칙만 조사할 때 `--no-index`를 쓴다. `uv.lock`과 `.python-version`에 적용되는 패턴이 없다면 해당 명령에서 출력되지 않는 것이 정상이다. [git check-ignore 설명](https://git-scm.com/docs/git-check-ignore)

`git ls-files -ci --exclude-standard`가 출력되면 자동 삭제하지 말고 경로를 검토한다. 이미 의도적으로 추적한 파일도 나올 수 있다. 또한 `git diff --cached`에는 비밀 값이 보일 수 있으므로 공개 화면이나 수업 채팅에 그대로 붙이지 않는다. [git ls-files 옵션](https://git-scm.com/docs/git-ls-files)

## 이미 추가한 파일 처리하기

`.gitignore`를 나중에 고쳐도 **이미 추적 중인 파일은 자동으로 추적 해제되지 않는다.** 파일의 상태에 따라 처리한다.

| 상태 | 조치 |
|---|---|
| 아직 `git add`하지 않음 | `.gitignore`를 먼저 작성하고 `git status`로 확인 |
| 실수로 새 파일을 `git add`했지만 아직 커밋 전 | 기존 커밋이 있는 저장소에서는 `git restore --staged -- .env`로 스테이징만 취소 |
| 최초 커밋 전이라 `HEAD`가 없음 | `git rm --cached -- .env`로 인덱스에서 빼고 ignore 규칙 추가 |
| 이전 커밋부터 추적하던 파일 | `git rm --cached -- .env`로 다음 커밋에서 추적 해제. 로컬 파일은 유지 |
| `.venv/` 전체를 이미 추적함 | 경로를 확인한 뒤 `git rm -r --cached -- .venv/`로 해당 폴더만 추적 해제 |

`git restore --staged`는 스테이징만 되돌리며, 이전부터 추적하던 파일을 계속 무시하게 만드는 명령은 아니다. `git rm --cached` 뒤에는 `.gitignore` 변경과 파일 추적 해제를 함께 커밋한다. 대상을 확인하지 않고 `git rm -r --cached .`로 저장소 전체 인덱스를 비우지 않는다. [git restore](https://git-scm.com/docs/git-restore), [git rm](https://git-scm.com/docs/git-rm)

토큰·API 키를 이미 커밋했다면 파일 삭제나 ignore 추가만으로 해결되지 않는다. 노출된 키를 발급처에서 **먼저 폐기·회전**하고, 사용 내역과 과거 커밋의 잔존 여부를 점검한다. 이력 정리가 필요하면 팀원과 협의해 진행한다. 과거 커밋을 수정해도 다른 사람의 clone·fork·복사본까지 회수되는 것은 아니다. [GitHub 민감 데이터 제거 안내](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository)

## 모델과 데이터 배포하기

AI 프로젝트의 재현성에는 Python 패키지 외에 모델과 데이터 버전도 필요하다. 큰 파일 자체 대신 README나 다운로드 스크립트에 **출처 URL, 모델 ID, 리비전 또는 체크섬, 라이선스, 예상 용량**을 기록한다. 인증이 필요하면 토큰 발급 방법을 안내하되 토큰은 포함하지 않는다.

GitHub의 일반 Git 저장소는 100 MiB를 초과하는 파일을 차단한다. 모델 가중치·대규모 데이터는 권한과 용도에 따라 Hugging Face Hub, Git LFS, 릴리스 첨부 파일 등 별도 배포 위치를 선택한다. Git LFS를 쓴다면 저장소에 `.gitattributes`를 포함하고, 다운로드 방법과 저장·대역폭 조건도 확인한다. **Git LFS도 비밀이나 개인정보를 숨기는 장치가 아니다.** [GitHub 대용량 파일 안내](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github)

평가 결과를 보고서에 넣어야 한다면 `outputs/` 전체를 강제로 추가하기보다 공개 가능한 결과만 검토·익명화해 `docs/results/` 같은 배포 경로에 옮긴다. 모델을 Git에서 제외했다는 이유만으로 데이터의 재배포 권한이 생기지는 않는다.

## 5분 확인 실습

개인 연습 저장소에서 실제 토큰 없이 진행한다.

1. `.env.local`에 `DEMO_VALUE=local-only`, `.env.example`에 `DEMO_VALUE=`를 넣는다.
2. `.gitignore`의 `.env.*`와 `!.env.example` 순서를 확인한다.
3. `git check-ignore -v --no-index .env.local .env.example`을 실행하고 두 출력의 차이를 설명한다.
4. `git status --short`에서 새 `.env.local`이 커밋 후보로 나오지 않는지 확인한다. 이미 추적했다면 위 처리 절을 적용한다.
5. `uv.lock`, `.python-version`, 소스, 작은 입력 예제를 받는 사람이 확보할 수 있는지 확인한다.
6. 배포할 Git 커밋을 별도 폴더로 clone하거나 GitHub 소스 ZIP을 받아, **기존 `.venv/` 없이** `uv sync --locked`와 README의 실행 명령을 확인한다. ZIP에서 `.env`가 없고 `.env.example`이 있는지도 확인한다.

성공 기준은 "내 PC에서 실행된다"에 더해, **받는 사람이 환경을 재생성하고 동일한 예제를 실행할 수 있으며 비밀·환경 폴더가 배포물에 들어가지 않는다**는 것이다.
