# 15주차 교차 재현 검증 — clone → 태그 checkout → uv sync --frozen → pytest → verify_release.py 를 한 번에 실행한다.
# README 절차대로 실제 기능을 실행하는 단계는 자동화하지 않는다. 그 단계는 사람이 직접 하고 체크리스트에 기록한다.
#
# 사용 예 (이 스크립트가 있는 폴더에서):
#   .\cross_review.ps1 -RepoUrl https://github.com/<org>/<repo>.git -Team team-a -Tag v0.1.0
#   .\cross_review.ps1 -RepoUrl C:\path\to\local-repo -Team team-b
#
# 결과: outputs\cross-review-<Team>-<시각>.log 와 verify_release.py 의 outputs\verify-<Team>-*.md / .json

param(
    [Parameter(Mandatory = $true)][string]$RepoUrl,
    [string]$Team = "team-a",
    [string]$Tag = "",
    [string]$WorkDir = "review"
)

$ErrorActionPreference = "Continue"
# 한글 로그가 깨지지 않도록 콘솔·Python 출력을 UTF-8로 맞춘다.
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$env:PYTHONIOENCODING = "utf-8"
$toolDir = $PSScriptRoot
$logDir = Join-Path $toolDir "outputs"
$stamp = Get-Date -Format "yyyyMMdd-HHmmss"
$log = Join-Path $logDir "cross-review-$Team-$stamp.log"

New-Item -ItemType Directory -Force -Path $logDir | Out-Null
New-Item -ItemType Directory -Force -Path $WorkDir | Out-Null
$target = Join-Path (Resolve-Path $WorkDir).Path $Team

function Step([string]$Title) {
    $line = "=== $Title ==="
    Write-Host $line
    Add-Content -Path $log -Value $line
}

Step "0. 대상: $RepoUrl -> $target (태그: $Tag)"

if (Test-Path $target) {
    Step "중단: $target 이 이미 있다. 폴더를 지우거나 -Team 값을 바꾼 뒤 다시 실행한다."
    exit 1
}

Step "1. git clone"
git clone $RepoUrl $target 2>&1 | Tee-Object -FilePath $log -Append
if ($LASTEXITCODE -ne 0) {
    Step "clone 실패 — URL·네트워크·권한을 확인하고 환경 문제인지 기록한다."
    exit 1
}

if ($Tag -ne "") {
    Step "1-1. git checkout $Tag"
    git -C $target checkout $Tag 2>&1 | Tee-Object -FilePath $log -Append
    if ($LASTEXITCODE -ne 0) {
        Step "태그 checkout 실패 — 릴리스 태그가 없으면 릴리스 결함으로 기록한다."
    }
}

Push-Location $target

Step "2. uv sync --frozen"
uv sync --frozen 2>&1 | Tee-Object -FilePath $log -Append
$syncCode = $LASTEXITCODE
if ($syncCode -ne 0) {
    Step "sync 실패 (exit $syncCode) — uv.lock 없음/불일치는 릴리스 결함, 네트워크·캐시 문제는 환경 문제로 구분해 기록한다."
}

Step "3. uv run --frozen pytest"
if (Test-Path "tests") {
    # --frozen: lock을 새로 만들지 않는다. lock이 없으면 여기서도 실패하는 것이 맞다(2단계와 같은 릴리스 결함).
    # 없이 실행하면 uv가 clone 폴더에 새 uv.lock을 만들어 '재현'이 아니라 '새 설치'가 되고, 4단계 검사가 오염된다.
    uv run --frozen pytest -q 2>&1 | Tee-Object -FilePath $log -Append
    Step "pytest exit code: $LASTEXITCODE"
}
else {
    Step "tests/ 폴더 없음 — 13주차 테스트가 없는 릴리스. 체크리스트에 기록한다."
}

Pop-Location

Step "4. verify_release.py"
Push-Location $toolDir
uv run python verify_release.py --repo $target --team $Team 2>&1 | Tee-Object -FilePath $log -Append
Step "verify exit code: $LASTEXITCODE"
Pop-Location

Step "5. 남은 일: README 재현 절차대로 직접 실행하고 결과를 reviewer_checklist.md 에 기록한다."
Step "로그: $log"
