# Native Command Execution from PowerShell

Use this reference when PowerShell launches `.exe`, `.cmd`, `.bat`, package managers, compilers, Git, Python, Node, .NET tools, or other native programs.

## Distinguish PowerShell commands from native programs

PowerShell cmdlets participate in PowerShell parameter binding, error streams, and common parameters.

Native programs receive command-line arguments and byte/text streams according to their own contracts. Do not append PowerShell-only parameters such as `-WhatIf` to native programs unless that program independently defines such a flag.

## Prefer argument boundaries over command strings

Avoid:

```powershell
$command = "git commit -m `"$message`""
Invoke-Expression $command
```

Prefer:

```powershell
$gitArgs = @(
    'commit'
    '-m'
    $message
)

& git @gitArgs

if ($LASTEXITCODE -ne 0) {
    throw "git failed with exit code $LASTEXITCODE"
}
```

This reduces quoting errors for spaces, non-ASCII text, JSON, and shell metacharacters.

## Native exit codes

`$ErrorActionPreference = 'Stop'` is not a universal substitute for native exit-code handling.

After a native tool whose exit status matters:

```powershell
& tool.exe @args

if ($LASTEXITCODE -ne 0) {
    throw "tool.exe failed with exit code $LASTEXITCODE"
}
```

Some tools intentionally use nonzero codes for nonfatal states; honor that tool's documented contract.

## Native stdin encoding

PowerShell uses `$OutputEncoding` when piping text into native applications.

Do not change it globally for one tool. Use a scoped change and restore it:

```powershell
$oldOutputEncoding = $OutputEncoding

try {
    $OutputEncoding = [System.Text.Encoding]::GetEncoding(936)
    $text | legacy-tool.exe
}
finally {
    $OutputEncoding = $oldOutputEncoding
}
```

Choose 936/932/949/950/UTF-8 because the target program requires it, not because of the Windows language.

## Native stdout/stderr encoding

Native programs may emit UTF-8, a legacy Windows code page, or a tool-specific encoding. Inspect the tool's documentation or verified behavior.

Do not assume that changing `$OutputEncoding` fixes native output decoding: `$OutputEncoding` controls PowerShell -> native stdin, not file output and not every native stdout decoding path.

## CMD and batch files

`.cmd` and `.bat` ultimately execute under `cmd.exe` semantics. Their argument parsing, percent expansion, metacharacters, and console code page are not the same as PowerShell.

For untrusted or complex arguments, prefer a native executable/API that supports structured arguments rather than constructing a batch command string.

## Destructive native commands

For native tools:

1. Use the tool's own dry-run/preview flag when available.
2. Otherwise inspect and display the exact target set.
3. Require confirmation when the operation is destructive and not already clearly authorized.
4. Never append PowerShell `-WhatIf` mechanically to a native command.

## Related references

- `windows-text-encoding.md` for code pages, BOM, console and file boundaries.
- `powershell-vs-cmd.md` for shell-specific quoting and parsing.
- `common-pitfalls.md` for common Windows shell mistakes.
