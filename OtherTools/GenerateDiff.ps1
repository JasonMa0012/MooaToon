[CmdletBinding()]
param(
    # Relative to this script, independent of the caller's working directory.
    [string]$RepositoryPath = '..\MooaToon-Engine',
    [string]$EpicRemote = 'epic',
    # Defaults to the current branch name, e.g. 5.7.
    [string]$BaseBranch = '',
    # Upgrade destination for display; the patch still exports the current HEAD.
    [string]$TargetBranch = '5.8',
    # Semicolon- or newline-separated paths for callers such as cmd.exe; overrides ExcludePaths.
    [AllowEmptyString()]
    [string]$ExcludePathsText,
    # Relative to the repository root.
    [string]$OutputPath = 'diff.patch',
    [string[]]$ExcludePaths = @(
        'Engine/Plugins/MooaToonThirdparty',
        'Engine/Build/Commit.gitdeps.xml'
    )
)

$ErrorActionPreference = 'Stop'
if ($PSBoundParameters.ContainsKey('ExcludePathsText')) {
    $ExcludePaths = @($ExcludePathsText -split '[;\r\n]' | ForEach-Object { $_.Trim() } | Where-Object { $_ -ne '' })
}
function Invoke-Git {
    param([string[]]$GitArguments)
    $result = & git -C $script:RepositoryRoot @GitArguments
    if ($LASTEXITCODE -ne 0) { throw "Git failed ($LASTEXITCODE): $($GitArguments -join ' ')" }
    return $result
}

$RepositoryRoot = if ([IO.Path]::IsPathRooted($RepositoryPath)) {
    [IO.Path]::GetFullPath($RepositoryPath)
} else {
    [IO.Path]::GetFullPath((Join-Path $PSScriptRoot $RepositoryPath))
}
$RepositoryRoot = [IO.Path]::GetFullPath(([string](Invoke-Git @('rev-parse', '--show-toplevel'))).Trim())
if ([string]::IsNullOrWhiteSpace($BaseBranch)) {
    $BaseBranch = Invoke-Git @('symbolic-ref', '--quiet', '--short', 'HEAD')
}
$remotes = @(Invoke-Git @('remote'))
if ($EpicRemote -notin $remotes) { throw "Remote does not exist: $EpicRemote" }
$baseRef = "refs/remotes/$EpicRemote/$BaseBranch"
$baseCommit = Invoke-Git @('rev-parse', '--verify', "$baseRef^{commit}")
$headCommit = Invoke-Git @('rev-parse', '--verify', 'HEAD')
Invoke-Git @('merge-base', '--is-ancestor', $baseCommit, $headCommit)

Write-Host "Repository: $RepositoryRoot"
Write-Host "Epic remote: $EpicRemote"
Write-Host "Source baseline: $EpicRemote/$BaseBranch -> HEAD"
Write-Host "Upgrade target: $TargetBranch (display only; no checkout or apply)"
Write-Host 'Excluded repository-relative directories/files:'
if ($ExcludePaths.Count -eq 0) { Write-Host '  (none)' }
foreach ($excludedPath in $ExcludePaths) { Write-Host "  $excludedPath" }

$pathspecs = @('.')
foreach ($excludedPath in $ExcludePaths) {
    $normalized = $excludedPath.Replace('\', '/').TrimEnd('/')
    if ([string]::IsNullOrWhiteSpace($normalized) -or [IO.Path]::IsPathRooted($normalized) -or $normalized -match '(^|/)\.\.(/|$)') {
        throw "Exclusions must be repository-relative paths: $excludedPath"
    }
    $pathspecs += ":(top,exclude,literal)$normalized"
}
$destination = if ([IO.Path]::IsPathRooted($OutputPath)) {
    [IO.Path]::GetFullPath($OutputPath)
} else {
    [IO.Path]::GetFullPath((Join-Path $RepositoryRoot $OutputPath))
}
if (Test-Path -LiteralPath $destination -PathType Container) { throw "Output is a directory: $destination" }
$trackedOutput = @(Invoke-Git @('ls-files', '--', $destination))
if ($trackedOutput.Count -gt 0) { throw 'Output must not overwrite a tracked file.' }

# Check only the exported scope. The output patch itself is allowed to be an
# untracked file because this script intentionally overwrites it in place.
$repositoryPrefix = $RepositoryRoot.TrimEnd('\', '/') + '\'
$normalizedDestination = $destination.Replace('/', '\')
$relativeDestination = if ($normalizedDestination.StartsWith($repositoryPrefix, [StringComparison]::OrdinalIgnoreCase)) {
    $normalizedDestination.Substring($repositoryPrefix.Length).Replace('\', '/')
} else {
    $null
}
$changes = @(Invoke-Git (@('status', '--porcelain', '--untracked-files=normal', '--') + $pathspecs))
$changes = @($changes | Where-Object {
    $line = [string]$_
    if ($line.StartsWith('?? ')) {
        $reportedPath = $line.Substring(3).Trim('"').Replace('\', '/')
        return $null -eq $relativeDestination -or $reportedPath -ne $relativeDestination
    }
    return $true
})
if ($changes.Count -gt 0) {
    throw "Export scope has uncommitted/untracked changes. Commit or preserve them separately before exporting HEAD:`n$($changes -join "`n")"
}
$parentDir = Split-Path -Parent $destination
if (-not (Test-Path -LiteralPath $parentDir -PathType Container)) { throw "Output directory does not exist: $parentDir" }
$temporary = "$destination.tmp-$([Guid]::NewGuid().ToString('N'))"
try {
    Invoke-Git (@('diff', '--binary', '--full-index', '--no-ext-diff', '--no-textconv', "--output=$temporary", $baseCommit, $headCommit, '--') + $pathspecs)
    if ((Get-Item -LiteralPath $temporary).Length -eq 0) { throw 'No differences; previous patch was preserved.' }
    Invoke-Git @('apply', '--reverse', '--check', '--binary', $temporary)
    Move-Item -LiteralPath $temporary -Destination $destination -Force
} finally {
    if (Test-Path -LiteralPath $temporary) { Remove-Item -LiteralPath $temporary }
}
Write-Host "Base: $baseRef ($baseCommit)"
Write-Host "HEAD: $headCommit"
Invoke-Git @('apply', '--stat', $destination) | Select-Object -Last 1
Write-Host "Patch: $destination ($((Get-Item -LiteralPath $destination).Length) bytes)"
$sha256 = [Security.Cryptography.SHA256]::Create()
$stream = [IO.File]::OpenRead($destination)
try {
    $hash = [BitConverter]::ToString($sha256.ComputeHash($stream)).Replace('-', '')
    Write-Host "SHA256: $hash"
} finally {
    $stream.Dispose()
    $sha256.Dispose()
}
