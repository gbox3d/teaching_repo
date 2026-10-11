[CmdletBinding(SupportsShouldProcess = $true, ConfirmImpact = 'High')]
param(
    [switch]$Execute,
    [switch]$RemoveSshKeys,
    [switch]$RemoveVSCodeAuth,
    [switch]$Force
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Continue'

$script:Changed = 0
$script:Warnings = 0
$script:CleanupCmdlet = $PSCmdlet

function Write-Step {
    param([string]$Message)
    Write-Host "`n== $Message ==" -ForegroundColor Cyan
}

function Write-Result {
    param(
        [ValidateSet('OK', 'SKIP', 'WARN', 'INFO')]
        [string]$Status,
        [string]$Message
    )

    $color = switch ($Status) {
        'OK'   { 'Green' }
        'SKIP' { 'DarkGray' }
        'WARN' { 'Yellow' }
        default { 'Gray' }
    }

    Write-Host ("[{0}] {1}" -f $Status, $Message) -ForegroundColor $color
}

function Invoke-CleanupAction {
    param(
        [string]$Target,
        [string]$Action,
        [scriptblock]$Operation
    )

    if (-not $Execute) {
        Write-Result INFO "Would ${Action}: $Target"
        return
    }

    if ($WhatIfPreference) {
        Write-Result INFO "Would ${Action}: $Target"
        return
    }

    if ($Force -or $script:CleanupCmdlet.ShouldProcess($Target, $Action)) {
        try {
            & $Operation
            $script:Changed++
            Write-Result OK "${Action}: $Target"
        }
        catch {
            $script:Warnings++
            Write-Result WARN "$Action failed for '$Target': $($_.Exception.Message)"
        }
    }
}

function Remove-GitConfigValue {
    param([string]$Key)

    if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
        Write-Result SKIP "Git is not installed."
        return
    }

    $values = @(git config --global --get-all $Key 2>$null)
    if ($LASTEXITCODE -ne 0 -or $values.Count -eq 0) {
        Write-Result SKIP "Global Git setting '$Key' is not set."
        return
    }

    Invoke-CleanupAction "global Git setting '$Key'" 'remove' {
        git config --global --unset-all $Key 2>$null
        if ($LASTEXITCODE -notin @(0, 5)) {
            throw "git config returned exit code $LASTEXITCODE"
        }
    }
}

function Remove-PathIfPresent {
    param(
        [string]$LiteralPath,
        [switch]$Recurse
    )

    if (-not (Test-Path -LiteralPath $LiteralPath)) {
        Write-Result SKIP "Not found: $LiteralPath"
        return
    }

    Invoke-CleanupAction $LiteralPath 'delete' {
        if ($Recurse) {
            Remove-Item -LiteralPath $LiteralPath -Recurse -Force -ErrorAction Stop
        }
        else {
            Remove-Item -LiteralPath $LiteralPath -Force -ErrorAction Stop
        }
    }
}

function Get-WindowsCredentialTargets {
    if (-not (Get-Command cmdkey.exe -ErrorAction SilentlyContinue)) {
        return @()
    }

    $output = @(cmdkey.exe /list 2>$null)
    $targets = foreach ($line in $output) {
        # Handles English and Korean Windows output by taking the value after ':'.
        if ($line -match '^\s*[^:]+:\s*(.+)$') {
            $candidate = $Matches[1].Trim()
            if ($candidate -match '(?i)(github|git:https://github\.com|vscode.*github)') {
                $candidate
            }
        }
    }

    @($targets | Sort-Object -Unique)
}

function Remove-GitHubKnownHostLines {
    param([string]$KnownHostsPath)

    if (-not (Test-Path -LiteralPath $KnownHostsPath)) {
        Write-Result SKIP "Not found: $KnownHostsPath"
        return
    }

    $lines = @(Get-Content -LiteralPath $KnownHostsPath -ErrorAction SilentlyContinue)
    $remaining = @($lines | Where-Object { $_ -notmatch '(^|,)github\.com([ ,]|$)' })

    if ($remaining.Count -eq $lines.Count) {
        Write-Result SKIP "No GitHub host entry in $KnownHostsPath"
        return
    }

    Invoke-CleanupAction $KnownHostsPath 'remove GitHub host entries from' {
        if ($remaining.Count -eq 0) {
            Remove-Item -LiteralPath $KnownHostsPath -Force -ErrorAction Stop
        }
        else {
            Set-Content -LiteralPath $KnownHostsPath -Value $remaining -Encoding utf8 -ErrorAction Stop
        }
    }
}

