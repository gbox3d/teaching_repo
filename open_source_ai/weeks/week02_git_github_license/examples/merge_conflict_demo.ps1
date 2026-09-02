<#
merge_conflict_demo.ps1 — 같은 줄 충돌을 재현하는 명령 순서

1교시 실습에서 손으로 하는 절차를 그대로 스크립트로 옮긴 것이다.
각 단계의 git 명령을 읽으면서 실행 결과와 대응시킨다.

사용법 (PowerShell 7 권장):
  pwsh -ExecutionPolicy Bypass -File .\merge_conflict_demo.ps1
      현재 폴더 아래에 conflict-demo 저장소를 만들고 충돌 상태에서 멈춘다.
  pwsh -ExecutionPolicy Bypass -File .\merge_conflict_demo.ps1 -Path C:\practice
      지정한 폴더 아래에 만든다.
  pwsh -ExecutionPolicy Bypass -File .\merge_conflict_demo.ps1 -AutoResolve
      충돌 해결과 merge commit까지 자동으로 수행한다(관찰용).

주의:
  - 수업 자료 저장소 안에서 실행하지 않는다. 별도 연습 폴더에서 실행한다.
  - 사용자 이름·이메일은 만들어진 저장소 안에서만 유효하게 설정한다(전역 설정 변경 없음).
  - 파일 내용은 콘솔 코드페이지와 무관하게 보이도록 영문으로 둔다.
#>
param(
    [string]$Path = (Get-Location).Path,
    [string]$Name = "conflict-demo",
    [switch]$AutoResolve
)

$ErrorActionPreference = "Continue"
if (Test-Path variable:PSNativeCommandUseErrorActionPreference) {
    $PSNativeCommandUseErrorActionPreference = $false
}

$repo = Join-Path $Path $Name
if (Test-Path $repo) {
    Write-Host "이미 존재한다: $repo"
    Write-Host "폴더를 지우거나 -Name 으로 다른 이름을 준다."
    exit 1
}

$readmePath = Join-Path $repo "README.md"

function Write-Step([string]$Title) {
    Write-Host ""
    Write-Host ("=" * 60)
    Write-Host $Title
    Write-Host ("=" * 60)
}

# ---------------------------------------------------------------
# 1단계 · 저장소 만들기 (1주차 3교시의 git init에 해당)
# ---------------------------------------------------------------
Write-Step "1단계 · git init, main branch, 저장소 안 사용자 설정"
New-Item -ItemType Directory -Path $repo | Out-Null
Push-Location $repo
git init -q
git branch -M main
git config user.name "student01"
git config user.email "student01@example.com"

# ---------------------------------------------------------------
# 2단계 · main 첫 commit — README 2번째 줄이 나중에 충돌하는 줄이다
# ---------------------------------------------------------------
Write-Step "2단계 · main 첫 commit (Add README)"
[System.IO.File]::WriteAllLines($readmePath, @(
    "# conflict-demo",
    "This repository is a practice sandbox.",
    ""
))
git add README.md
git commit -q -m "Add README"
git log --oneline

# ---------------------------------------------------------------
# 3단계 · feature/readme branch에서 2번째 줄 수정
# ---------------------------------------------------------------
Write-Step "3단계 · feature/readme 에서 2번째 줄 수정 (Describe repository purpose)"
git switch -q -c feature/readme
[System.IO.File]::WriteAllLines($readmePath, @(
    "# conflict-demo",
    "This repository is the starting point of the local AI helper project.",
    ""
))
git add README.md
git commit -q -m "Describe repository purpose"
git log --oneline

# ---------------------------------------------------------------
# 4단계 · main으로 돌아가 같은 줄을 다르게 수정
# ---------------------------------------------------------------
Write-Step "4단계 · main 에서 같은 줄을 다르게 수정 (State repository scope)"
git switch -q main
[System.IO.File]::WriteAllLines($readmePath, @(
    "# conflict-demo",
    "This repository is the lab record of the open source AI course.",
    ""
))
git add README.md
git commit -q -m "State repository scope"
git log --graph --oneline --all

# ---------------------------------------------------------------
# 5단계 · merge → 같은 줄이므로 충돌
# ---------------------------------------------------------------
Write-Step "5단계 · git merge feature/readme (충돌 예상)"
git merge feature/readme
Write-Host ""
Write-Host "--- git status --short ---"
git status --short
Write-Host ""
Write-Host "--- README.md (충돌 마커 포함) ---"
Get-Content -Path $readmePath -Encoding utf8

# ---------------------------------------------------------------
# 6단계 · 해결: 마커를 지우고 두 의도를 합친 한 문장을 쓴다
# ---------------------------------------------------------------
if ($AutoResolve) {
    Write-Step "6단계 · 자동 해결: 마커 제거, 두 의도를 합친 문장, merge commit"
    [System.IO.File]::WriteAllLines($readmePath, @(
        "# conflict-demo",
        "This repository is the lab record of the open source AI course and the starting point of the local AI helper project.",
        ""
    ))
    git add README.md
    git commit -q -m "Merge branch 'feature/readme' (combine purpose and scope)"
    Write-Host ""
    git log --graph --oneline --all
    Write-Host ""
    Write-Host "완료: $repo"
} else {
    Write-Step "다음 할 일 (손으로 해결)"
    Write-Host "1. VS Code로 README.md 를 연다:  code `"$readmePath`""
    Write-Host "2. <<<<<<< HEAD, =======, >>>>>>> feature/readme 세 줄을 지우고"
    Write-Host "   2번째 줄을 두 의도를 합친 한 문장으로 쓴다."
    Write-Host "3. git add README.md"
    Write-Host "4. git commit          (또는 git commit -m `"Merge branch 'feature/readme'`")"
    Write-Host "5. git log --graph --oneline --all"
    Write-Host "되돌리려면: git merge --abort"
    Write-Host ""
    Write-Host "저장소 위치: $repo"
}

Pop-Location
