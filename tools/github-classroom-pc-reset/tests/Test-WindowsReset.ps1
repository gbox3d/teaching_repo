[CmdletBinding()]
param(
    [string[]]$PowerShellPath = @(
        @('powershell.exe', 'pwsh.exe') | Where-Object { Get-Command $_ -ErrorAction SilentlyContinue }
    )
)

# Run the real reset entry point against a disposable profile. Credential Manager,
# Git credential rejection, gh and ssh-add are replaced before the entry point runs.
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$toolDirectory = Split-Path -Parent $PSScriptRoot
$realGit = (Get-Command git.exe -ErrorAction Stop).Source
$testRoot = Join-Path ([IO.Path]::GetTempPath()) ('classroom-reset-test-' + [guid]::NewGuid().ToString('N'))
$assertions = 0
$lastCaseOutput = ''

function Assert-Condition {
    param([bool]$Condition, [string]$Message)
    if (-not $Condition) { throw ($Message + "`n" + $script:lastCaseOutput) }
    $script:assertions++
}

function Get-ProfileSnapshot {
    param([string]$Directory)
    $powerShellCacheDirectory = Join-Path $Directory 'AppData\Local\Microsoft\PowerShell'
    @(
        Get-ChildItem -LiteralPath $Directory -File -Recurse |
            # The PowerShell 7 host itself creates this startup timing cache.
            Where-Object { -not ($_.DirectoryName -eq $powerShellCacheDirectory -and $_.Name -like 'StartupProfileData-*') } |
            Sort-Object FullName | ForEach-Object {
            $_.FullName.Substring($Directory.Length) + ':' + (Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash
        }
    ) -join "`n"
}

$credentialMock = @'
function Initialize-WindowsCredentialStore { }
function Get-WindowsCredentialTargets {
    param([switch]$IncludeVSCodeAuth)
    [pscustomobject]@{ Target = 'git:https://github.com'; Type = 1 }
    [pscustomobject]@{ Target = 'gh:github.com:fixture-student'; Type = 1 }
    [pscustomobject]@{ Target = 'gh:github.com:another-student'; Type = 1 }
    if ($IncludeVSCodeAuth) {
        [pscustomobject]@{ Target = 'vscodevscode.github-authentication'; Type = 1 }
    }
}
function Remove-WindowsCredentialTarget {
    param([string]$Target, [int]$Type)
    Write-TestInvocation 'credential-delete' @{ target = $Target; type = $Type }
    if ($env:RESET_TEST_CREDENTIAL_FAILURE -eq '1' -and $Target -eq 'git:https://github.com') {
        throw 'Simulated credential deletion failure.'
    }
}
'@

$workerScript = @'
param([ValidateSet('Preview', 'WhatIf', 'Execute', 'CredentialFailure', 'RunningVSCode', 'XdgConfig')][string]$Mode)
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function global:Write-TestInvocation {
    param([string]$Kind, [hashtable]$Data)
    $record = @{ kind = $Kind; data = $Data } | ConvertTo-Json -Compress -Depth 5
    Add-Content -LiteralPath $env:RESET_TEST_LOG -Value $record -Encoding UTF8
}

function global:git {
    $gitArguments = @($args | ForEach-Object { [string]$_ })
    if (($gitArguments -contains 'credential') -and ($gitArguments -contains 'reject')) {
        $request = ($input | Out-String)
        $helper = & $env:RESET_TEST_GIT config --global --get credential.helper
        Write-TestInvocation 'credential-reject' @{ request = $request; helper = [string]$helper }
        $global:LASTEXITCODE = 0
        return
    }
    & $env:RESET_TEST_GIT @gitArguments
    $global:LASTEXITCODE = $LASTEXITCODE
}

function global:gh {
    Write-TestInvocation 'gh-call' @{ arguments = @($args | ForEach-Object { [string]$_ }) }
    $global:LASTEXITCODE = 0
}

function global:ssh-add {
    if ($args -contains '-D') { Write-TestInvocation 'ssh-remove' @{} }
    $global:LASTEXITCODE = 0
}

# Prevent portable VS Code discovery from following the real user's PATH. A
# function has no executable Source, so every scanned data root stays in fixture.
function global:code { }
function global:code-insiders { }

function global:Get-Process {
    param([string[]]$Name, [int[]]$Id, [switch]$IncludeUserName)
    # The test profile has no editor processes. Do not inspect the real session.
    if ($PSBoundParameters.ContainsKey('Id')) { return [pscustomobject]@{ SessionId = 0 } }
    if ($env:RESET_TEST_RUNNING_CODE -eq '1') { return [pscustomobject]@{ SessionId = 0; ProcessName = 'Code' } }
    @()
}

# A regression to cmdkey must fail without invoking the real credential store.
function global:cmdkey.exe { throw 'Tests prohibit calling the real cmdkey.exe.' }

Set-Location -LiteralPath $env:RESET_TEST_PROFILE
$entryPoint = Join-Path $env:RESET_TEST_SCRIPTS 'GitHub-Classroom-Reset.ps1'
switch ($Mode) {
    'Preview' { & $entryPoint -RemoveSshKeys -RemoveVSCodeAuth }
    'WhatIf' { & $entryPoint -Execute -Force -RemoveSshKeys -RemoveVSCodeAuth -WhatIf }
    'Execute' { & $entryPoint -Execute -Force -RemoveSshKeys -RemoveVSCodeAuth }
    'CredentialFailure' {
        $env:RESET_TEST_CREDENTIAL_FAILURE = '1'
        & $entryPoint -Execute -Force -RemoveSshKeys -RemoveVSCodeAuth
    }
    'RunningVSCode' {
        $env:RESET_TEST_RUNNING_CODE = '1'
        & $entryPoint -Execute -Force -RemoveSshKeys -RemoveVSCodeAuth
    }
    'XdgConfig' {
        Remove-Item Env:\GIT_CONFIG_GLOBAL
        & $entryPoint -Execute -Force -RemoveSshKeys -RemoveVSCodeAuth
    }
}
exit $LASTEXITCODE
'@

function New-Fixture {
    param([string]$Directory)
    $profile = Join-Path $Directory ('profile space ' + [char]0xD559 + [char]0xC0DD)
    $appData = Join-Path $profile 'AppData\Roaming'
    $xdg = Join-Path $profile 'xdg'
    $ghConfig = Join-Path $profile 'custom gh'
    $scriptDirectory = Join-Path $Directory 'scripts'
    foreach ($path in @($profile, $appData, $xdg, $ghConfig, $scriptDirectory, (Join-Path $profile '.ssh'),
        (Join-Path $profile '.config\git'), (Join-Path $profile '.config\gh'),
        (Join-Path $appData 'GitHub CLI'))) {
        New-Item -ItemType Directory -Path $path -Force | Out-Null
    }
    # Copy the executable code, then replace the native credential boundary only in
    # this sandbox. No call can enumerate or delete the actual Windows credentials.
    Get-ChildItem -LiteralPath $toolDirectory -Filter '*.ps1' -File | Copy-Item -Destination $scriptDirectory
    Set-Content -LiteralPath (Join-Path $scriptDirectory 'WindowsCredentialStore.ps1') -Value $credentialMock -Encoding UTF8
    $config = Join-Path $profile '.gitconfig'
    $settings = [ordered]@{
        'user.name' = 'Fixture Student'
        'user.email' = 'fixture@example.invalid'
        'user.signingkey' = 'fixture-signing-key'
        'credential.username' = 'fixture-student'
        'github.user' = 'fixture-student'
        'credential.helper' = 'fixture-safe-helper'
        'credential.https://github.com.username' = 'fixture-student'
        'credential.https://github.com.helper' = 'fixture-scoped-helper'
        'http.https://github.com/.extraheader' = 'fixture-header'
        'http.https://student@github.com:443/.extraheader' = 'fixture-scoped-header'
        'http.https://github.com.evil.invalid/.extraheader' = 'keep-lookalike-host-header'
        'credential.https://example.invalid.username' = 'keep-this-account'
        'core.editor' = 'fixture-editor'
    }
    foreach ($key in $settings.Keys) {
        & $realGit config --file $config $key $settings[$key]
        if ($LASTEXITCODE -ne 0) { throw "Cannot seed Git setting: $key" }
    }
    $includedConfig = Join-Path $profile '.config\git\included.cfg'
    & $realGit config --file $includedConfig user.name 'Included Fixture Student'
    & $realGit config --file $includedConfig credential.https://github.com/classroom.username 'included-student'
    & $realGit config --file $includedConfig core.autocrlf 'true'
    & $realGit config --file $config include.path $includedConfig
    $xdgConfig = Join-Path $xdg 'git\config'
    New-Item -ItemType Directory -Path (Split-Path -Parent $xdgConfig) -Force | Out-Null
    & $realGit config --file $xdgConfig user.name 'XDG Fixture Student'
    & $realGit config --file $xdgConfig credential.https://github.com.username 'xdg-student'
    & $realGit config --file $xdgConfig core.autocrlf 'input'
    $files = [ordered]@{
        '.git-credentials' = 'https://fixture:fake@github.com'
        '.config\git\credentials' = 'https://fixture:fake@github.com'
        '.config\gh\hosts.yml' = "github.com:`n  user: fixture-student"
        '.config\gh\config.yml' = 'editor: fixture-editor'
        'custom gh\hosts.yml' = "github.com:`n  user: fixture-student"
        'custom gh\config.yml' = 'editor: fixture-editor'
        'custom gh\unrelated.txt' = 'keep arbitrary user data'
        'AppData\Roaming\GitHub CLI\hosts.yml' = "github.com:`n  user: fixture-student"
        'AppData\Roaming\GitHub CLI\config.yml' = 'editor: fixture-editor'
        '.ssh\id_ed25519' = 'fake private key'
        '.ssh\id_ed25519.pub' = 'fake public key'
        '.ssh\custom_key' = 'keep custom key'
        '.ssh\known_hosts' = "github.com ssh-ed25519 fake-github-key`nexample.invalid ssh-ed25519 keep-key"
        'AppData\Roaming\Code\User\settings.json' = '{"editor.fontSize":16}'
    }
    foreach ($path in $files.Keys) {
        $absolute = Join-Path $profile $path
        New-Item -ItemType Directory -Path (Split-Path -Parent $absolute) -Force | Out-Null
        Set-Content -LiteralPath $absolute -Value $files[$path] -Encoding UTF8
    }
    $worker = Join-Path $Directory 'worker.ps1'
    Set-Content -LiteralPath $worker -Value $workerScript -Encoding UTF8
    [pscustomobject]@{
        Profile = $profile; AppData = $appData; Xdg = $xdg; GhConfig = $ghConfig
        ScriptDirectory = $scriptDirectory; Worker = $worker; Config = $config; IncludedConfig = $includedConfig; XdgConfig = $xdgConfig
        Log = (Join-Path $Directory 'calls.jsonl')
    }
}

function Invoke-Fixture {
    param([string]$HostPath, $Fixture, [string]$Mode)
    $start = New-Object Diagnostics.ProcessStartInfo
    $start.FileName = $HostPath
    $start.Arguments = '-NoLogo -NoProfile -NonInteractive -ExecutionPolicy Bypass -File "' + $Fixture.Worker + '" -Mode ' + $Mode
    $start.UseShellExecute = $false
    $start.CreateNoWindow = $true
    $start.RedirectStandardOutput = $true
    $start.RedirectStandardError = $true
    $start.WorkingDirectory = $Fixture.Profile
    foreach ($name in @('GH_TOKEN', 'GITHUB_TOKEN', 'GH_ENTERPRISE_TOKEN', 'GITHUB_ENTERPRISE_TOKEN',
        'GIT_CONFIG_COUNT', 'GIT_CONFIG_PARAMETERS', 'VSCODE_PORTABLE', 'VSCODE_APPDATA',
        'RESET_TEST_CREDENTIAL_FAILURE', 'RESET_TEST_RUNNING_CODE')) {
        $start.EnvironmentVariables.Remove($name)
    }
    $environment = @{
        USERPROFILE = $Fixture.Profile; HOME = $Fixture.Profile; APPDATA = $Fixture.AppData
        LOCALAPPDATA = (Join-Path $Fixture.Profile 'AppData\Local'); XDG_CONFIG_HOME = $Fixture.Xdg
        GH_CONFIG_DIR = $Fixture.GhConfig; GIT_CONFIG_GLOBAL = $Fixture.Config
        GIT_CONFIG_NOSYSTEM = '1'; GIT_CONFIG_SYSTEM = (Join-Path $Fixture.Profile 'no-system-config')
        GIT_TERMINAL_PROMPT = '0'; GCM_INTERACTIVE = 'never'; RESET_TEST_GIT = $realGit
        RESET_TEST_PROFILE = $Fixture.Profile; RESET_TEST_SCRIPTS = $Fixture.ScriptDirectory
        RESET_TEST_LOG = $Fixture.Log
    }
    foreach ($name in $environment.Keys) { $start.EnvironmentVariables[$name] = $environment[$name] }
    $process = New-Object Diagnostics.Process
    $process.StartInfo = $start
    try {
        [void]$process.Start()
        $stdoutTask = $process.StandardOutput.ReadToEndAsync()
        $stderrTask = $process.StandardError.ReadToEndAsync()
        if (-not $process.WaitForExit(60000)) {
            $process.Kill()
            throw 'Reset test timed out.'
        }
        [pscustomobject]@{
            ExitCode = $process.ExitCode
            Output = $stdoutTask.GetAwaiter().GetResult() + $stderrTask.GetAwaiter().GetResult()
        }
    }
    finally { $process.Dispose() }
}

try {
    New-Item -ItemType Directory -Path $testRoot | Out-Null
    foreach ($hostName in $PowerShellPath) {
        $hostCommand = Get-Command $hostName -ErrorAction Stop
        foreach ($mode in @('Preview', 'WhatIf', 'Execute', 'CredentialFailure', 'RunningVSCode', 'XdgConfig')) {
            $caseDirectory = Join-Path $testRoot ([guid]::NewGuid().ToString('N'))
            $fixture = New-Fixture $caseDirectory
            if ($mode -eq 'RunningVSCode') {
                $database = Join-Path $fixture.AppData 'Code\User\globalStorage\state.vscdb'
                New-Item -ItemType Directory -Path (Split-Path -Parent $database) -Force | Out-Null
                Set-Content -LiteralPath $database -Value 'do-not-open-while-code-runs' -Encoding UTF8
            }
            $before = Get-ProfileSnapshot $fixture.Profile
            $result = Invoke-Fixture $hostCommand.Source $fixture $mode
            $script:lastCaseOutput = $result.Output
            $expectedExitCode = if ($mode -in @('CredentialFailure', 'RunningVSCode')) { 1 } else { 0 }
            Assert-Condition ($result.ExitCode -eq $expectedExitCode) "$hostName $mode returned $($result.ExitCode), expected $expectedExitCode."
            $calls = @()
            if (Test-Path -LiteralPath $fixture.Log) {
                $calls = @(Get-Content -LiteralPath $fixture.Log | ForEach-Object { $_ | ConvertFrom-Json })
            }
            Assert-Condition (@($calls | Where-Object { $_.kind -eq 'gh-call' }).Count -eq 0) "$hostName $mode invoked gh, which may refresh tokens or prompt."
            if ($mode -in @('Preview', 'WhatIf')) {
                $after = Get-ProfileSnapshot $fixture.Profile
                $difference = Compare-Object ($before -split "`n") ($after -split "`n") | Out-String
                Assert-Condition ($after -ceq $before) "$hostName $mode changed profile files:`n$difference"
                Assert-Condition ($calls.Count -eq 0) "$hostName $mode invoked a credential mutation."
            }
            else {
                $remainingKeys = @(& $realGit config --file $fixture.Config --name-only --list)
                foreach ($key in @('user.name', 'user.email', 'user.signingkey', 'credential.username', 'github.user',
                    'credential.https://github.com.username', 'credential.https://github.com.helper', 'http.https://github.com/.extraheader',
                    'http.https://student@github.com:443/.extraheader')) {
                    Assert-Condition ($remainingKeys -notcontains $key) "$hostName left Git setting '$key'."
                }
                foreach ($key in @('credential.helper', 'credential.https://example.invalid.username', 'core.editor',
                    'http.https://github.com.evil.invalid/.extraheader')) {
                    Assert-Condition ($remainingKeys -contains $key) "$hostName removed unrelated Git setting '$key'."
                }
                $includedKeys = @(& $realGit config --file $fixture.IncludedConfig --name-only --list)
                Assert-Condition ($includedKeys -notcontains 'user.name') "$hostName left identity in an included config file."
                Assert-Condition ($includedKeys -notcontains 'credential.https://github.com/classroom.username') "$hostName left GitHub credentials in an included config file."
                Assert-Condition ($includedKeys -contains 'core.autocrlf') "$hostName removed unrelated included Git config."
                if ($mode -eq 'XdgConfig') {
                    $xdgKeys = @(& $realGit config --file $fixture.XdgConfig --name-only --list)
                    Assert-Condition ($xdgKeys -notcontains 'user.name') "$hostName left identity in the XDG global config."
                    Assert-Condition ($xdgKeys -notcontains 'credential.https://github.com.username') "$hostName left GitHub credentials in the XDG global config."
                    Assert-Condition ($xdgKeys -contains 'core.autocrlf') "$hostName removed unrelated XDG global config."
                }
                $rejects = @($calls | Where-Object { $_.kind -eq 'credential-reject' })
                Assert-Condition ($rejects.Count -gt 0) "$hostName did not reject stored Git credentials."
                Assert-Condition (@($rejects | Where-Object { $_.data.helper -eq 'fixture-safe-helper' }).Count -gt 0) "$hostName rejected credentials after deleting the helper."
                Assert-Condition (@($rejects | Where-Object { $_.data.request -match 'host=github\.com' }).Count -gt 0) "$hostName did not send GitHub credential context."
                $deletions = @($calls | Where-Object { $_.kind -eq 'credential-delete' })
                foreach ($target in @('git:https://github.com', 'gh:github.com:fixture-student', 'gh:github.com:another-student')) {
                    Assert-Condition (@($deletions | Where-Object { $_.data.target -eq $target }).Count -eq 1) "$hostName did not attempt removal of native credential '$target'."
                }
                foreach ($path in @('.git-credentials', '.config\git\credentials', '.config\gh\hosts.yml', 'custom gh\hosts.yml',
                    'AppData\Roaming\GitHub CLI\hosts.yml', '.ssh\id_ed25519', '.ssh\id_ed25519.pub')) {
                    Assert-Condition (-not (Test-Path -LiteralPath (Join-Path $fixture.Profile $path))) "$hostName left cleanup target '$path'."
                }
                foreach ($path in @('.config\gh\config.yml', 'custom gh\config.yml', 'custom gh\unrelated.txt', 'AppData\Roaming\GitHub CLI\config.yml')) {
                    Assert-Condition (Test-Path -LiteralPath (Join-Path $fixture.Profile $path)) "$hostName removed unrelated CLI settings '$path'."
                }
                Assert-Condition (Test-Path -LiteralPath (Join-Path $fixture.Profile '.ssh\custom_key')) "$hostName removed a custom SSH key."
                Assert-Condition (Test-Path -LiteralPath (Join-Path $fixture.AppData 'Code\User\settings.json')) "$hostName removed VS Code settings."
                $hosts = Get-Content -Raw -LiteralPath (Join-Path $fixture.Profile '.ssh\known_hosts')
                Assert-Condition ($hosts -notmatch 'github\.com') "$hostName left the GitHub known_hosts entry."
                Assert-Condition ($hosts -match 'example\.invalid') "$hostName removed another host's trust entry."
                if ($mode -eq 'CredentialFailure') {
                    Assert-Condition ($result.Output -match '\[WARN\].*Simulated credential deletion failure') "$hostName hid a failed credential removal."
                    Assert-Condition ($result.Output -match 'warnings: 1') "$hostName did not report the failed cleanup in its summary."
                }
                if ($mode -eq 'RunningVSCode') {
                    Assert-Condition ($result.Output -match '\[WARN\] VS Code is running') "$hostName did not explain why VS Code cleanup was skipped."
                    Assert-Condition ((Get-Content -Raw -LiteralPath $database).Trim() -eq 'do-not-open-while-code-runs') "$hostName edited a VS Code database while Code was running."
                    Assert-Condition ($result.Output -notmatch 'Unable to inspect VS Code authentication database') "$hostName attempted to open a VS Code database while Code was running."
                }
            }
            Write-Host "PASS $hostName $mode"
        }
    }
    Write-Host "Passed $assertions assertions. No real user credentials or profile files were used."
}
finally {
    if (Test-Path -LiteralPath $testRoot) {
        $resolvedTestRoot = [IO.Path]::GetFullPath($testRoot)
        $resolvedTemp = [IO.Path]::GetFullPath([IO.Path]::GetTempPath()).TrimEnd('\') + '\'
        if (-not $resolvedTestRoot.StartsWith($resolvedTemp, [StringComparison]::OrdinalIgnoreCase) -or
            [IO.Path]::GetFileName($resolvedTestRoot) -notlike 'classroom-reset-test-*') {
            throw "Refusing to remove unverified test directory: $resolvedTestRoot"
        }
        Remove-Item -LiteralPath $resolvedTestRoot -Recurse -Force
    }
}
