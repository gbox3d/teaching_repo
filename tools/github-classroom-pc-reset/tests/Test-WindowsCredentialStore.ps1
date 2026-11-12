[CmdletBinding()]
param([switch]$NativeRoundTrip)

# Default checks compile the helper and test synthetic target names only.
# -NativeRoundTrip additionally creates one uniquely named fake credential,
# enumerates metadata, and deletes only that fixture. Existing secrets are never read.
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
. (Join-Path (Split-Path -Parent $PSScriptRoot) 'WindowsCredentialStore.ps1')
$assertions = 0

function Assert-Condition {
    param([bool]$Condition, [string]$Message)
    if (-not $Condition) { throw $Message }
    $script:assertions++
}

Initialize-WindowsCredentialStore
Assert-Condition ($null -ne ('GitHubClassroomReset.WindowsCredentials.NativeStore' -as [type])) 'Credential helper failed to compile.'

$cases = @(
    @('git:https://github.com', $false, $true),
    @('git:https://student@github.com/course/repo', $false, $true),
    @('git:https://student@github.com:443/course/repo', $false, $true),
    @('gh:github.com:student', $false, $true),
    @('gh:github.com:', $false, $true),
    @('GitHub - https://api.github.com', $false, $true),
    @('git:https://gist.github.com', $false, $true),
    @('git:https://GITHUB.COM', $false, $true),
    @('github.com', $false, $true),
    @('git:https://evil.com', $false, $false),
    @('git:https://notgithub.com', $false, $false),
    @('git:https://github.com.example.org', $false, $false),
    @('git:https://github.com-example.org', $false, $false),
    @('git:https://github.com@evil.com', $false, $false),
    @('git:https://evil.com/github.com', $false, $false),
    @('git:https://evil.com/path/https://github.com', $false, $false),
    @('git:https://evil.com/?redirect=https://github.com', $false, $false),
    @('gh:github.com.evil.com:student', $false, $false),
    @('mygithubaccount', $false, $false),
    @('vscodevscode.github-authentication', $false, $false),
    @('vscodevscode.github-authentication', $true, $true),
    @('vscode-insidersvscode.github-authentication/github.auth', $true, $true),
    @('vscodevscode.github-authentication/github.com', $false, $false),
    @('vscodevscode.github-authentication/github.com', $true, $true),
    @('vscodevscode.microsoft-authentication', $true, $false)
)
foreach ($case in $cases) {
    $actual = Test-GitHubCredentialTarget -Target $case[0] -IncludeVSCodeAuth:$case[1]
    Assert-Condition ($actual -eq $case[2]) ('Unexpected credential target match: ' + $case[0])
}

if ($NativeRoundTrip) {
    # Embed the nonce in the URL username so it is still an actual GitHub host
    # target. Never call reset or delete a wildcard / discovered non-fixture name.
    $fixtureTarget = 'git:https://classroom-reset-fixture-' + [guid]::NewGuid().ToString('N') + '@github.com'
    $created = $false
    try {
        $null = & cmdkey.exe "/generic:$fixtureTarget" '/user:reset-fixture' '/pass:disposable-test-value'
        if ($LASTEXITCODE -ne 0) { throw 'Disposable credential fixture creation failed.' }
        $created = $true

        $fixture = @(Get-WindowsCredentialTargets | Where-Object { $_.Target -ceq $fixtureTarget })
        Assert-Condition ($fixture.Count -eq 1) 'The disposable fixture was not enumerated exactly once.'
        Assert-Condition ($fixture[0].Type -eq 1) 'The disposable fixture did not retain its generic credential type.'
        Remove-WindowsCredentialTarget -Target $fixtureTarget -Type 1
        $created = $false
        $remaining = @(Get-WindowsCredentialTargets | Where-Object { $_.Target -ceq $fixtureTarget })
        Assert-Condition ($remaining.Count -eq 0) 'The disposable credential survived native deletion.'

        $missingReported = $false
        try { Remove-WindowsCredentialTarget -Target $fixtureTarget -Type 1 }
        catch { $missingReported = $_.Exception.Message -match '1168' }
        Assert-Condition $missingReported 'Missing credential deletion did not expose Win32 error 1168.'
    }
    finally {
        if ($created) {
            Remove-WindowsCredentialTarget -Target $fixtureTarget -Type 1
        }
    }
}

Write-Output ("PASS: Windows credential store, {0} assertions (PowerShell {1}; native fixture: {2})." -f $assertions, $PSVersionTable.PSVersion, [bool]$NativeRoundTrip)
