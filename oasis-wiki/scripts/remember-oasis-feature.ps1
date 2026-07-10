param(
    [string] $ProjectRoot = (Get-Location).Path,

    [string] $Title = '',

    [string] $Summary = '',

    [string] $Author = 'luojiawei',

    [switch] $FromLastAuthorCommit,

    [switch] $Force
)

$ErrorActionPreference = 'Stop'

function Resolve-FullPath {
    param([Parameter(Mandatory = $true)][string] $Path)
    $resolved = Resolve-Path -LiteralPath $Path -ErrorAction Stop
    return $resolved.ProviderPath
}

function Get-StringSha256Prefix {
    param(
        [Parameter(Mandatory = $true)][string] $Text,
        [int] $Length = 12
    )

    $sha = [System.Security.Cryptography.SHA256]::Create()
    try {
        $bytes = [System.Text.Encoding]::UTF8.GetBytes($Text)
        $hashBytes = $sha.ComputeHash($bytes)
        $hash = -join ($hashBytes | ForEach-Object { $_.ToString('x2') })
        return $hash.Substring(0, [Math]::Min($Length, $hash.Length))
    } finally {
        $sha.Dispose()
    }
}

function Get-SafeCacheName {
    param([Parameter(Mandatory = $true)][string] $Name)
    $safe = $Name -replace '[^A-Za-z0-9._-]', '_'
    if ([string]::IsNullOrWhiteSpace($safe)) { return 'project' }
    return $safe
}

function Get-SafeFileName {
    param([Parameter(Mandatory = $true)][string] $Name)
    $safe = $Name -replace '[\\/:*?"<>|]', '_' -replace '\s+', '-'
    $safe = $safe.Trim('.- ')
    if ([string]::IsNullOrWhiteSpace($safe)) { return 'feature' }
    if ($safe.Length -gt 80) { return $safe.Substring(0, 80).Trim('.- ') }
    return $safe
}

function Get-DefaultCacheRoot {
    $codexHome = $env:CODEX_HOME
    if ([string]::IsNullOrWhiteSpace($codexHome)) {
        $codexHome = Join-Path $env:USERPROFILE '.codex'
    }
    return Join-Path $codexHome 'oasis-project-cache'
}

function Get-ProjectCacheRoot {
    param([Parameter(Mandatory = $true)][string] $ProjectRootFull)

    $projectName = Get-SafeCacheName ([System.IO.DirectoryInfo]::new($ProjectRootFull).Name)
    $cacheKey = Get-StringSha256Prefix ([System.IO.Path]::GetFullPath($ProjectRootFull).ToLowerInvariant())
    return [pscustomobject]@{
        CacheRoot = (Join-Path (Get-DefaultCacheRoot) "$projectName-$cacheKey")
        CacheKey = $cacheKey
        ProjectName = $projectName
    }
}

function Invoke-Git {
    param(
        [Parameter(Mandatory = $true)][string] $RepoRoot,
        [Parameter(Mandatory = $true)][string[]] $Arguments
    )

    $output = & git -C $RepoRoot @Arguments 2>&1
    $exit = $LASTEXITCODE
    return [pscustomobject]@{
        ExitCode = $exit
        Text = (($output | Out-String).Trim())
    }
}

function Limit-Text {
    param(
        [AllowNull()][string] $Text,
        [int] $MaxLength = 12000
    )

    if ($null -eq $Text) { return '' }
    if ($Text.Length -le $MaxLength) { return $Text }
    return $Text.Substring(0, $MaxLength) + "`n... <truncated>"
}

$projectRootFull = Resolve-FullPath $ProjectRoot
$projectCache = Get-ProjectCacheRoot $projectRootFull
$featureRoot = Join-Path $projectCache.CacheRoot 'features'
New-Item -ItemType Directory -Path $featureRoot -Force | Out-Null

