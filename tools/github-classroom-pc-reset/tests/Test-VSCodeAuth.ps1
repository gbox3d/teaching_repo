[CmdletBinding()]
param()

# Run with either host; no Python, SQLite CLI, Pester or user profile access needed:
# powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\tests\Test-VSCodeAuth.ps1
# pwsh.exe -NoProfile -File .\tests\Test-VSCodeAuth.ps1
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
. (Join-Path (Split-Path -Parent $PSScriptRoot) 'Windows-VSCodeAuth.ps1')
$assertions = 0
$testRoot = Join-Path ([IO.Path]::GetTempPath()) ('classroom-vscode-test-' + [guid]::NewGuid().ToString('N') + '-' + [char]0xD559 + [char]0xC0DD)

function Assert-Condition {
    param([bool]$Condition, [string]$Message)
    if (-not $Condition) { throw $Message }
    $script:assertions++
}

function Assert-Rejected {
    param([scriptblock]$Operation, [string]$Message)
    $rejected = $false
    try { & $Operation | Out-Null } catch { $rejected = $true }
    Assert-Condition $rejected $Message
}

# This fixture boundary creates only synthetic databases below $testRoot. The
# production helper deliberately does not offer database creation or arbitrary SQL.
if (-not ('GitHubClassroomReset.Tests.VSCodeFixture' -as [type])) {
    Add-Type -ErrorAction Stop -TypeDefinition @'
using System;
using System.IO;
using System.Runtime.InteropServices;
using System.Text;

namespace GitHubClassroomReset.Tests
{
    public static class VSCodeFixture
    {
        [DllImport("winsqlite3.dll", CallingConvention = CallingConvention.Cdecl)]
        private static extern int sqlite3_open_v2(byte[] filename, out IntPtr db, int flags, IntPtr vfs);
        [DllImport("winsqlite3.dll", CallingConvention = CallingConvention.Cdecl)]
        private static extern int sqlite3_close(IntPtr db);
        [DllImport("winsqlite3.dll", CallingConvention = CallingConvention.Cdecl)]
        private static extern int sqlite3_exec(IntPtr db, byte[] sql, IntPtr callback, IntPtr state, out IntPtr error);
        [DllImport("winsqlite3.dll", CallingConvention = CallingConvention.Cdecl)]
        private static extern void sqlite3_free(IntPtr memory);
        [DllImport("winsqlite3.dll", CallingConvention = CallingConvention.Cdecl)]
        private static extern int sqlite3_prepare_v2(IntPtr db, byte[] sql, int length, out IntPtr statement, IntPtr tail);
        [DllImport("winsqlite3.dll", CallingConvention = CallingConvention.Cdecl)]
        private static extern int sqlite3_step(IntPtr statement);
        [DllImport("winsqlite3.dll", CallingConvention = CallingConvention.Cdecl)]
        private static extern int sqlite3_column_int(IntPtr statement, int column);
        [DllImport("winsqlite3.dll", CallingConvention = CallingConvention.Cdecl)]
        private static extern int sqlite3_finalize(IntPtr statement);

        private static byte[] Utf8(string value) { return Encoding.UTF8.GetBytes(value + "\0"); }
        private static void Check(int result)
        {
            if (result != 0) throw new IOException("Synthetic SQLite fixture failed (code " + result + ").");
        }
        private static IntPtr Open(string path, bool create)
        {
            IntPtr db;
            int result = sqlite3_open_v2(Utf8(Path.GetFullPath(path)), out db, create ? 6 : 2, IntPtr.Zero);
            if (result != 0) { if (db != IntPtr.Zero) sqlite3_close(db); Check(result); }
            return db;
        }
        private static void Execute(IntPtr db, string sql)
        {
            IntPtr error;
            int result = sqlite3_exec(db, Utf8(sql), IntPtr.Zero, IntPtr.Zero, out error);
            if (error != IntPtr.Zero) sqlite3_free(error);
            Check(result);
        }
        public static void Create(string path)
        {
            IntPtr db = Open(path, true);
            try
            {
                Execute(db,
                    "CREATE TABLE ItemTable(key TEXT UNIQUE ON CONFLICT REPLACE, value BLOB);" +
                    "INSERT INTO ItemTable VALUES('secret://{\"extensionId\":\"vscode.github-authentication\",\"key\":\"github.auth\"}', 'DUMMY-GITHUB-SECRET');" +
                    "INSERT INTO ItemTable VALUES('secret://{\"extensionId\":\"vscode.github-authentication\",\"key\":\"school.example.ghes.auth\"}', 'DUMMY-ENTERPRISE-SECRET');" +
                    "INSERT INTO ItemTable VALUES('vscode.github-authentication', '{}');" +
                    "INSERT INTO ItemTable VALUES('secret://{\"extensionId\":\"vscode.microsoft-authentication\",\"key\":\"accounts\"}', 'UNRELATED-MICROSOFT-SECRET');" +
                    "INSERT INTO ItemTable VALUES('secret://{\"extensionId\":\"vscode.github-authentication-other\",\"key\":\"github.auth\"}', 'UNRELATED-EXTENSION-SECRET');" +
                    "INSERT INTO ItemTable VALUES('settings.fixture', 'KEEP-THIS');" +
                    "INSERT INTO ItemTable VALUES('history.github.com', 'KEEP-HISTORY');");
            }
            finally { sqlite3_close(db); }
        }
        public static int Scalar(string path, string sql)
        {
            IntPtr db = Open(path, false);
            try
            {
                IntPtr statement;
                Check(sqlite3_prepare_v2(db, Utf8(sql), -1, out statement, IntPtr.Zero));
                try
                {
                    int result = sqlite3_step(statement);
                    if (result != 100) throw new IOException("Synthetic SQLite scalar query failed (code " + result + ").");
                    return sqlite3_column_int(statement, 0);
                }
                finally { sqlite3_finalize(statement); }
            }
            finally { sqlite3_close(db); }
        }
        public static IntPtr Lock(string path)
        {
            IntPtr db = Open(path, false);
            try { Execute(db, "BEGIN EXCLUSIVE;"); return db; }
            catch { sqlite3_close(db); throw; }
        }
        public static IntPtr OpenWal(string path)
        {
            IntPtr db = Open(path, false);
            try
            {
                Execute(db, "PRAGMA journal_mode = WAL; UPDATE ItemTable SET value = 'DUMMY-GITHUB-WAL-SECRET' WHERE key = 'vscode.github-authentication';");
                return db;
            }
            catch { sqlite3_close(db); throw; }
        }
        public static void Close(IntPtr db) { Check(sqlite3_close(db)); }
        public static void Unlock(IntPtr db)
        {
            try { Execute(db, "ROLLBACK;"); }
            finally { sqlite3_close(db); }
        }
    }
}
'@
}

