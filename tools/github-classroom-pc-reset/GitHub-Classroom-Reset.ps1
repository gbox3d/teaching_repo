[CmdletBinding(SupportsShouldProcess = $true, ConfirmImpact = 'High')]
param(
    [switch]$Execute,
    [switch]$RemoveSshKeys,
    [switch]$RemoveVSCodeAuth,
    [switch]$Force,
    [string[]]$VSCodeUserDataPath = @(),
    [string[]]$VSCodeSharedDataPath = @()
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Continue'

$script:Changed = 0
$script:Warnings = 0
$script:Planned = 0
$script:CleanupCmdlet = $PSCmdlet

foreach ($helper in @('WindowsCredentialStore.ps1', 'Windows-VSCodeAuth.ps1')) {
    $helperPath = Join-Path $PSScriptRoot $helper
    if (-not (Test-Path -LiteralPath $helperPath -PathType Leaf)) {
        Write-Host "Missing required helper: $helper. Copy the entire reset tool folder and retry." -ForegroundColor Red
        exit 1
    }
    . $helperPath
}

$script:GitHome = $env:USERPROFILE
if (-not [string]::IsNullOrWhiteSpace($env:HOME)) {
    $script:GitHome = $env:HOME
}

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

    if (-not $Execute -or $WhatIfPreference) {
        $script:Planned++
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
    else {
        Write-Result SKIP "Declined ${Action}: $Target"
    }
}

function Remove-GitIdentitySettings {
    # Normal Git loads both HOME and XDG global files, while --global may select
    # just one. Inspect both explicitly, including active include files, unless
    # GIT_CONFIG_GLOBAL overrides them. Remove values from their actual origins.
    # NUL delimiters preserve spaces and non-ASCII characters in file paths.
    $pattern = '^(user\.(name|email|signingkey)|credential\.username|github\.user|credential\.(https?://)?([^/@]*@)?([a-zA-Z0-9-]+\.)*github\.com([/:].*)?\.[^.]+|http\.https?://([^/@]*@)?([a-zA-Z0-9-]+\.)*github\.com(:[0-9]+)?(/.*)?\.extraheader)$'
    $configFiles = @(
        if (-not [string]::IsNullOrWhiteSpace($env:GIT_CONFIG_GLOBAL)) {
            $env:GIT_CONFIG_GLOBAL
        }
        else {
            Join-Path $script:GitHome '.gitconfig'
            if (-not [string]::IsNullOrWhiteSpace($env:XDG_CONFIG_HOME)) {
                Join-Path $env:XDG_CONFIG_HOME 'git\config'
            }
            else {
                Join-Path $script:GitHome '.config\git\config'
            }
        }
    )
    $raw = ''
    foreach ($configFile in $configFiles) {
        if (-not (Test-Path -LiteralPath $configFile -PathType Leaf)) { continue }
        $part = @(git -C $script:GitHome config --file $configFile --includes --null --show-origin --name-only --get-regexp $pattern 2>$null) -join "`n"
        if ($LASTEXITCODE -eq 1) { continue }
        if ($LASTEXITCODE -ne 0) {
            $script:Warnings++
            Write-Result WARN "Unable to read Git settings from '$configFile'. Check configuration syntax and permissions."
            continue
        }
        $raw += $part
    }
    if ($raw.Length -eq 0) {
        Write-Result SKIP 'No matching global Git identity or GitHub authentication settings.'
        return
    }

    $fields = $raw.Split([char]0)
    $seen = @{}
    for ($index = 0; $index + 1 -lt $fields.Length; $index += 2) {
        $origin = $fields[$index]
        $key = $fields[$index + 1]
        if (-not $origin.StartsWith('file:')) {
            $script:Warnings++
            Write-Result WARN "Cannot remove Git setting '$key' from non-file configuration."
            continue
        }
        $configPath = $origin.Substring(5)
        $identity = "$configPath`0$key"
        if ($seen.ContainsKey($identity)) { continue }
        $seen[$identity] = $true
        Invoke-CleanupAction "$key ($configPath)" 'remove Git setting' {
            git -C $script:GitHome config --file $configPath --unset-all $key 2>$null
            if ($LASTEXITCODE -ne 0) {
                throw "git config --unset-all returned exit code $LASTEXITCODE"
            }
            $null = git -C $script:GitHome config --file $configPath --get-all $key 2>$null
            if ($LASTEXITCODE -ne 1) {
                throw 'Git setting removal could not be verified.'
            }
        }
    }
}

function Remove-PathIfPresent {
    param([string]$LiteralPath)

    if (-not (Test-Path -LiteralPath $LiteralPath)) {
        Write-Result SKIP "Not found: $LiteralPath"
        return
    }

    $resolvedPath = [IO.Path]::GetFullPath($LiteralPath)
    # Delete exact regular files only, never a directory or a linked file.
    $item = Get-Item -LiteralPath $resolvedPath -Force -ErrorAction Stop
    if ($item.PSIsContainer -or ($item.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0) {
        $script:Warnings++
        Write-Result WARN "Expected a regular credential file; refusing to delete: $resolvedPath"
        return
    }

    Invoke-CleanupAction $LiteralPath 'delete' {
        Remove-Item -LiteralPath $resolvedPath -Force -ErrorAction Stop
    }
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

$originalConsoleEncoding = [Console]::OutputEncoding
$originalPipelineEncoding = $OutputEncoding
try {
    # Windows PowerShell 5.1 otherwise decodes Git's UTF-8 origin paths using
    # the console code page, making Korean Windows profile paths unusable.
    $OutputEncoding = New-Object Text.UTF8Encoding($false)
    [Console]::OutputEncoding = $OutputEncoding

Write-Host 'GitHub Classroom Shared-PC Reset' -ForegroundColor White -BackgroundColor DarkBlue
if (-not $Execute -or $WhatIfPreference) {
    Write-Host 'PREVIEW MODE: nothing will be changed. Add -Execute to clean.' -ForegroundColor Yellow
}
elseif (-not $Force) {
    Write-Host 'EXECUTE MODE: PowerShell will ask before each cleanup action.' -ForegroundColor Yellow
}
else {
    Write-Host 'EXECUTE + FORCE MODE: matching data will be removed without individual prompts.' -ForegroundColor Red
}

Write-Step 'Git credential helpers (github.com)'
if (Get-Command git -ErrorAction SilentlyContinue) {
    # Ask helpers to erase first: a GitHub-specific helper may itself be one of
    # the settings that is removed below. Do not run in the repository's scope.
    Invoke-CleanupAction 'github.com in configured Git credential helpers' 'erase credentials for' {
        $null = "protocol=https`nhost=github.com`n`n" | git -C $script:GitHome credential reject 2>&1
        if ($LASTEXITCODE -ne 0) {
            throw "git credential reject returned exit code $LASTEXITCODE"
        }
    }
    Write-Step 'Git global identity and authentication settings'
    Remove-GitIdentitySettings
}
else {
    Write-Result SKIP 'Git is not installed.'
}

Write-Step 'Git HTTPS credential files'
@(
    (Join-Path $script:GitHome '.git-credentials'),
    (Join-Path $script:GitHome '.config\git\credentials')
    if (-not [string]::IsNullOrWhiteSpace($env:XDG_CONFIG_HOME)) {
        Join-Path $env:XDG_CONFIG_HOME 'git\credentials'
    }
) | Sort-Object -Unique | ForEach-Object { Remove-PathIfPresent $_ }

Write-Step 'Windows Credential Manager'
try {
    $credentialTargets = @(Get-WindowsCredentialTargets -IncludeVSCodeAuth:$RemoveVSCodeAuth)
    if ($credentialTargets.Count -eq 0) {
        Write-Result SKIP 'No GitHub-related Windows credentials were found.'
    }
    else {
        foreach ($credential in $credentialTargets) {
            Invoke-CleanupAction $credential.Target 'delete Windows credential' {
                Remove-WindowsCredentialTarget -Target $credential.Target -Type $credential.Type
            }
        }
    }
}
catch {
    $script:Warnings++
    Write-Result WARN "Windows Credential Manager could not be inspected: $($_.Exception.Message)"
}

Write-Step 'GitHub CLI'
# Secure gh tokens were removed in the native credential sweep above. Remove
# only the account file, including invalid/multiple accounts, without online
# auth checks, token refreshes or interactive account-selection prompts.
@(
    (Join-Path $env:APPDATA 'GitHub CLI'),
    (Join-Path $script:GitHome '.config\gh')
    if (-not [string]::IsNullOrWhiteSpace($env:GH_CONFIG_DIR)) { $env:GH_CONFIG_DIR }
    if (-not [string]::IsNullOrWhiteSpace($env:XDG_CONFIG_HOME)) {
        Join-Path $env:XDG_CONFIG_HOME 'gh'
    }
) | Sort-Object -Unique | ForEach-Object { Remove-PathIfPresent (Join-Path $_ 'hosts.yml') }

Write-Step 'SSH agent and GitHub known_hosts entry'
if (Get-Command ssh-add -ErrorAction SilentlyContinue) {
    $null = ssh-add -l 2>&1
    if ($LASTEXITCODE -eq 0) {
        Invoke-CleanupAction 'current user SSH agent' 'remove all loaded keys from' {
            $null = ssh-add -D 2>&1
            if ($LASTEXITCODE -ne 0) {
                throw "ssh-add -D returned exit code $LASTEXITCODE"
            }
        }
    }
    else {
        Write-Result SKIP 'No accessible SSH agent with loaded keys.'
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
    $sessionId = (Get-Process -Id $PID).SessionId
    $runningCode = @(
        Get-Process -Name 'Code', 'Code - Insiders' -ErrorAction SilentlyContinue |
            Where-Object { $_.SessionId -eq $sessionId }
    )
    if ($runningCode.Count -gt 0 -and $Execute -and -not $WhatIfPreference) {
        $script:Warnings++
        Write-Result WARN 'VS Code is running. Close all VS Code windows and re-run to remove its saved GitHub sessions.'
    }
    else {
        try {
            $userDataRoots = @(
                (Join-Path $env:APPDATA 'Code'),
                (Join-Path $env:APPDATA 'Code - Insiders')
                if (-not [string]::IsNullOrWhiteSpace($env:VSCODE_APPDATA)) {
                    Join-Path $env:VSCODE_APPDATA 'Code'
                    Join-Path $env:VSCODE_APPDATA 'Code - Insiders'
                }
                $VSCodeUserDataPath
            )
            $sharedDataRoots = @(
                (Join-Path $env:USERPROFILE '.vscode-shared'),
                (Join-Path $env:USERPROFILE '.vscode-insiders-shared')
                $VSCodeSharedDataPath
            )
            $portableRoots = @(
                if (-not [string]::IsNullOrWhiteSpace($env:VSCODE_PORTABLE)) { $env:VSCODE_PORTABLE }
                foreach ($commandName in @('code', 'code-insiders')) {
                    $command = Get-Command $commandName -ErrorAction SilentlyContinue
                    if ($command -and $command.Source) {
                        $installRoot = Split-Path (Split-Path $command.Source -Parent) -Parent
                        if ($installRoot) { Join-Path $installRoot 'data' }
                    }
                }
            ) | Sort-Object -Unique
            foreach ($portableRoot in $portableRoots) {
                $userDataRoots += Join-Path $portableRoot 'user-data'
                $sharedDataRoots += Join-Path $portableRoot 'shared-data'
            }
            $databases = @(Get-VSCodeAuthDatabasePaths -UserDataDirectories $userDataRoots -SharedDataDirectories $sharedDataRoots)
            if ($databases.Count -eq 0) { Write-Result SKIP 'No VS Code authentication databases found.' }
            foreach ($database in $databases) {
                try {
                    $count = Get-VSCodeGitHubAuthEntryCount -LiteralPath $database
                    if ($count -eq 0) {
                        Write-Result SKIP "No saved GitHub authentication entries in $database"
                        continue
                    }
                    Invoke-CleanupAction "$database ($count GitHub entries)" 'remove saved GitHub authentication from' {
                        $null = Remove-VSCodeGitHubAuthEntries -LiteralPath $database
                    }
                }
                catch {
                    $script:Warnings++
                    Write-Result WARN "Unable to inspect VS Code authentication database '$database': $($_.Exception.Message)"
                }
            }
        }
        catch {
            $script:Warnings++
            Write-Result WARN "Unable to locate VS Code authentication storage: $($_.Exception.Message)"
        }
    }
}
else {
    Write-Result INFO 'VS Code auth storage was preserved. Use -RemoveVSCodeAuth to include it.'
}

Write-Step 'Summary'
if (-not $Execute -or $WhatIfPreference) {
    Write-Host ("Preview complete. Planned actions: {0}, warnings: {1}. Nothing was changed." -f $script:Planned, $script:Warnings) -ForegroundColor Yellow
}
else {
    $summaryColor = if ($script:Warnings -gt 0) { 'Yellow' } else { 'Green' }
    Write-Host ("Cleanup complete. Successful actions: {0}, warnings: {1}" -f $script:Changed, $script:Warnings) -ForegroundColor $summaryColor
    Write-Host 'Also sign out of github.com in the browser, or use a Guest/InPrivate browser window for class.' -ForegroundColor Yellow
}

if ($script:Warnings -gt 0) {
    exit 1
}
exit 0
}
catch {
    Write-Result WARN "Reset stopped: $($_.Exception.Message)"
    exit 1
}
finally {
    [Console]::OutputEncoding = $originalConsoleEncoding
    $OutputEncoding = $originalPipelineEncoding
}