$gitTopLevelResult = Invoke-Git $projectRootFull @('rev-parse', '--show-toplevel')
$gitTopLevel = if ($gitTopLevelResult.ExitCode -eq 0) { $gitTopLevelResult.Text } else { '' }
$gitHead = (Invoke-Git $projectRootFull @('rev-parse', '--short', 'HEAD')).Text
$gitUserName = (Invoke-Git $projectRootFull @('config', 'user.name')).Text
$gitUserEmail = (Invoke-Git $projectRootFull @('config', 'user.email')).Text
$status = (Invoke-Git $projectRootFull @('status', '--short')).Text
$diffNameStatus = (Invoke-Git $projectRootFull @('diff', '--name-status')).Text
$diffStat = (Invoke-Git $projectRootFull @('diff', '--stat')).Text
$diffText = (Invoke-Git $projectRootFull @('diff', '--', '*.lua', '*.ini', '*.json', '*.csv', '*.md')).Text

$commitHash = ''
$commitSubject = ''
$commitFiles = ''
$commitShow = ''
if ($FromLastAuthorCommit -or [string]::IsNullOrWhiteSpace($status)) {
    $lastCommit = (Invoke-Git $projectRootFull @('log', '--author', $Author, '-1', '--pretty=format:%H%x09%s')).Text
    if (-not [string]::IsNullOrWhiteSpace($lastCommit)) {
        $parts = $lastCommit -split "`t", 2
        $commitHash = $parts[0]
        if ($parts.Count -gt 1) { $commitSubject = $parts[1] }
        $commitFiles = (Invoke-Git $projectRootFull @('show', '--name-status', '--pretty=format:', $commitHash)).Text
        $commitShow = (Invoke-Git $projectRootFull @('show', '--stat', '--', $commitHash)).Text
    }
}

if ([string]::IsNullOrWhiteSpace($Title)) {
    if (-not [string]::IsNullOrWhiteSpace($commitSubject)) {
        $Title = $commitSubject
    } elseif (-not [string]::IsNullOrWhiteSpace($Summary)) {
        $Title = ($Summary -split "`r?`n" | Select-Object -First 1)
    } else {
        $Title = 'Untitled feature memory'
    }
}

$timestamp = (Get-Date).ToUniversalTime().ToString('yyyyMMdd-HHmmss')
$featureId = "$timestamp-$(Get-SafeFileName $Title)"
$featurePath = Join-Path $featureRoot "$featureId.md"
if ((Test-Path -LiteralPath $featurePath) -and -not $Force) {
    throw "Feature memory already exists. Use -Force to overwrite: $featurePath"
}

