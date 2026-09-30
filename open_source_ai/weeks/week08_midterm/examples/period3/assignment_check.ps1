# 2차 종합과제 제출 전 검사 — 파일 존재, .gitignore, 추적 파일, 비밀 흔적, working tree 상태를 훑는다.
# 사용: .\assignment_check.ps1 -RepoPath C:\path\to\my-rag-project
# 이 스크립트는 assignment_brief.md 의 "제출 전 검사" 목록 중 기계로 확인할 수 있는 항목만 본다.
param(
    [Parameter(Mandatory = $true)]
    [string]$RepoPath
)

if (-not (Test-Path (Join-Path $RepoPath ".git"))) {
    Write-Host "[오류] Git 저장소가 아니다: $RepoPath"
    exit 1
}
# 검사 동안만 저장소로 이동하고, 끝나면 호출한 폴더로 돌아온다.
Push-Location $RepoPath

$fails = 0

function Report([bool]$ok, [string]$label) {
    if ($ok) {
        Write-Host "[PASS] $label"
    } else {
        Write-Host "[FAIL] $label"
        $script:fails++
    }
}

# 1. 저장소 루트에 있어야 하는 파일
$rootFiles = @("LICENSE", "README.md", ".gitignore", ".env.example", "SOURCES.md")
foreach ($name in $rootFiles) {
    Report (Test-Path $name) "루트 파일 존재: $name"
}

# 2. 저장소 어딘가에 있어야 하는 파일 (.venv 제외)
$anywhere = @("pyproject.toml", "uv.lock", "evalset.json")
foreach ($name in $anywhere) {
    $found = Get-ChildItem -Path . -Recurse -Filter $name -File -ErrorAction SilentlyContinue |
        Where-Object { $_.FullName -notmatch "\\\.venv\\" } |
        Select-Object -First 1
    Report ($null -ne $found) "저장소 안에 존재: $name"
}

# 3. .gitignore 내용
if (Test-Path ".gitignore") {
    $ignore = Get-Content ".gitignore" -Raw
    Report ($ignore -match "(?m)^\.env\r?$") ".gitignore 에 .env 가 있다"
    Report ($ignore -match "(?m)^\.venv/?\r?$") ".gitignore 에 .venv/ 가 있다"
    Report ($ignore -match "(?m)^outputs/?\r?$") ".gitignore 에 outputs/ 가 있다"
}

# 4. 추적 파일에 비밀·환경 폴더가 없는가
$tracked = @(git ls-files)
Report (-not ($tracked -contains ".env")) "추적 파일에 .env 가 없다"
Report (-not ($tracked | Where-Object { $_ -like ".venv/*" })) "추적 파일에 .venv/ 가 없다"
Report (-not ($tracked | Where-Object { $_ -like "*.safetensors" -or $_ -like "*.gguf" -or $_ -like "*.bin" })) "추적 파일에 모델 가중치가 없다"

# 5. 이력에 토큰 패턴이 없는가 (패턴만 검사한다. 실제 값은 출력하지 않는다)
$history = @(git log --all -p)
$patterns = @("hf_[A-Za-z0-9]{20,}", "ghp_[A-Za-z0-9]{20,}", "sk-[A-Za-z0-9]{20,}")
foreach ($p in $patterns) {
    $hit = $history | Select-String -Pattern $p -Quiet
    Report (-not $hit) "이력에 토큰 패턴이 없다: $p"
}

# 6. working tree 상태
$dirty = @(git status --porcelain)
Report ($dirty.Count -eq 0) "working tree 가 clean 이다"

Pop-Location
Write-Host ""
if ($fails -eq 0) {
    Write-Host "모든 항목 통과. assignment_brief.md 의 제출 전 검사 목록을 이어서 확인한다."
    exit 0
} else {
    Write-Host "FAIL $fails 건. 조치 후 다시 실행한다."
    exit 1
}
