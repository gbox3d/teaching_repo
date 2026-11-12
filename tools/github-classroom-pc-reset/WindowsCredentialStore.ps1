# Windows Credential Manager access without parsing localized cmdkey output.
# Only credential names and types are copied; password/token blobs are never read.

function Initialize-WindowsCredentialStore {
    if ('GitHubClassroomReset.WindowsCredentials.NativeStore' -as [type]) {
        return
    }

    Add-Type -ErrorAction Stop -TypeDefinition @'
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Runtime.InteropServices;

namespace GitHubClassroomReset.WindowsCredentials
{
    public sealed class CredentialTarget
    {
        public string Target { get; set; }
        public uint Type { get; set; }
    }

    public static class NativeStore
    {
        // Only the header of CREDENTIALW is marshalled. In particular,
        // CredentialBlob and UserName are not accessed.
        [StructLayout(LayoutKind.Sequential)]
        private struct CredentialHeader
        {
            public uint Flags;
            public uint Type;
            public IntPtr TargetName;
        }

        [DllImport("advapi32.dll", EntryPoint = "CredEnumerateW", CharSet = CharSet.Unicode,
            SetLastError = true, ExactSpelling = true)]
        [return: MarshalAs(UnmanagedType.Bool)]
        private static extern bool CredEnumerate(string filter, uint flags,
            out uint count, out IntPtr credentials);

        [DllImport("advapi32.dll", EntryPoint = "CredDeleteW", CharSet = CharSet.Unicode,
            SetLastError = true, ExactSpelling = true)]
        [return: MarshalAs(UnmanagedType.Bool)]
        private static extern bool CredDelete(string target, uint type, uint flags);

        [DllImport("advapi32.dll", ExactSpelling = true)]
        private static extern void CredFree(IntPtr buffer);

        public static CredentialTarget[] Enumerate()
        {
            uint count;
            IntPtr credentials;
            if (!CredEnumerate(null, 0, out count, out credentials))
            {
                int error = Marshal.GetLastWin32Error();
                if (error == 1168) // ERROR_NOT_FOUND: an empty credential set.
                    return new CredentialTarget[0];
                throw new Win32Exception(error, "Windows credential enumeration failed (Win32 " + error + ").");
            }

            try
            {
                var result = new List<CredentialTarget>();
                for (uint index = 0; index < count; index++)
                {
                    IntPtr entry = Marshal.ReadIntPtr(credentials, checked((int)index * IntPtr.Size));
                    var header = (CredentialHeader)Marshal.PtrToStructure(entry, typeof(CredentialHeader));
                    result.Add(new CredentialTarget {
                        Target = Marshal.PtrToStringUni(header.TargetName),
                        Type = header.Type
                    });
                }
                return result.ToArray();
            }
            finally
            {
                CredFree(credentials);
            }
        }

        public static void Delete(string target, uint type)
        {
            if (String.IsNullOrWhiteSpace(target))
                throw new ArgumentException("A credential target is required.", "target");
            if (!CredDelete(target, type, 0))
            {
                int error = Marshal.GetLastWin32Error();
                throw new Win32Exception(error, "Windows credential deletion failed (Win32 " + error + ").");
            }
        }
    }
}
'@
}

function Test-GitHubCredentialTarget {
    param(
        [Parameter(Mandatory = $true)][string]$Target,
        [switch]$IncludeVSCodeAuth
    )

    # Apply the VS Code opt-in first, including accounts named github.com.
    if ($Target -match '(?i)^(?:vscode|vscode-insiders)vscode\.github-authentication(?:[/:].*)?$') {
        return [bool]$IncludeVSCodeAuth
    }

    # GCM and Desktop put a URL inside their target names. Parse its host:
    # github.com can also occur in an unrelated URL's username or path.
    if ($Target -match '(?i)(?:^|[^a-z0-9+.-])(https?://\S+)') {
        $credentialUri = $null
        if (-not [Uri]::TryCreate($Matches[1], [UriKind]::Absolute, [ref]$credentialUri)) {
            return $false
        }
        return ($credentialUri.Host -ieq 'github.com' -or
            $credentialUri.Host.EndsWith('.github.com', [StringComparison]::OrdinalIgnoreCase))
    }

    # gh uses service:hostname:account rather than a URL. Plain host targets
    # can also be present in Windows Credential Manager.
    return ($Target -match '(?i)^gh:(?:[a-z0-9-]+\.)*github\.com(?::.*)?$' -or
        $Target -match '(?i)^(?:[a-z0-9-]+\.)*github\.com(?::[0-9]+)?$')
}

function Get-WindowsCredentialTargets {
    param([switch]$IncludeVSCodeAuth)

    Initialize-WindowsCredentialStore
    [GitHubClassroomReset.WindowsCredentials.NativeStore]::Enumerate() |
        Where-Object { Test-GitHubCredentialTarget -Target $_.Target -IncludeVSCodeAuth:$IncludeVSCodeAuth }
}

function Remove-WindowsCredentialTarget {
    param(
        [Parameter(Mandatory = $true)][ValidateNotNullOrEmpty()][string]$Target,
        [Parameter(Mandatory = $true)][uint32]$Type
    )

    Initialize-WindowsCredentialStore
    [GitHubClassroomReset.WindowsCredentials.NativeStore]::Delete($Target, $Type)
}