$lines = New-Object System.Collections.Generic.List[string]
$lines.Add("# $Title") | Out-Null
$lines.Add('') | Out-Null
$lines.Add(('- Project: `' + $projectCache.ProjectName + '`')) | Out-Null
$lines.Add(('- Project root: `' + $projectRootFull + '`')) | Out-Null
$lines.Add(('- Cache key: `' + $projectCache.CacheKey + '`')) | Out-Null
$lines.Add("- Remembered at UTC: $((Get-Date).ToUniversalTime().ToString('o'))") | Out-Null
$lines.Add(('- Preferred author: `' + $Author + '`')) | Out-Null
$lines.Add(('- Git user: `' + $gitUserName + ' <' + $gitUserEmail + '>`')) | Out-Null
$lines.Add(('- Git HEAD: `' + $gitHead + '`')) | Out-Null
if (-not [string]::IsNullOrWhiteSpace($commitHash)) {
    $lines.Add(('- Source commit: `' + $commitHash + '` ' + $commitSubject)) | Out-Null
}
$lines.Add('') | Out-Null
$lines.Add('## Human Summary') | Out-Null
if ([string]::IsNullOrWhiteSpace($Summary)) {
    $lines.Add('- No manual summary was provided. Future agents should infer cautiously from the git evidence below and inspect source files before answering.') | Out-Null
} else {
    $lines.Add($Summary) | Out-Null
}
$lines.Add('') | Out-Null
$lines.Add('## Changed Files') | Out-Null
if (-not [string]::IsNullOrWhiteSpace($diffNameStatus)) {
    $lines.Add('```text') | Out-Null
    $lines.Add($diffNameStatus) | Out-Null
    $lines.Add('```') | Out-Null
} elseif (-not [string]::IsNullOrWhiteSpace($commitFiles)) {
    $lines.Add('```text') | Out-Null
    $lines.Add($commitFiles) | Out-Null
    $lines.Add('```') | Out-Null
} else {
    $lines.Add('- No changed files were found in the working tree or last author commit.') | Out-Null
}
$lines.Add('') | Out-Null
$lines.Add('## Git Stat') | Out-Null
$statText = if (-not [string]::IsNullOrWhiteSpace($diffStat)) { $diffStat } else { $commitShow }
if ([string]::IsNullOrWhiteSpace($statText)) {
    $lines.Add('- No git stat available.') | Out-Null
} else {
    $lines.Add('```text') | Out-Null
    $lines.Add((Limit-Text $statText 8000)) | Out-Null
    $lines.Add('```') | Out-Null
}
$lines.Add('') | Out-Null
$lines.Add('## Text Diff Snapshot') | Out-Null
if ([string]::IsNullOrWhiteSpace($diffText)) {
    $lines.Add('- No text diff snapshot captured. Binary UAsset/UMap changes must be verified in the editor and via changed file paths.') | Out-Null
} else {
    $lines.Add('```diff') | Out-Null
    $lines.Add((Limit-Text $diffText 12000)) | Out-Null
    $lines.Add('```') | Out-Null
}
$lines.Add('') | Out-Null
$lines.Add('## Future Lookup Notes') | Out-Null
$lines.Add('- Search this file first for remembered intent, then open real project files before giving exact code guidance.') | Out-Null
$lines.Add('- Do not treat this memory as source of truth over git or project files.') | Out-Null

$lines | Set-Content -LiteralPath $featurePath -Encoding UTF8

$indexPath = Join-Path $projectCache.CacheRoot 'features.tsv'
$changedFilesOneLine = (($diffNameStatus -split "`r?`n") | Where-Object { -not [string]::IsNullOrWhiteSpace($_) } | ForEach-Object { $_.Trim() }) -join '; '
if ([string]::IsNullOrWhiteSpace($changedFilesOneLine) -and -not [string]::IsNullOrWhiteSpace($commitFiles)) {
    $changedFilesOneLine = (($commitFiles -split "`r?`n") | Where-Object { -not [string]::IsNullOrWhiteSpace($_) } | ForEach-Object { $_.Trim() }) -join '; '
}
$indexLine = @(
    $featureId,
    (Get-Date).ToUniversalTime().ToString('o'),
    $Author,
    $gitHead,
    ($Title -replace "`t", ' '),
    ($featurePath -replace "`t", ' '),
    ($changedFilesOneLine -replace "`t", ' ')
) -join "`t"
Add-Content -LiteralPath $indexPath -Value $indexLine -Encoding UTF8

$memoryJsonPath = Join-Path $projectCache.CacheRoot 'feature-memory.json'
$memory = [pscustomobject]@{
    projectRoot = $projectRootFull
    projectName = $projectCache.ProjectName
    cacheKey = $projectCache.CacheKey
    cacheRoot = $projectCache.CacheRoot
    preferredAuthor = $Author
    gitUserName = $gitUserName
    gitUserEmail = $gitUserEmail
    lastFeatureId = $featureId
    lastFeaturePath = $featurePath
    updatedAtUtc = (Get-Date).ToUniversalTime().ToString('o')
}
$memory | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath $memoryJsonPath -Encoding UTF8

Write-Output "Wrote Oasis feature memory:"
Write-Output "  $featurePath"
Write-Output "  $indexPath"
Write-Output "  $memoryJsonPath"
