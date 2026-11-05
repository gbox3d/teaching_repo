[CmdletBinding(SupportsShouldProcess = $true, ConfirmImpact = 'High')]
param(
    [switch]$Execute,
    [switch]$RemoveSshKeys,
    [switch]$RemoveVSCodeAuth,
    [switch]$OpenGitHubLogout,
    [switch]$Force
)

# GitHub Classroom Shared-PC Reset (Windows). ASCII only: Windows PowerShell 5.1 reads a BOM-less
# script as ANSI. Companion for macOS/Linux: github-classroom-reset.sh. Details: README.md.

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Continue'

$script:Changed = 0
$script:Warnings = 0
$script:CleanupCmdlet = $PSCmdlet
$script:GitHubHosts = @('github.com', 'gist.github.com')
$script:HaveGit = $false

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

    if ($Status -eq 'WARN') { $script:Warnings++ }
    Write-Host ("[{0}] {1}" -f $Status, $Message) -ForegroundColor $color
}

function Test-Command {
    param([string]$Name)
    return [bool](Get-Command $Name -ErrorAction SilentlyContinue)
}

# Runs $Operation in execute mode (after ShouldProcess unless -Force); only reports in preview mode.
# Returns $true when the operation ran and succeeded.
function Invoke-CleanupAction {
    param(
        [string]$Target,
        [string]$Action,
        [scriptblock]$Operation
    )

    if (-not $Execute -or $WhatIfPreference) {
        Write-Result INFO "Would ${Action}: $Target"
        return $false
    }

    if (-not ($Force -or $script:CleanupCmdlet.ShouldProcess($Target, $Action))) {
        Write-Result SKIP "Skipped by user: $Target"
        return $false
    }

    try {
        & $Operation
        $script:Changed++
        Write-Result OK "${Action}: $Target"
        return $true
    }
    catch {
        Write-Result WARN "$Action failed for '$Target': $($_.Exception.Message)"
        return $false
    }
}

function Remove-GitConfigValue {
    param([string]$Key)

    $values = @(git config --global --get-all $Key 2>$null)
    if ($LASTEXITCODE -ne 0 -or $values.Count -eq 0) {
        Write-Result SKIP "Global Git setting '$Key' is not set."
        return
    }

    [void](Invoke-CleanupAction "global Git setting '$Key'" 'remove' {
        git config --global --unset-all $Key 2>$null
        if ($LASTEXITCODE -notin @(0, 5)) {
            throw "git config returned exit code $LASTEXITCODE"
        }
    })
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

    [void](Invoke-CleanupAction $LiteralPath 'delete' {
        if ($Recurse) {
            Remove-Item -LiteralPath $LiteralPath -Recurse -Force -ErrorAction Stop
        }
        else {
            Remove-Item -LiteralPath $LiteralPath -Force -ErrorAction Stop
        }
    })
}

