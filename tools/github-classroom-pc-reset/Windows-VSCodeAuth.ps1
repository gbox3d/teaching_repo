# Selective VS Code GitHub SecretStorage cleanup for Windows PowerShell 5.1+.
# VS Code stores encrypted secrets as ItemTable rows, not extension directories.
# Sources:
# https://github.com/microsoft/vscode/blob/main/src/vs/workbench/api/browser/mainThreadSecretState.ts
# https://github.com/microsoft/vscode/blob/main/src/vs/platform/secrets/common/secrets.ts
# https://github.com/microsoft/vscode/blob/main/src/vs/platform/storage/electron-main/storageMain.ts

function Initialize-VSCodeAuthDatabase {
    if ('GitHubClassroomReset.VSCodeAuthDatabase' -as [type]) { return }

    Add-Type -ErrorAction Stop -TypeDefinition @'
using System;
using System.IO;
using System.Runtime.InteropServices;
using System.Text;

namespace GitHubClassroomReset
{
    public static class VSCodeAuthDatabase
    {
        // The extension host constructs these keys using JSON.stringify({ extensionId, key }).
        // Match only this extension's secrets and its own extension state, never all secrets.
        private const string Predicate =
            "(key LIKE 'secret://{\"extensionId\":\"vscode.github-authentication\",%' " +
            "OR key = 'vscode.github-authentication')";

        [DllImport("winsqlite3.dll", CallingConvention = CallingConvention.Cdecl)]
        private static extern int sqlite3_open_v2(byte[] filename, out IntPtr db, int flags, IntPtr vfs);
        [DllImport("winsqlite3.dll", CallingConvention = CallingConvention.Cdecl)]
        private static extern int sqlite3_close(IntPtr db);
        [DllImport("winsqlite3.dll", CallingConvention = CallingConvention.Cdecl)]
        private static extern int sqlite3_busy_timeout(IntPtr db, int milliseconds);
        [DllImport("winsqlite3.dll", CallingConvention = CallingConvention.Cdecl)]
        private static extern int sqlite3_prepare_v2(IntPtr db, byte[] sql, int length, out IntPtr statement, IntPtr tail);
        [DllImport("winsqlite3.dll", CallingConvention = CallingConvention.Cdecl)]
        private static extern int sqlite3_step(IntPtr statement);
        [DllImport("winsqlite3.dll", CallingConvention = CallingConvention.Cdecl)]
        private static extern int sqlite3_column_int(IntPtr statement, int column);
        [DllImport("winsqlite3.dll", CallingConvention = CallingConvention.Cdecl)]
        private static extern int sqlite3_finalize(IntPtr statement);
        [DllImport("winsqlite3.dll", CallingConvention = CallingConvention.Cdecl)]
        private static extern int sqlite3_changes(IntPtr db);
        [DllImport("winsqlite3.dll", CallingConvention = CallingConvention.Cdecl)]
        private static extern int sqlite3_exec(IntPtr db, byte[] sql, IntPtr callback, IntPtr state, out IntPtr error);
        [DllImport("winsqlite3.dll", CallingConvention = CallingConvention.Cdecl)]
        private static extern void sqlite3_free(IntPtr memory);
        [DllImport("winsqlite3.dll", CallingConvention = CallingConvention.Cdecl)]
        private static extern int sqlite3_wal_checkpoint_v2(IntPtr db, byte[] databaseName, int mode, out int logFrames, out int checkpointedFrames);

        private static byte[] Utf8(string value)
        {
            return Encoding.UTF8.GetBytes(value + "\0");
        }

        private static void Check(int result)
        {
            if (result != 0)
                throw new IOException("VS Code authentication database operation failed (SQLite code " + result + "). Close all VS Code windows and retry.");
        }

        private static IntPtr Open(string path, bool writable)
        {
            // READONLY / READWRITE without CREATE: a missing database must never be created.
            IntPtr db;
            int result = sqlite3_open_v2(Utf8(Path.GetFullPath(path)), out db, writable ? 2 : 1, IntPtr.Zero);
            if (result != 0)
            {
                if (db != IntPtr.Zero) sqlite3_close(db);
                Check(result);
            }
            try { Check(sqlite3_busy_timeout(db, 1500)); }
            catch { sqlite3_close(db); throw; }
            return db;
        }

        private static void Execute(IntPtr db, string sql)
        {
            IntPtr error;
            int result = sqlite3_exec(db, Utf8(sql), IntPtr.Zero, IntPtr.Zero, out error);
            // Do not include SQL or database contents in errors (they may contain secrets).
            if (error != IntPtr.Zero) sqlite3_free(error);
            Check(result);
        }

        private static int Count(IntPtr db)
        {
            IntPtr statement;
            Check(sqlite3_prepare_v2(db, Utf8("SELECT COUNT(*) FROM ItemTable WHERE " + Predicate), -1, out statement, IntPtr.Zero));
            try
            {
                int result = sqlite3_step(statement);
                if (result != 100) { Check(result); throw new IOException("No count returned from the VS Code authentication database."); }
                return sqlite3_column_int(statement, 0);
            }
            finally { sqlite3_finalize(statement); }
        }

        public static int CountGitHubEntries(string path)
        {
            IntPtr db = Open(path, false);
            try { return Count(db); }
            finally { sqlite3_close(db); }
        }

        public static int RemoveGitHubEntries(string path)
        {
            IntPtr db = Open(path, true);
            try
            {
                Execute(db, "PRAGMA secure_delete = ON; BEGIN IMMEDIATE;");
                int changed;
                try
                {
                    Execute(db, "DELETE FROM ItemTable WHERE " + Predicate);
                    changed = sqlite3_changes(db);
                    if (Count(db) != 0) throw new IOException("VS Code GitHub authentication entries remain after deletion.");
                    Execute(db, "COMMIT;");
                }
                catch
                {
                    try { Execute(db, "ROLLBACK;"); } catch { }
                    throw;
                }

                // Truncate any WAL so older encrypted session values are not retained there.
                int logFrames, checkpointedFrames;
                Check(sqlite3_wal_checkpoint_v2(db, Utf8("main"), 3, out logFrames, out checkpointedFrames));
                return changed;
            }
            finally { sqlite3_close(db); }
        }
    }
}
'@
}