Write-Host 'GitHub Classroom Shared-PC Reset' -ForegroundColor White -BackgroundColor DarkBlue
if (-not $Execute) {
    Write-Host 'PREVIEW MODE: nothing will be changed. Add -Execute to clean.' -ForegroundColor Yellow
}
elseif (-not $Force) {
    Write-Host 'EXECUTE MODE: PowerShell will ask before each cleanup action.' -ForegroundColor Yellow
}
else {
    Write-Host 'EXECUTE + FORCE MODE: matching data will be removed without individual prompts.' -ForegroundColor Red
}

Write-Step 'Git global identity and authentication settings'
@(
    'user.name',
    'user.email',
    'user.signingkey',
    'credential.username',
    'github.user'
) | ForEach-Object { Remove-GitConfigValue $_ }

if (Get-Command git -ErrorAction SilentlyContinue) {
    $githubSpecificKeys = @(
        git config --global --name-only --get-regexp '^(credential\..*github\.com|http\.https://github\.com/\.extraheader)$' 2>$null
    )
    $githubSpecificKeys |
        Where-Object { -not [string]::IsNullOrWhiteSpace($_) } |
        Sort-Object -Unique |
        ForEach-Object { Remove-GitConfigValue $_ }
}

Write-Step 'Git HTTPS credential files'
@(
    (Join-Path $env:USERPROFILE '.git-credentials'),
    (Join-Path $env:USERPROFILE '.config\git\credentials')
) | ForEach-Object { Remove-PathIfPresent $_ }

Write-Step 'Windows Credential Manager'
$credentialTargets = @(Get-WindowsCredentialTargets)
if ($credentialTargets.Count -eq 0) {
    Write-Result SKIP 'No GitHub-related Windows credentials were found.'
}
else {
    foreach ($target in $credentialTargets) {
        Invoke-CleanupAction $target 'delete Windows credential' {
            $result = cmdkey.exe "/delete:$target" 2>&1
            if ($LASTEXITCODE -ne 0) {
                throw ($result -join ' ')
            }
        }
    }
}

Write-Step 'GitHub CLI'
@(
    (Join-Path $env:APPDATA 'GitHub CLI'),
    (Join-Path $env:USERPROFILE '.config\gh')
) | ForEach-Object { Remove-PathIfPresent $_ -Recurse }

Write-Step 'SSH agent and GitHub known_hosts entry'
if (Get-Command ssh-add -ErrorAction SilentlyContinue) {
    Invoke-CleanupAction 'current user SSH agent' 'remove all loaded keys from' {
        $result = ssh-add -D 2>&1
        if ($LASTEXITCODE -notin @(0, 1)) {
            throw ($result -join ' ')
        }
    }
}
else {
    Write-Result SKIP 'OpenSSH ssh-add is not installed.'
}

$sshDirectory = Join-Path $env:USERPROFILE '.ssh'
Remove-GitHubKnownHostLines (Join-Path $sshDirectory 'known_hosts')
Remove-GitHubKnownHostLines (Join-Path $sshDirectory 'known_hosts.old')

if ($RemoveSshKeys) {
    Write-Step 'Standard user SSH keys'
    @(
        'id_rsa', 'id_rsa.pub',
        'id_ed25519', 'id_ed25519.pub',
        'id_ecdsa', 'id_ecdsa.pub',
        'id_dsa', 'id_dsa.pub'
    ) | ForEach-Object {
        Remove-PathIfPresent (Join-Path $sshDirectory $_)
    }
}
else {
    Write-Result INFO 'SSH key files were preserved. Use -RemoveSshKeys to include standard id_* key files.'
}

Write-Step 'VS Code GitHub authentication'
if ($RemoveVSCodeAuth) {
    $vscodeAuthPaths = @(
        (Join-Path $env:APPDATA 'Code\User\globalStorage\github.vscode-auth'),
        (Join-Path $env:APPDATA 'Code - Insiders\User\globalStorage\github.vscode-auth')
    )
    $vscodeAuthPaths | ForEach-Object { Remove-PathIfPresent $_ -Recurse }
    Write-Result INFO 'Close all VS Code windows before cleaning; active processes may retain a session.'
}
else {
    Write-Result INFO 'VS Code auth storage was preserved. Use -RemoveVSCodeAuth to include it.'
}

Write-Step 'Summary'
if (-not $Execute) {
    Write-Host 'Preview complete. Re-run with -Execute, or use the included BAT launcher.' -ForegroundColor Yellow
}
else {
    Write-Host ("Cleanup complete. Successful actions: {0}, warnings: {1}" -f $script:Changed, $script:Warnings) -ForegroundColor Green
    Write-Host 'Also sign out of github.com in the browser, or use a Guest/InPrivate browser window for class.' -ForegroundColor Yellow
}

if ($script:Warnings -gt 0) {
    exit 1
}