# Talks to the configured Git credential helpers (GCM, wincred, store, cache, gh ...) without ever
# prompting: no terminal prompt, no askpass program, GCM interaction disabled, no repository config.
function Invoke-GitCredential {
    param(
        [string]$Operation,
        [string]$CredentialHost,
        [string]$UserName
    )

    $lines = @('protocol=https', "host=$CredentialHost")
    if ($UserName) { $lines += "username=$UserName" }
    $lines += ''

    $saved = @{}
    foreach ($name in @('GIT_ASKPASS', 'SSH_ASKPASS', 'GIT_TERMINAL_PROMPT', 'GCM_INTERACTIVE')) {
        $saved[$name] = [Environment]::GetEnvironmentVariable($name)
    }
    [Environment]::SetEnvironmentVariable('GIT_ASKPASS', $null)
    [Environment]::SetEnvironmentVariable('SSH_ASKPASS', $null)
    [Environment]::SetEnvironmentVariable('GIT_TERMINAL_PROMPT', '0')
    [Environment]::SetEnvironmentVariable('GCM_INTERACTIVE', 'never')

    Push-Location $env:USERPROFILE
    try {
        $output = @($lines | git -c core.askPass= credential $Operation 2>&1 | ForEach-Object { "$_" })
        $exitCode = $LASTEXITCODE
    }
    finally {
        Pop-Location
        foreach ($name in $saved.Keys) {
            [Environment]::SetEnvironmentVariable($name, $saved[$name])
        }
    }

    $user = $null
    $hasPassword = $false
    foreach ($line in $output) {
        if ($line -match '^username=(.*)$') { $user = $Matches[1] }
        elseif ($line -match '^password=') { $hasPassword = $true }
    }

    # Never carry the raw output around: in a fill it contains the secret.
    $messages = @($output | Where-Object { $_ -notmatch '^(username|password|password_expiry_utc|oauth_refresh_token)=' })
    return @{
        UserName      = $user
        HasPassword   = $hasPassword
        ExitCode      = $exitCode
        Messages      = $messages
        HelperMissing = [bool](@($messages | Where-Object { $_ -match 'is not a git command|not recognized as|cannot find the path|No such file' }).Count)
    }
}

# Asks the helpers for a stored github.com credential and, in execute mode, tells them to erase it,
# repeating until nothing comes back (several accounts can be stored side by side).
function Clear-GitHelperCredentials {
    param([string]$CredentialHost)

    for ($round = 0; $round -lt 10; $round++) {
        $probe = Invoke-GitCredential 'fill' $CredentialHost
        if (-not $probe.HasPassword) {
            if ($round -eq 0) {
                if ($probe.HelperMissing) {
                    Write-Result WARN "A Git credential helper for $CredentialHost is configured but not installed: $($probe.Messages[0])"
                }
                else {
                    Write-Result SKIP "No stored credential for $CredentialHost in the Git credential helpers."
                }
            }
            return
        }

        $label = if ($probe.UserName) { "'$($probe.UserName)'" } else { 'an unknown user' }
        $done = Invoke-CleanupAction "$CredentialHost credential for $label held by the Git credential helper" 'erase' {
            $result = Invoke-GitCredential 'reject' $CredentialHost $probe.UserName
            if ($result.ExitCode -ne 0) {
                throw ($result.Messages -join ' ')
            }
        }
        if (-not $done) { return }
    }

    Write-Result WARN "Gave up after 10 rounds; the helper still returns a credential for $CredentialHost."
}

function Get-WindowsCredentialTargets {
    param([switch]$All)

    if (-not (Test-Command cmdkey.exe)) { return @() }

    $output = @(cmdkey.exe /list 2>&1 | ForEach-Object { "$_" })
    $targets = foreach ($line in $output) {
        # Only the Target line carries ':target=' (LegacyGeneric:target=..., Domain:target=...), whatever
        # language the label before it is in. User: and Type: lines are ignored on purpose.
        if ($line -match '([A-Za-z]+:target=.*)$') {
            $candidate = $Matches[1].Trim()
            if ($All -or $candidate -match '(?i)github') { $candidate }
        }
    }

    return @($targets | Sort-Object -Unique)
}

