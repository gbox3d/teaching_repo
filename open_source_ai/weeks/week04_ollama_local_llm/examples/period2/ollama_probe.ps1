# 1교시 기록 도우미 — ollama list / show / ps 출력을 outputs/ 에 텍스트로 저장한다.
#
# 사용:  .\ollama_probe.ps1                       (OLLAMA_MODEL 또는 qwen3:8b)
#        .\ollama_probe.ps1 -Model qwen3:0.6b
#        powershell -ExecutionPolicy Bypass -File .\ollama_probe.ps1 -Model qwen3:8b   (실행 정책이 막을 때)
#
# ollama ps 는 "지금 메모리에 올라간 모델"만 보여 준다.
# ollama run 을 끝낸 직후(기본 5분 안)에 실행해야 SIZE 와 PROCESSOR 가 보인다.

param(
    [string]$Model = "",
    [string]$OutDir = "outputs"
)

if ($Model -eq "") {
    if ($env:OLLAMA_MODEL) { $Model = $env:OLLAMA_MODEL } else { $Model = "qwen3:8b" }
}

New-Item -ItemType Directory -Force -Path $OutDir | Out-Null

$safeName = $Model -replace "[:/\\]", "-"
$stamp = Get-Date -Format "yyyyMMdd-HHmmss"
$file = Join-Path $OutDir "probe-$safeName-$stamp.txt"

$lines = @()
$lines += "# ollama probe — model: $Model — $stamp"
$lines += ""
$lines += "## ollama list"
$lines += (ollama list 2>&1)
$lines += ""
$lines += "## ollama show $Model"
$lines += (ollama show $Model 2>&1)
$lines += ""
$lines += "## ollama ps"
$lines += (ollama ps 2>&1)

$lines | Set-Content -Path $file -Encoding utf8

Write-Host "saved: $file"
Write-Host "ps 결과가 비어 있으면 모델이 이미 내려간 것이다. ollama run 으로 다시 올린 뒤 5분 안에 실행한다."
