# 모의 실기 A 준비 스크립트 — broken_project 를 복사하고 .env 가 커밋된 Git 이력을 만든다.
# 사용: .\make_broken_repo.ps1 -Destination $HOME\osa-practice\week08-mock-a
# 공개 저장소에는 .env 를 넣을 수 없으므로, "동료가 .env 까지 커밋해 버린 상황"을 이 스크립트가 재현한다.
param(
    [string]$Destination = (Join-Path $HOME "osa-practice\week08-mock-a")
)

$source = Join-Path $PSScriptRoot "broken_project"

if (-not (Test-Path $source)) {
    Write-Host "[오류] broken_project 폴더를 찾을 수 없다: $source"
    exit 1
}
if (Test-Path $Destination) {
    Write-Host "[오류] 대상 폴더가 이미 있다. 다른 이름을 쓰거나 폴더를 지운 뒤 다시 실행한다: $Destination"
    exit 1
}

New-Item -ItemType Directory -Path $Destination | Out-Null
Copy-Item -Path (Join-Path $source "*") -Destination $Destination -Recurse
Set-Location $Destination

# 가짜 값이다. 실제 토큰·비밀번호를 넣지 않는다.
# BOM 없는 UTF-8 로 쓴다. PowerShell 버전에 따라 Set-Content -Encoding utf8 이 BOM 을 붙이면 python-dotenv 가 첫 줄을 경고하기 때문이다.
$envLines = @(
    "# 모의 실기용 가짜 설정 - 실제 값이 아니다",
    "OLLAMA_HOST=http://localhost:11434",
    "OLLAMA_MODEL=qwen3:8b",
    "HF_TOKEN=hf_mock_token_for_exam_practice_only"
)
$envPath = Join-Path $Destination ".env"
$utf8NoBom = New-Object System.Text.UTF8Encoding $false
[System.IO.File]::WriteAllLines($envPath, $envLines, $utf8NoBom)

git init -b main | Out-Null
git add .
git commit -m "Add report script (WIP)" | Out-Null
if ($LASTEXITCODE -ne 0) {
    Write-Host "[오류] commit 에 실패했다. git user.name / user.email 설정을 강의자 안내에 따라 확인한다."
    exit 1
}

Write-Host "[준비 완료] $Destination"
Write-Host "--- git log ---"
git log --oneline
Write-Host "--- git ls-files ---"
git ls-files
Write-Host ""
Write-Host "다음: tasks_A.md 의 A-1 요구사항을 읽고 'uv sync' 부터 시작한다."