try {
    New-Item -ItemType Directory -Path $testRoot | Out-Null
    $userDataRoots = @((Join-Path $testRoot 'Code'), (Join-Path $testRoot 'Code - Insiders'))
    $sharedDataRoots = @((Join-Path $testRoot '.vscode-shared'), (Join-Path $testRoot '.vscode-insiders-shared'))
    $expectedPaths = @(
        foreach ($root in $userDataRoots) {
            foreach ($relative in @('User\globalStorage', 'User\profiles\fixture\globalStorage')) {
                $directory = Join-Path $root $relative
                New-Item -ItemType Directory -Path $directory -Force | Out-Null
                $database = Join-Path $directory 'state.vscdb'
                [GitHubClassroomReset.Tests.VSCodeFixture]::Create($database)
                Copy-Item -LiteralPath $database -Destination ($database + '.backup')
                $database
                $database + '.backup'
            }
        }
        foreach ($root in $sharedDataRoots) {
            $directory = Join-Path $root 'sharedStorage'
            New-Item -ItemType Directory -Path $directory -Force | Out-Null
            $database = Join-Path $directory 'state.vscdb'
            [GitHubClassroomReset.Tests.VSCodeFixture]::Create($database)
            Copy-Item -LiteralPath $database -Destination ($database + '.backup')
            $database
            $database + '.backup'
        }
    )
    # Workspace state is outside the authentication scan even when its basename
    # matches. This catches accidental recursive searches of all user data.
    $workspaceDirectory = Join-Path $userDataRoots[0] 'User\workspaceStorage\fixture'
    New-Item -ItemType Directory -Path $workspaceDirectory -Force | Out-Null
    $workspaceDatabase = Join-Path $workspaceDirectory 'state.vscdb'
    [GitHubClassroomReset.Tests.VSCodeFixture]::Create($workspaceDatabase)

    $databases = @(Get-VSCodeAuthDatabasePaths -UserDataDirectories ($userDataRoots + $userDataRoots[0]) -SharedDataDirectories $sharedDataRoots)
    Assert-Condition ($databases.Count -eq 12) 'Expected 12 unique default/profile/shared database and backup paths.'
    foreach ($path in $expectedPaths) { Assert-Condition ($databases -contains $path) ('Missing database path: ' + $path) }
    Assert-Condition ($databases -notcontains $workspaceDatabase) 'Workspace storage entered the authentication scan.'
    Assert-Condition (@(Get-VSCodeAuthDatabasePaths -UserDataDirectories (Join-Path $testRoot 'absent')).Count -eq 0) 'Absent user data produced database paths.'

    foreach ($database in $databases) {
        $before = (Get-FileHash -LiteralPath $database -Algorithm SHA256).Hash
        Assert-Condition ((Get-VSCodeGitHubAuthEntryCount -LiteralPath $database) -eq 3) 'Incorrect GitHub entry count.'
        Assert-Condition ((Get-FileHash -LiteralPath $database -Algorithm SHA256).Hash -ceq $before) 'Preview changed database bytes.'
        Assert-Condition ((Remove-VSCodeGitHubAuthEntries -LiteralPath $database) -eq 3) 'Selective cleanup removed an unexpected number of rows.'
        Assert-Condition ((Get-VSCodeGitHubAuthEntryCount -LiteralPath $database) -eq 0) 'GitHub auth entries remain.'
        Assert-Condition ((Remove-VSCodeGitHubAuthEntries -LiteralPath $database) -eq 0) 'Repeated cleanup removed additional rows.'
        Assert-Condition ([GitHubClassroomReset.Tests.VSCodeFixture]::Scalar($database, 'SELECT COUNT(*) FROM ItemTable') -eq 4) 'Unrelated rows were removed.'
        Assert-Condition ([GitHubClassroomReset.Tests.VSCodeFixture]::Scalar($database, "SELECT COUNT(*) FROM ItemTable WHERE value IN ('UNRELATED-MICROSOFT-SECRET','UNRELATED-EXTENSION-SECRET','KEEP-THIS','KEEP-HISTORY')") -eq 4) 'Unrelated row values were changed.'
        Assert-Condition ([GitHubClassroomReset.Tests.VSCodeFixture]::Scalar($database, "SELECT COUNT(*) FROM pragma_integrity_check WHERE integrity_check = 'ok'") -eq 1) 'Cleaned database failed integrity verification.'
        $databaseBytes = [Text.Encoding]::UTF8.GetString([IO.File]::ReadAllBytes($database))
        Assert-Condition (-not $databaseBytes.Contains('DUMMY-GITHUB-SECRET')) 'Deleted GitHub token data remained in free database pages.'
        Assert-Condition (-not $databaseBytes.Contains('DUMMY-ENTERPRISE-SECRET')) 'Deleted Enterprise token data remained in free database pages.'
    }
    Assert-Condition ((Get-VSCodeGitHubAuthEntryCount -LiteralPath $workspaceDatabase) -eq 3) 'Workspace fixture was changed.'

    $missingDatabase = Join-Path $testRoot 'missing.vscdb'
    Assert-Rejected { Get-VSCodeGitHubAuthEntryCount -LiteralPath $missingDatabase } 'Missing database was accepted for preview.'
    Assert-Rejected { Remove-VSCodeGitHubAuthEntries -LiteralPath $missingDatabase } 'Missing database was accepted for cleanup.'
    Assert-Condition (-not (Test-Path -LiteralPath $missingDatabase)) 'Missing database was created by inspection or cleanup.'

    $invalidDatabase = Join-Path $testRoot 'invalid.vscdb'
    Set-Content -LiteralPath $invalidDatabase -Value 'This is a synthetic non-SQLite file.' -Encoding ASCII
    $beforeInvalid = (Get-FileHash -LiteralPath $invalidDatabase -Algorithm SHA256).Hash
    Assert-Rejected { Get-VSCodeGitHubAuthEntryCount -LiteralPath $invalidDatabase } 'Malformed database was accepted for preview.'
    Assert-Rejected { Remove-VSCodeGitHubAuthEntries -LiteralPath $invalidDatabase } 'Malformed database was accepted for cleanup.'
    Assert-Condition ((Get-FileHash -LiteralPath $invalidDatabase -Algorithm SHA256).Hash -ceq $beforeInvalid) 'Malformed file was altered.'

    $lockedDatabase = Join-Path $testRoot 'locked.vscdb'
    [GitHubClassroomReset.Tests.VSCodeFixture]::Create($lockedDatabase)
    $beforeLocked = (Get-FileHash -LiteralPath $lockedDatabase -Algorithm SHA256).Hash
    $lockHandle = [GitHubClassroomReset.Tests.VSCodeFixture]::Lock($lockedDatabase)
    try {
        Assert-Rejected { Get-VSCodeGitHubAuthEntryCount -LiteralPath $lockedDatabase } 'Locked database was accepted for preview.'
        Assert-Rejected { Remove-VSCodeGitHubAuthEntries -LiteralPath $lockedDatabase } 'Locked database was accepted for cleanup.'
    }
    finally { [GitHubClassroomReset.Tests.VSCodeFixture]::Unlock($lockHandle) }
    Assert-Condition ((Get-FileHash -LiteralPath $lockedDatabase -Algorithm SHA256).Hash -ceq $beforeLocked) 'Locked database was altered.'
    Assert-Condition ((Get-VSCodeGitHubAuthEntryCount -LiteralPath $lockedDatabase) -eq 3) 'Locked database lost its original GitHub entries.'

    $walDatabase = Join-Path $testRoot 'wal.vscdb'
    [GitHubClassroomReset.Tests.VSCodeFixture]::Create($walDatabase)
    $walHandle = [GitHubClassroomReset.Tests.VSCodeFixture]::OpenWal($walDatabase)
    try {
        Assert-Condition ((Get-Item -LiteralPath ($walDatabase + '-wal')).Length -gt 0) 'WAL fixture did not create journal frames.'
        Assert-Condition ((Get-VSCodeGitHubAuthEntryCount -LiteralPath $walDatabase) -eq 3) 'Preview missed GitHub entries in WAL mode.'
        Assert-Condition ((Remove-VSCodeGitHubAuthEntries -LiteralPath $walDatabase) -eq 3) 'WAL cleanup removed an unexpected number of rows.'
        Assert-Condition ((Get-Item -LiteralPath ($walDatabase + '-wal')).Length -eq 0) 'Old encrypted GitHub sessions remain in WAL frames.'
        Assert-Condition ([GitHubClassroomReset.Tests.VSCodeFixture]::Scalar($walDatabase, 'SELECT COUNT(*) FROM ItemTable') -eq 4) 'WAL cleanup removed unrelated rows.'
    }
    finally { [GitHubClassroomReset.Tests.VSCodeFixture]::Close($walHandle) }

    Write-Host ("PASS VS Code auth: {0} assertions on PowerShell {1}. Only synthetic temporary databases were used." -f $assertions, $PSVersionTable.PSVersion)
}
finally {
    if (Test-Path -LiteralPath $testRoot) {
        $resolvedTestRoot = [IO.Path]::GetFullPath($testRoot)
        $resolvedTemp = [IO.Path]::GetFullPath([IO.Path]::GetTempPath()).TrimEnd('\') + '\'
        if (-not $resolvedTestRoot.StartsWith($resolvedTemp, [StringComparison]::OrdinalIgnoreCase) -or
            [IO.Path]::GetFileName($resolvedTestRoot) -notlike 'classroom-vscode-test-*') {
            throw "Refusing to remove unverified test directory: $resolvedTestRoot"
        }
        Remove-Item -LiteralPath $resolvedTestRoot -Recurse -Force
    }
}
