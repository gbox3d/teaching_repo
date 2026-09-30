# reproduce_check.ps1 — 깨끗한 폴더에서 uv 프로젝트를 재현한다.
#
# 무엇을 하는가
#   1. 원본 저장소를 새 폴더에 git clone 한다. (.venv, .env, outputs/ 는 커밋되지 않았으므로 따라오지 않는다)
#   2. 그 폴더에서 uv sync --locked 를 실행해 프로젝트 선언과 lock을 검증하고 설치한다.
#   3. 확인 명령을 실행하고, 결과를 현재 폴더의 outputs/reproduce-<시각>.md 에 기록한다.
#
# 사용법 (PowerShell 7 권장. 한글이 깨지면 pwsh 로 실행한다)
#   .\reproduce_check.ps1 -Source C:\classwork\osa-practice
#   .\reproduce_check.ps1 -Source C:\classwork\osa-practice -Check 'uv run --locked oss-tool greet --name student01'
#   .\reproduce_check.ps1 -Source C:\classwork\osa-practice -Dest C:\classwork\_repro\osa-practice -Keep
#
# -Keep 을 주지 않으면 검사 후 복제 폴더를 지운다. 종료 코드 0 이면 모든 단계 통과.
# -Check 는 직접 검토한 명령만 지정한다. uv 명령에는 --locked 를 유지한다.

param(
    [Parameter(Mandatory = $true)]
    [string]$Source,
    [string]$Dest = "",
    [string]$Check = 'uv run --locked python -c "import sys; print(sys.version)"',
    [switch]$Keep
)

$stamp = Get-Date -Format "yyyyMMdd-HHmmss"
if ($Dest -eq "") {
    $Dest = Join-Path ([System.IO.Path]::GetTempPath()) "osa-repro-$stamp"
}
if (Test-Path $Dest) {
    Write-Host "대상 폴더가 이미 있다: $Dest — 비어 있는 새 경로를 지정한다."
    exit 1
}

$outDir = Join-Path (Get-Location).Path "outputs"
New-Item -ItemType Directory -Force -Path $outDir | Out-Null
$logPath = Join-Path $outDir "reproduce-$stamp.md"

$lines = New-Object System.Collections.Generic.List[string]
$lines.Add("# 재현 검사 $stamp")
$lines.Add("")
$lines.Add("- 원본: $Source")
$lines.Add("- 대상: $Dest")
$lines.Add("- 확인 명령: $Check")
$lines.Add("")

function Add-Result([string]$title, [bool]$ok, [string]$detail) {
    $mark = "FAIL"
    if ($ok) { $mark = "OK" }
    Write-Host "[$mark] $title"
    $script:lines.Add("## $title — $mark")
    $script:lines.Add("")
    $script:lines.Add('```text')
    $script:lines.Add($detail.TrimEnd())
    $script:lines.Add('```')
    $script:lines.Add("")
}

# 1. clone — 커밋된 것만 따라온다
$cloneOut = (git clone --quiet $Source $Dest 2>&1 | Out-String)
$cloneOk = ($LASTEXITCODE -eq 0)
Add-Result "1. git clone" $cloneOk $cloneOut
if (-not $cloneOk) {
    [System.IO.File]::WriteAllLines($logPath, $lines)
    Write-Host "기록: $logPath"
    exit 1
}

# 2. 복제본 점검 — .venv 와 .env 는 없어야 하고 uv.lock 은 있어야 한다
$hasVenv = Test-Path (Join-Path $Dest ".venv")
$hasEnv = Test-Path (Join-Path $Dest ".env")
$hasLock = Test-Path (Join-Path $Dest "uv.lock")
$inventory = ".venv 존재: $hasVenv`n.env 존재: $hasEnv`nuv.lock 존재: $hasLock"
$inventoryOk = ((-not $hasVenv) -and (-not $hasEnv) -and $hasLock)
Add-Result "2. 복제본 점검 (.venv 없음, .env 없음, uv.lock 있음)" $inventoryOk $inventory

# 3. 선언과 uv.lock 을 검증한다. 앞 단계 실패를 자동 갱신으로 덮지 않는다.
$syncOk = $false
$checkOk = $false
if ($inventoryOk) {
    Push-Location $Dest
    try {
        $syncOut = (uv sync --locked 2>&1 | Out-String)
        $syncOk = ($LASTEXITCODE -eq 0)
        Add-Result "3. uv sync --locked" $syncOk $syncOut

        # 4. sync 가 성공했을 때만 복제본의 환경에서 실행한다.
        if ($syncOk) {
            $checkOut = (Invoke-Expression $Check 2>&1 | Out-String)
            $checkOk = ($LASTEXITCODE -eq 0)
            Add-Result "4. 확인 명령: $Check" $checkOk $checkOut
        } else {
            Add-Result "4. 확인 명령: $Check" $false "SKIP: lock 검증 또는 환경 설치 실패"
        }
    } finally {
        Pop-Location
    }
} else {
    Add-Result "3. uv sync --locked" $false "SKIP: 복제본 점검 실패"
    Add-Result "4. 확인 명령: $Check" $false "SKIP: 복제본 점검 실패"
}

[System.IO.File]::WriteAllLines($logPath, $lines)
Write-Host "기록: $logPath"

if (-not $Keep) {
    Remove-Item -Recurse -Force $Dest
    Write-Host "복제 폴더 삭제: $Dest (-Keep 을 주면 유지)"
}

if ($cloneOk -and $inventoryOk -and $syncOk -and $checkOk) {
    exit 0
}
exit 1