function Get-VSCodeAuthDatabasePaths {
    param(
        [string[]]$UserDataDirectories = @(),
        [string[]]$SharedDataDirectories = @()
    )

    $storageDirectories = @(
        foreach ($directory in $UserDataDirectories) {
            if ([string]::IsNullOrWhiteSpace($directory)) { continue }
            $userDirectory = Join-Path $directory 'User'
            Join-Path $userDirectory 'globalStorage'
            $profilesDirectory = Join-Path $userDirectory 'profiles'
            if (Test-Path -LiteralPath $profilesDirectory -PathType Container) {
                Get-ChildItem -LiteralPath $profilesDirectory -Directory -ErrorAction Stop |
                    ForEach-Object { Join-Path $_.FullName 'globalStorage' }
            }
        }
        foreach ($directory in $SharedDataDirectories) {
            if (-not [string]::IsNullOrWhiteSpace($directory)) {
                Join-Path $directory 'sharedStorage'
            }
        }
    )

    @(
        foreach ($directory in $storageDirectories) {
            foreach ($name in @('state.vscdb', 'state.vscdb.backup')) {
                $databasePath = Join-Path $directory $name
                if (Test-Path -LiteralPath $databasePath -PathType Leaf) {
                    [IO.Path]::GetFullPath($databasePath)
                }
            }
        }
    ) | Sort-Object -Unique
}

function Get-VSCodeGitHubAuthEntryCount {
    param([Parameter(Mandatory = $true)][string]$LiteralPath)

    Initialize-VSCodeAuthDatabase
    [GitHubClassroomReset.VSCodeAuthDatabase]::CountGitHubEntries($LiteralPath)
}

function Remove-VSCodeGitHubAuthEntries {
    param([Parameter(Mandatory = $true)][string]$LiteralPath)

    Initialize-VSCodeAuthDatabase
    [GitHubClassroomReset.VSCodeAuthDatabase]::RemoveGitHubEntries($LiteralPath)
}
