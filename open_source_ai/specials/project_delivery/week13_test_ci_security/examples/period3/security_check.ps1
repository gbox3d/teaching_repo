# 비밀·위험 파일 점검 — Git 이 아는 파일(추적 + 스테이지)에서 토큰 패턴, .env 추적, 모델 파일 형식을 찾는다.
# 사용:  .\security_check.ps1                          # 현재 폴더 점검, outputs\security-*.md 에 기록
#        .\security_check.ps1 -Path C:\classwork\team-a  # 다른 저장소 점검
# 종료 코드: 문제 없음 0, 문제 있음 1
# 발견한 줄의 내용은 출력하지 않는다(비밀을 화면·로그에 다시 남기지 않기 위해). 파일과 줄 번호만 적는다.
param(
    [string]$Path = ".",
    [string]$OutDir = "outputs"
)

$self = "security_check.ps1"
$problems = 0
$report = New-Object System.Collections.Generic.List[string]

function Add-Line([string]$text) {
    $script:report.Add($text)
    Write-Host $text
}

Push-Location $Path
try {
    Add-Line "# 보안 점검 결과"
    Add-Line ""
    Add-Line "- 폴더: $((Get-Location).Path)"
    Add-Line "- 시각: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
    Add-Line ""

    # 1. 대상 파일 — git 이 아는 파일. git 저장소가 아니면 .venv·outputs 등을 뺀 전체 파일.
    $inGit = $false
    $probe = git rev-parse --is-inside-work-tree 2>$null
    if ($probe -eq "true") { $inGit = $true }
    if ($inGit) {
        $files = @(git -c core.quotepath=false ls-files)
    } else {
        $files = @(Get-ChildItem -Recurse -File |
            Where-Object { $_.FullName -notmatch '[\\/](\.venv|\.git|outputs|__pycache__|\.pytest_cache|\.ruff_cache)[\\/]' } |
            ForEach-Object { Resolve-Path -Relative $_.FullName })
    }
    Add-Line "## 1. 대상 파일"
    Add-Line ""
    Add-Line "- git 저장소: $inGit, 파일 수: $($files.Count)"
    Add-Line ""

    # 2. 비밀 파일 — .env 가 git 에 있는가, .gitignore 에 .env 가 있는가
    Add-Line "## 2. 비밀 파일"
    Add-Line ""
    $envTracked = @($files | Where-Object { $_ -match '(^|/)\.env$' })
    if ($envTracked.Count -gt 0) {
        Add-Line "- 문제: .env 가 git 에 올라가 있다 → git rm --cached .env 로 내린다. 이미 push 했다면 그 안의 토큰을 회전한다"
        $problems++
    } else {
        Add-Line "- ok: .env 는 추적되지 않는다"
    }
    if (Test-Path ".gitignore") {
        $ignore = @(Get-Content ".gitignore")
        if ($ignore -contains ".env") { Add-Line "- ok: .gitignore 에 .env 가 있다" }
        else { Add-Line "- 문제: .gitignore 에 .env 줄이 없다"; $problems++ }
    } else {
        Add-Line "- 문제: .gitignore 가 없다"
        $problems++
    }
    Add-Line ""

    # 3. 토큰·비밀 패턴 — 텍스트 파일만, 이 스크립트 자신은 제외
    Add-Line "## 3. 토큰·비밀 패턴"
    Add-Line ""
    $patterns = @(
        @{ Name = "Hugging Face 토큰"; Regex = 'hf_[A-Za-z0-9]{20,}' },
        @{ Name = "GitHub 토큰"; Regex = 'gh[pousr]_[A-Za-z0-9]{20,}' },
        @{ Name = "OpenAI 형식 키"; Regex = 'sk-[A-Za-z0-9_\-]{20,}' },
        @{ Name = "AWS 액세스 키"; Regex = 'AKIA[0-9A-Z]{16}' },
        @{ Name = "개인 키 블록"; Regex = 'BEGIN [A-Z ]*PRIVATE KEY' },
        @{ Name = "비밀번호·키 대입"; Regex = '(?i)(password|passwd|secret|api[_-]?key|token)\s*[=:]\s*\S{8,}' }
    )
    $skipExt = @('.png', '.jpg', '.jpeg', '.gif', '.ico', '.pdf', '.zip', '.gz', '.gguf', '.safetensors', '.bin', '.pt', '.pth', '.pkl', '.ckpt', '.onnx')
    $hits = 0
    foreach ($file in $files) {
        if (-not (Test-Path -LiteralPath $file)) { continue }
        if ((Split-Path $file -Leaf) -eq $self) { continue }
        $ext = [System.IO.Path]::GetExtension($file).ToLower()
        if ($skipExt -contains $ext) { continue }
        foreach ($p in $patterns) {
            $found = @(Select-String -LiteralPath $file -Pattern $p.Regex -AllMatches)
            foreach ($m in $found) {
                $hits++
                Add-Line "- 문제: $($p.Name) 패턴 → $file 줄 $($m.LineNumber)"
            }
        }
    }
    if ($hits -eq 0) { Add-Line "- ok: 토큰·비밀 패턴이 없다" } else { $problems += $hits }
    Add-Line ""

    # 4. 모델 파일 형식과 원격 코드 실행
    Add-Line "## 4. 모델 파일·원격 코드"
    Add-Line ""
    $pickleExt = @('.pkl', '.pickle', '.pt', '.pth', '.bin', '.ckpt')
    $risky = @($files | Where-Object { $pickleExt -contains ([System.IO.Path]::GetExtension($_).ToLower()) })
    foreach ($f in $risky) {
        Add-Line "- 확인 필요: $f — pickle 기반일 수 있는 형식. safetensors·GGUF 를 쓰고 출처를 SOURCES.md 에 적는다. 큰 파일은 Git 에 넣지 않는다"
        $problems++
    }
    $remoteHits = 0
    foreach ($file in $files) {
        if ($file -notlike '*.py') { continue }
        if (-not (Test-Path -LiteralPath $file)) { continue }
        $found = @(Select-String -LiteralPath $file -Pattern 'trust_remote_code\s*=\s*True')
        foreach ($m in $found) {
            $remoteHits++
            Add-Line "- 확인 필요: $file 줄 $($m.LineNumber) trust_remote_code=True — 모델 저장소의 코드를 실행한다. revision 을 고정하고 코드를 읽었는지 기록한다"
        }
    }
    $problems += $remoteHits
    if ($risky.Count -eq 0 -and $remoteHits -eq 0) { Add-Line "- ok: pickle 계열 모델 파일과 trust_remote_code=True 가 없다" }
    Add-Line ""

    # 5. 결과 요약과 기록
    Add-Line "## 결과"
    Add-Line ""
    if ($problems -eq 0) { Add-Line "- 문제 0건. 이 파일을 리뷰 코멘트나 릴리스 점검표에 첨부한다" }
    else { Add-Line "- 문제 $problems 건. 위 항목을 처리한 뒤 다시 실행한다" }

    New-Item -ItemType Directory -Force $OutDir | Out-Null
    $stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
    $outFile = Join-Path $OutDir "security-$stamp.md"
    $report | Set-Content -Path $outFile -Encoding utf8
    Write-Host ""
    Write-Host "기록: $outFile"
}
finally {
    Pop-Location
}

if ($problems -gt 0) { exit 1 } else { exit 0 }
