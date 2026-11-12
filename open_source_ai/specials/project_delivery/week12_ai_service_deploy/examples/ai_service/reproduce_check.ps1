# 재현 절차 점검 — 필수 파일, .env 추적 여부, 실행 경로(docker 또는 uv)를 확인한다.
# 사용:  .\reproduce_check.ps1          # 점검만
#        .\reproduce_check.ps1 -Run     # 점검 후 실제로 빌드·실행까지 진행
param(
    [string]$Tag = "osa-ai-service:dev",
    [switch]$Run
)

Write-Host "== 1. 필수 파일"
$required = @("pyproject.toml", ".env.example", ".gitignore", ".dockerignore", "Dockerfile", "README.md", "app/main.py", "app/ollama_client.py", "app/schemas.py")
$missing = 0
foreach ($f in $required) {
    if (Test-Path $f) { Write-Host "  ok       $f" } else { Write-Host "  MISSING  $f"; $missing++ }
}

Write-Host "== 2. 비밀 파일 추적 여부"
if (Test-Path ".git") {
    $tracked = git ls-files .env
    if ($tracked) { Write-Host "  경고     .env 가 git 에 추적되고 있다. git rm --cached .env 로 내린다." } else { Write-Host "  ok       .env 는 추적되지 않는다" }
} else {
    Write-Host "  info     git 저장소가 아니다. git init 후 첫 commit 을 만들고 다시 실행한다."
}
if (Test-Path ".env") { Write-Host "  info     .env 가 로컬에 있다(정상)." } else { Write-Host "  info     .env 가 없다. Copy-Item .env.example .env 로 만든다." }

Write-Host "== 3. 실행 경로"
$docker = Get-Command docker -ErrorAction SilentlyContinue
if ($docker) {
    Write-Host "  docker 발견 -> 컨테이너 경로"
    Write-Host "    docker build -t $Tag ."
    Write-Host "    docker run --rm -p 8000:8000 -e OLLAMA_HOST=http://host.docker.internal:11434 $Tag"
    if ($Run) {
        docker build -t $Tag .
        docker run --rm -p 8000:8000 -e OLLAMA_HOST=http://host.docker.internal:11434 $Tag
    }
} else {
    Write-Host "  docker 없음 -> uv 경로"
    Write-Host "    uv sync"
    Write-Host "    uv run uvicorn app.main:app --port 8000"
    if ($Run) {
        uv sync
        uv run uvicorn app.main:app --port 8000
    }
}

Write-Host "== 4. 확인 방법 (다른 터미널에서)"
Write-Host "    uv run python smoke_test.py --skip-stream"
if ($missing -gt 0) { Write-Host "누락 파일 $missing 개. 위 목록을 먼저 채운다." }