function Remove-GitHubKnownHostLines {
    param([string]$KnownHostsPath)

    if (-not (Test-Path -LiteralPath $KnownHostsPath)) {
        Write-Result SKIP "Not found: $KnownHostsPath"
        return
    }

    $raw = [System.IO.File]::ReadAllText($KnownHostsPath)
    $newline = if ($raw -match "`r`n") { "`r`n" } else { "`n" }
    $lines = @($raw -split "`r?`n")
    if ($lines.Count -gt 1 -and $lines[-1] -eq '') { $lines = @($lines[0..($lines.Count - 2)]) }
    elseif ($lines.Count -eq 1 -and $lines[0] -eq '') { $lines = @() }
    $remaining = @($lines | Where-Object { $_ -notmatch '(^|,)github\.com([ ,]|$)' })

    if ($remaining.Count -eq $lines.Count) {
        Write-Result SKIP "No GitHub host entry in $KnownHostsPath"
        return
    }

    [void](Invoke-CleanupAction $KnownHostsPath 'remove GitHub host entries from' {
        if ($remaining.Count -eq 0) {
            Remove-Item -LiteralPath $KnownHostsPath -Force -ErrorAction Stop
        }
        else {
            # No BOM (Set-Content -Encoding utf8 writes one on PowerShell 5.1, which breaks the first line).
            $text = ($remaining -join $newline) + $newline
            [System.IO.File]::WriteAllText($KnownHostsPath, $text, (New-Object System.Text.UTF8Encoding $false))
        }
    })
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

Write-Step 'Environment'
Write-Result INFO ("PowerShell {0}, user {1}" -f $PSVersionTable.PSVersion, $env:USERNAME)
if (-not $env:SESSIONNAME) {
    Write-Result WARN 'Not a desktop or Remote Desktop session (SESSIONNAME is empty). Windows Credential Manager is normally unreachable from SSH or scheduled tasks; run this on the PC itself.'
}
$script:HaveGit = Test-Command git
if (-not $script:HaveGit) {
    Write-Result SKIP 'Git is not on PATH; Git settings and credential helpers are skipped.'
}
$editorProcesses = @(Get-Process -Name 'Code', 'Code - Insiders' -ErrorAction SilentlyContinue)
if ($editorProcesses.Count -gt 0) {
    Write-Result INFO 'VS Code is running (close every window before resetting its sign-in storage).'
}

Write-Step 'Git global identity and GitHub-specific settings'
if ($script:HaveGit) {
    $keys = @('user.name', 'user.email', 'user.signingkey', 'credential.username', 'github.user')
    $keys += @(git config --global --name-only --get-regexp '^(credential\..*github\.com.*|http\.https://github\.com/\.extraheader)$' 2>$null)
    $keys |
        Where-Object { -not [string]::IsNullOrWhiteSpace($_) } |
        Sort-Object -Unique |
        ForEach-Object { Remove-GitConfigValue $_ }
    Write-Result INFO 'credential.helper is kept so the next student can sign in.'
}
else {
    Write-Result SKIP 'Git is not installed.'
}

Write-Step 'GitHub CLI'
if (Test-Command gh) {
    $savedPrompt = $env:GH_PROMPT_DISABLED
    $env:GH_PROMPT_DISABLED = '1'
    try {
        $statusLines = @(gh auth status 2>&1 | ForEach-Object { "$_" })
        $accounts = foreach ($line in $statusLines) {
            if ($line -match 'github\.com (?:account|as) (\S+)') { $Matches[1] }
        }
        $accounts = @($accounts | Sort-Object -Unique)
        if ($accounts.Count -eq 0) {
            Write-Result SKIP 'GitHub CLI is not logged in to github.com.'
        }
        foreach ($account in $accounts) {
            [void](Invoke-CleanupAction "GitHub CLI login '$account'" 'log out' {
                $result = @(gh auth logout --hostname github.com --user $account 2>&1 | ForEach-Object { "$_" })
                if ($LASTEXITCODE -ne 0) {
                    # gh before 2.40 has no --user; a single account logs out without it.
                    $result = @(gh auth logout --hostname github.com 2>&1 | ForEach-Object { "$_" })
                    if ($LASTEXITCODE -ne 0) { throw ($result -join ' ') }
                }
            })
        }
    }
    finally {
        [Environment]::SetEnvironmentVariable('GH_PROMPT_DISABLED', $savedPrompt)
    }
}
else {
    Write-Result SKIP 'GitHub CLI is not installed.'
}
@(
    (Join-Path $env:APPDATA 'GitHub CLI'),
    (Join-Path $env:USERPROFILE '.config\gh')
) | ForEach-Object { Remove-PathIfPresent $_ -Recurse }

Write-Step 'Git credential helpers (Git Credential Manager, wincred, store ...)'
if ($script:HaveGit) {
    $helpers = @(git config --get-all credential.helper 2>$null)
    if ($helpers.Count -gt 0) { Write-Result INFO "Configured helpers: $($helpers -join ', ')" }
    foreach ($credentialHost in $script:GitHubHosts) {
        Clear-GitHelperCredentials $credentialHost
    }
}
else {
    Write-Result SKIP 'Git is not installed.'
}

Write-Step 'Credential files'
@(
    (Join-Path $env:USERPROFILE '.git-credentials'),
    (Join-Path $env:USERPROFILE '.config\git\credentials')
) | ForEach-Object { Remove-PathIfPresent $_ }
foreach ($storeRoot in @((Join-Path $env:USERPROFILE '.gcm\store'), (Join-Path $env:USERPROFILE '.gcm\dpapi_store'))) {
    if (-not (Test-Path -LiteralPath $storeRoot)) {
        Write-Result SKIP "Not found: $storeRoot"
        continue
    }
    $entries = @(Get-ChildItem -LiteralPath $storeRoot -Recurse -Directory -ErrorAction SilentlyContinue |
        Where-Object { $_.Name -match '(?i)github\.com' })
    if ($entries.Count -eq 0) {
        Write-Result SKIP "No github.com entry in $storeRoot"
    }
    foreach ($entry in $entries) { Remove-PathIfPresent $entry.FullName -Recurse }
}

Write-Step 'Windows Credential Manager'
if (-not (Test-Command cmdkey.exe)) {
    Write-Result SKIP 'cmdkey.exe is not available.'
}
else {
    $allTargets = @(Get-WindowsCredentialTargets -All)
    $credentialTargets = @(Get-WindowsCredentialTargets)
    if ($allTargets.Count -eq 0 -and -not $env:SESSIONNAME) {
        Write-Result WARN 'Credential Manager lists nothing at all from this session; the stored GitHub logins are probably just invisible from here.'
    }
    elseif ($credentialTargets.Count -eq 0) {
        Write-Result SKIP "No GitHub-related Windows credential among $($allTargets.Count) stored entries."
    }
    foreach ($target in $credentialTargets) {
        [void](Invoke-CleanupAction $target 'delete Windows credential' {
            $result = @(cmdkey.exe "/delete:$target" 2>&1 | ForEach-Object { "$_" })
            if ($LASTEXITCODE -ne 0) {
                throw ($result -join ' ')
            }
        })
    }
}

Write-Step 'SSH agent and GitHub known_hosts entry'
if (Test-Command ssh-add) {
    [void](ssh-add -l 2>&1)
    switch ($LASTEXITCODE) {
        0 {
            [void](Invoke-CleanupAction 'current user SSH agent' 'remove all loaded keys from' {
                $result = @(ssh-add -D 2>&1 | ForEach-Object { "$_" })
                if ($LASTEXITCODE -ne 0) { throw ($result -join ' ') }
            })
        }
        1 { Write-Result SKIP 'No keys are loaded in the SSH agent.' }
        default { Write-Result SKIP 'The SSH agent is not running.' }
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

Write-Step 'VS Code sign-in storage and Copilot tokens'
$vscodeStateFiles = @(
    (Join-Path $env:APPDATA 'Code\User\globalStorage\state.vscdb'),
    (Join-Path $env:APPDATA 'Code\User\globalStorage\state.vscdb.backup'),
    (Join-Path $env:USERPROFILE '.vscode-shared\sharedStorage\state.vscdb'),
    (Join-Path $env:USERPROFILE '.vscode-shared\sharedStorage\state.vscdb.backup'),
    (Join-Path $env:APPDATA 'Code - Insiders\User\globalStorage\state.vscdb'),
    (Join-Path $env:APPDATA 'Code - Insiders\User\globalStorage\state.vscdb.backup'),
    (Join-Path $env:USERPROFILE '.vscode-insiders-shared\sharedStorage\state.vscdb'),
    (Join-Path $env:USERPROFILE '.vscode-insiders-shared\sharedStorage\state.vscdb.backup')
)
if ($RemoveVSCodeAuth) {
    if ($editorProcesses.Count -gt 0 -and $Execute) {
        Write-Result SKIP 'VS Code is running; its state databases are locked and were left alone.'
    }
    else {
        # The GitHub (and Microsoft) sign-ins live encrypted inside these SQLite files; there is no
        # dependency-free way to delete single rows, so the whole global state is reset. Settings,
        # keybindings, snippets and extensions are separate files and stay.
        $vscodeStateFiles | ForEach-Object { Remove-PathIfPresent $_ }
    }
    Remove-PathIfPresent (Join-Path $env:LOCALAPPDATA 'github-copilot') -Recurse
}
else {
    Write-Result INFO 'VS Code sign-in storage was preserved. Use -RemoveVSCodeAuth to reset it (also clears the recently-opened list and extension state).'
}

Write-Step 'Browser session on github.com'
Write-Result INFO 'A browser still signed in to github.com re-authorizes Git Credential Manager silently: the next git push would store the previous student again.'
if ($OpenGitHubLogout) {
    [void](Invoke-CleanupAction 'https://github.com/logout in the default browser' 'open' {
        Start-Process 'https://github.com/logout' -ErrorAction Stop
    })
    if ($Execute) { Write-Result INFO 'Click "Sign out" in the browser window that opened.' }
}
else {
    Write-Result INFO 'Use -OpenGitHubLogout to open the GitHub sign-out page, or sign out manually.'
}

if ($Execute) {
    Write-Step 'Verification'
    if ($script:HaveGit) {
        foreach ($credentialHost in $script:GitHubHosts) {
            $probe = Invoke-GitCredential 'fill' $credentialHost
            if ($probe.HasPassword) {
                $who = if ($probe.UserName) { $probe.UserName } else { 'an unknown user' }
                Write-Result WARN "Git still obtains a $credentialHost credential for '$who' without asking."
            }
            elseif ($probe.HelperMissing) {
                Write-Result INFO "Not verifiable for ${credentialHost}: the configured credential helper is not installed."
            }
            else {
                Write-Result OK "Git credential helpers return nothing for $credentialHost."
            }
        }
    }
    if (Test-Command cmdkey.exe) {
        $left = @(Get-WindowsCredentialTargets)
        if ($left.Count -gt 0) {
            Write-Result WARN "Credential Manager still has: $($left -join '; ')"
        }
        elseif (@(Get-WindowsCredentialTargets -All).Count -eq 0 -and -not $env:SESSIONNAME) {
            Write-Result INFO 'Credential Manager could not be inspected from this session.'
        }
        else {
            Write-Result OK 'No GitHub-related entry left in Credential Manager.'
        }
    }
    if ($RemoveVSCodeAuth) {
        $leftFiles = @($vscodeStateFiles | Where-Object { Test-Path -LiteralPath $_ })
        if ($leftFiles.Count -gt 0) {
            Write-Result WARN "VS Code sign-in storage still present (close VS Code and run again): $($leftFiles -join '; ')"
        }
        else {
            Write-Result OK 'VS Code state databases are gone.'
        }
    }
}

Write-Step 'Summary'
if (-not $Execute) {
    Write-Host 'Preview complete. Re-run with -Execute, or use GitHub-Classroom-Reset.bat.' -ForegroundColor Yellow
}
else {
    Write-Host ("Cleanup complete. Successful actions: {0}, warnings: {1}" -f $script:Changed, $script:Warnings) -ForegroundColor Green
    Write-Host 'Sign out of github.com in every browser, or use a Guest/InPrivate window in class.' -ForegroundColor Yellow
}

if ($script:Warnings -gt 0) {
    exit 1
}
