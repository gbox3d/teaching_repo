# env_check.ps1 — 오픈소스 AI 응용 1주차: 실습환경 점검 스크립트
#
# 사용법(개인 실습 폴더의 복사본에서 실행):
#   .\env_check.ps1
#   .\env_check.ps1 -OutFile env_check_raw.md
# 실행 정책 오류가 나면 정책을 바꾸지 않고 이번 실행만 우회한다:
#   powershell -ExecutionPolicy Bypass -File .\env_check.ps1
#
# 하는 일: git, code, uv, ollama, nvidia-smi 다섯 도구의 버전 문자열을 모아
#          Markdown 표로 출력하고, 실패 항목과 조치 힌트를 따로 표시한다.
# 하지 않는 일: 설치, 설정 변경, 사용자 이름·홈 경로 출력.

param(
    [string]$OutFile = ""
)

$ErrorActionPreference = "Continue"

$tools = @(
    @{ Name = "Git";             Command = "git";        Args = @("--version") },
    @{ Name = "VS Code";         Command = "code";       Args = @("--version") },
    @{ Name = "uv";              Command = "uv";         Args = @("--version") },
    @{ Name = "Ollama";          Command = "ollama";     Args = @("--version") },
    @{ Name = "NVIDIA 드라이버"; Command = "nvidia-smi"; Args = @("--query-gpu=name,memory.total,driver_version", "--format=csv,noheader") }
)

$hints = @{
    "git"        = "Git for Windows 설치 후 새 PowerShell 창을 연다."
    "code"       = "VS Code 설치 때 PATH 추가 옵션이 빠졌을 수 있다. 조교에게 확인하거나 VS Code를 직접 연다."
    "uv"         = "uv 설치 후 새 창을 연다. 설치 경로가 PATH에 들어갔는지 확인한다."
    "ollama"     = "Ollama 설치 후 새 창을 연다. 서버 미기동 경고는 실패가 아니다."
    "nvidia-smi" = "NVIDIA GPU 또는 드라이버가 없다. GPU 없는 PC는 CPU·소형 모델 경로로 진행한다."
}

# 출력 줄 가운데 버전처럼 보이는 첫 줄(숫자.숫자 포함)을 고른다.
function Get-VersionLine {
    param([string[]]$Lines)
    foreach ($line in $Lines) {
        $text = "$line".Trim()
        if ($text -match "\d+\.\d+") { return $text }
    }
    return ""
}

$rows = @()
foreach ($tool in $tools) {
    $found = Get-Command $tool.Command -ErrorAction SilentlyContinue
    if (-not $found) {
        $rows += @{ Name = $tool.Name; Command = $tool.Command; Status = "실패"; Version = "명령을 찾을 수 없음" }
        continue
    }
    $arguments = $tool.Args
    try {
        $output = & $tool.Command @arguments 2>&1
        $version = Get-VersionLine -Lines @($output)
        if ($version) {
            $rows += @{ Name = $tool.Name; Command = $tool.Command; Status = "정상"; Version = $version }
        } else {
            $first = ("$($output | Select-Object -First 1)").Trim()
            $rows += @{ Name = $tool.Name; Command = $tool.Command; Status = "실패"; Version = "버전 문자열 없음: $first" }
        }
    } catch {
        $rows += @{ Name = $tool.Name; Command = $tool.Command; Status = "실패"; Version = "실행 오류: $($_.Exception.Message)" }
    }
}

# Git 사용자 설정은 값이 아니라 설정 여부만 본다(개인정보 출력 금지).
$gitIdentity = "확인 불가(git 없음)"
if (Get-Command git -ErrorAction SilentlyContinue) {
    $gitName = git config user.name 2>$null
    $gitEmail = git config user.email 2>$null
    if ($gitName -and $gitEmail) {
        $gitIdentity = "설정됨(값은 표시하지 않음)"
    } else {
        $gitIdentity = "미설정 - 3교시 commit 전에 강의자 안내에 따라 설정한다"
    }
}

$lines = @()
$lines += "# 실습환경 점검 결과(자동 수집)"
$lines += ""
$lines += "| 도구 | 명령 | 상태 | 버전 문자열 |"
$lines += "|---|---|---|---|"
foreach ($row in $rows) {
    $lines += "| $($row.Name) | ``$($row.Command)`` | $($row.Status) | $($row.Version) |"
}
$lines += ""
$lines += "- Git 사용자 설정(user.name / user.email): $gitIdentity"
$lines += ""

$failed = @($rows | Where-Object { $_.Status -eq "실패" })
if ($failed.Count -eq 0) {
    $lines += "실패 항목 없음."
} else {
    $lines += "## 실패 항목과 조치 힌트"
    $lines += ""
    foreach ($row in $failed) {
        $lines += "- $($row.Name): $($hints[$row.Command])"
    }
}

foreach ($line in $lines) { Write-Output $line }

if ($OutFile) {
    Set-Content -Path $OutFile -Value $lines -Encoding utf8
    Write-Output ""
    Write-Output "저장: $OutFile"
}
