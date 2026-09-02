# reproduce_by_stranger.ps1 — 처음 보는 사람이 README 만 보고 재현하는 절차를 단계별 시간과 함께 기록한다.
#
# 사용 (네트워크 있음):
#   .\reproduce_by_stranger.ps1 -Source https://github.com/team-b/local-ai-helper -Tag v0.1.0
# 사용 (네트워크 없음, 짝 팀 로컬 경로):
#   .\reproduce_by_stranger.ps1 -Source C:\classwork\team-b-repo -Tag v0.1.0
#
# 결과: <WorkDir>\repro-<시각>\ 에 clone 하고, <WorkDir>\repro-log-<시각>.md 에 단계·초·결과를 남긴다.
# 이 스크립트는 clone → checkout → uv sync --frozen → (tests 가 있으면) pytest 까지만 한다.
# README 「실행」 절의 명령은 사람이 직접 실행하고 결과를 기록 파일 아래에 적는다.

param(
    [Parameter(Mandatory = $true)][string]$Source,
    [string]$Tag = "v0.1.0",
    [string]$WorkDir = "repro"
)

$started = Get-Date
$stamp = Get-Date -Format "yyyyMMdd-HHmmss"
New-Item -ItemType Directory -Path $WorkDir -Force | Out-Null
$workAbs = (Resolve-Path $WorkDir).Path
$target = Join-Path $workAbs "repro-$stamp"
$log = Join-Path $workAbs "repro-log-$stamp.md"

function Invoke-Step {
    param([string]$Name, [scriptblock]$Action)
    $t0 = Get-Date
    Write-Host "== $Name"
    & $Action | Out-Host
    $ok = ($LASTEXITCODE -eq 0)
    $sec = [int]((Get-Date) - $t0).TotalSeconds
    $result = if ($ok) { "성공" } else { "실패" }
    Add-Content -Path $log -Encoding utf8 -Value "| $Name | $sec | $result |  |"
    return $ok
}

$header = @(
    "# 교차 재현 기록 ($stamp)",
    "",
    "- 대상: $Source",
    "- 태그: $Tag",
    "- 규칙: README 외의 것을 묻지 않는다. 막힌 곳이 곧 README 의 결함이다.",
    "",
    "| 단계 | 초 | 결과 | 막힌 곳·README 위치 |",
    "|---|---:|---|---|"
)
Set-Content -Path $log -Encoding utf8 -Value $header

if (-not (Invoke-Step "git clone" { git clone --quiet $Source $target })) {
    Write-Host "clone 실패. 주소·권한·네트워크를 확인한다. 기록: $log"
    exit 1
}

Push-Location $target
try {
    if (-not (Invoke-Step "git checkout $Tag" { git checkout --quiet $Tag })) {
        Write-Host "태그 $Tag 가 없다. 릴리스 태그가 push 되었는지 확인한다. 기록: $log"
        exit 1
    }
    if (-not (Invoke-Step "uv sync --frozen" { uv sync --frozen })) {
        Write-Host "uv sync --frozen 실패. 저장소에 uv.lock 이 있는지 확인한다. 기록: $log"
        exit 1
    }
    if (Test-Path ".env.example") {
        Copy-Item ".env.example" ".env"
        Write-Host "== .env.example 을 .env 로 복사했다 (값은 README 에 따라 채운다)"
    }
    if (Test-Path "tests") {
        Invoke-Step "uv run pytest -q" { uv run pytest -q } | Out-Null
    }
}
finally {
    Pop-Location
}

$total = [int]((Get-Date) - $started).TotalSeconds
$footer = @(
    "",
    "총 소요: $total 초 (목표 600 초 이내, README 실행 명령 포함)",
    "",
    "## README 실행 명령 결과",
    "",
    "- 실행한 명령:",
    "- 결과(성공/실패)와 첫 출력 3줄:",
    "- 막힌 곳과 README 의 어느 절인지:"
)
Add-Content -Path $log -Encoding utf8 -Value $footer
Write-Host "기록: $log (여기까지 $total 초). 이제 $target 에서 README 「실행」 절의 명령을 직접 실행한다."
