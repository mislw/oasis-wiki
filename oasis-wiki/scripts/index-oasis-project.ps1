param(
    [string] $ProjectRoot = (Get-Location).Path,

    [string] $OutputRoot = '',

    [switch] $Force,

    [int] $MaxSnippetLength = 220
)

$ErrorActionPreference = 'Stop'

function Resolve-FullPath {
    param([Parameter(Mandatory = $true)][string] $Path)
    $resolved = Resolve-Path -LiteralPath $Path -ErrorAction Stop
    return $resolved.ProviderPath
}

function Convert-ToRelativePath {
    param(
        [Parameter(Mandatory = $true)][string] $Root,
        [Parameter(Mandatory = $true)][string] $Path
    )

    $rootFull = [System.IO.Path]::GetFullPath($Root).TrimEnd([System.IO.Path]::DirectorySeparatorChar, [System.IO.Path]::AltDirectorySeparatorChar)
    $pathFull = [System.IO.Path]::GetFullPath($Path)
    $rootUri = New-Object System.Uri(($rootFull + [System.IO.Path]::DirectorySeparatorChar))
    $pathUri = New-Object System.Uri($pathFull)
    return [System.Uri]::UnescapeDataString($rootUri.MakeRelativeUri($pathUri).ToString()).Replace('/', [System.IO.Path]::DirectorySeparatorChar)
}

function Escape-Tsv {
    param([AllowNull()][string] $Value)
    if ($null -eq $Value) { return '' }
    return ($Value -replace "`t", ' ' -replace "`r?`n", ' ').Trim()
}

function Shorten-Snippet {
    param([AllowNull()][string] $Text)
    if ($null -eq $Text) { return '' }
    $clean = ($Text -replace "`t", ' ' -replace "`r?`n", ' ').Trim()
    if ($clean.Length -le $MaxSnippetLength) { return $clean }
    return $clean.Substring(0, [Math]::Max(0, $MaxSnippetLength - 3)) + '...'
}

function Add-Symbol {
    param(
        [System.Collections.Generic.List[object]] $Symbols,
        [Parameter(Mandatory = $true)][string] $Kind,
        [Parameter(Mandatory = $true)][string] $Name,
        [Parameter(Mandatory = $true)][string] $File,
        [Parameter(Mandatory = $true)][int] $Line,
        [AllowNull()][string] $Snippet
    )

    $Symbols.Add([pscustomobject]@{
        Kind = $Kind
        Name = $Name
        File = $File
        Line = $Line
        Snippet = (Shorten-Snippet $Snippet)
    }) | Out-Null
}

function Get-Sha256 {
    param([Parameter(Mandatory = $true)][string] $Path)
    return (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant()
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

$projectRootFull = Resolve-FullPath $ProjectRoot
$projectCache = Get-ProjectCacheRoot $projectRootFull
if ([string]::IsNullOrWhiteSpace($OutputRoot)) {
    $OutputRoot = Join-Path $projectCache.CacheRoot 'index'
}

$outputRootFull = $OutputRoot
if (-not [System.IO.Path]::IsPathRooted($outputRootFull)) {
    $outputRootFull = Join-Path $projectCache.CacheRoot $outputRootFull
}
$outputRootFull = [System.IO.Path]::GetFullPath($outputRootFull)

$allowedExtensions = @('.lua', '.json', '.csv', '.ini', '.txt', '.md', '.uasset', '.umap')
$textExtensions = @('.lua', '.json', '.csv', '.ini', '.txt', '.md')
$skipDirNames = @('.git', '.codex', 'Saved', 'Intermediate', 'DerivedDataCache', 'Binaries', 'Build', 'Logs', 'Backup')

if ((Test-Path -LiteralPath $outputRootFull) -and -not $Force) {
    throw "Output already exists. Use -Force to refresh: $outputRootFull"
}

New-Item -ItemType Directory -Path $outputRootFull -Force | Out-Null

$allFiles = Get-ChildItem -LiteralPath $projectRootFull -Recurse -File -Force |
    Where-Object {
        $relative = Convert-ToRelativePath -Root $projectRootFull -Path $_.FullName
        $parts = $relative -split '[\\/]'
        -not ($parts | Where-Object { $skipDirNames -contains $_ }) -and
        ($allowedExtensions -contains $_.Extension.ToLowerInvariant())
    } |
    Sort-Object FullName

$fileRows = New-Object System.Collections.Generic.List[object]
$symbols = New-Object System.Collections.Generic.List[object]
$apiCounts = @{}
$luaFiles = @()
$uiHints = New-Object System.Collections.Generic.List[string]

$apiPatterns = @(
    'UGCGameSystem',
    'UGCEventSystem',
    'UGCTimerTools',
    'UGCBackPackSystem',
    'UGCTeamSystem',
    'UnrealNetwork',
    'RepLazyProperty',
    'ForceNetUpdate',
    'GetAvailableServerRPCs',
    'CallUnrealRPC',
    'LuaQuickFireEvent',
    'UIManager',
    'AddToViewport',
    'UserWidget',
    'UE.LoadClass',
    'UE.LoadObject',
    'GameplayStatics',
    'EventDefine',
    'ugcprint'
)

foreach ($file in $allFiles) {
    $relative = Convert-ToRelativePath -Root $projectRootFull -Path $file.FullName
    $isTextFile = $textExtensions -contains $file.Extension.ToLowerInvariant()
    $hash = if ($isTextFile) { Get-Sha256 $file.FullName } else { '' }
    $fileRows.Add([pscustomobject]@{
        Path = $relative
        Extension = $file.Extension.ToLowerInvariant()
        Size = $file.Length
        LastWriteTime = $file.LastWriteTimeUtc.ToString('o')
        Hash = $hash
    }) | Out-Null

    if ($file.Extension.ToLowerInvariant() -eq '.lua') {
        $luaFiles += $file
    }

    if ($file.FullName -match '(?i)(UI|Widget|UMG|HUD)' -or $relative -match '(?i)(UI|Widget|UMG|HUD)') {
        $uiHints.Add($relative) | Out-Null
    }

    if (-not $isTextFile) {
        continue
    }

    $lines = Get-Content -LiteralPath $file.FullName -ErrorAction Stop
    for ($i = 0; $i -lt $lines.Count; $i++) {
        $line = [string]$lines[$i]
        $lineNumber = $i + 1

        foreach ($api in $apiPatterns) {
            if ($line -match [regex]::Escape($api)) {
                if (-not $apiCounts.ContainsKey($api)) { $apiCounts[$api] = 0 }
                $apiCounts[$api] += 1
            }
        }

        if ($file.Extension.ToLowerInvariant() -ne '.lua') {
            continue
        }

        if ($line -match '^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*Script\.Class') {
            Add-Symbol $symbols 'class' $Matches[1] $relative $lineNumber $line
        } elseif ($line -match '^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*Class\s*\(') {
            Add-Symbol $symbols 'class' $Matches[1] $relative $lineNumber $line
        } elseif ($line -match '^\s*function\s+([A-Za-z_][A-Za-z0-9_]*[:\.][A-Za-z_][A-Za-z0-9_]*)\s*\(') {
            $name = $Matches[1]
            Add-Symbol $symbols 'function' $name $relative $lineNumber $line
            if ($name -match 'ServerRPC|ClientRPC|MulticastRPC|RPC_') {
                Add-Symbol $symbols 'rpc' $name $relative $lineNumber $line
            }
        } elseif ($line -match '^\s*([A-Za-z_][A-Za-z0-9_]*[:\.][A-Za-z_][A-Za-z0-9_]*)\s*=\s*function\s*\(') {
            $name = $Matches[1]
            Add-Symbol $symbols 'function' $name $relative $lineNumber $line
            if ($name -match 'ServerRPC|ClientRPC|MulticastRPC|RPC_') {
                Add-Symbol $symbols 'rpc' $name $relative $lineNumber $line
            }
        }

        if ($line -match 'GetAvailableServerRPCs|ServerRPC_|ClientRPC_|CallUnrealRPC|LuaQuickFireEvent') {
            Add-Symbol $symbols 'rpc-usage' 'rpc-registration-or-call' $relative $lineNumber $line
        }
        if ($line -match 'UGCEventSystem:(AddListener|SendEvent|RemoveListener)|EventDefine\.|LuaQuickFireEvent') {
            Add-Symbol $symbols 'event' 'event-usage' $relative $lineNumber $line
        }
        if ($line -match 'UGCTimerTools|SetTimer|K2_SetTimer|Timer') {
            Add-Symbol $symbols 'timer' 'timer-usage' $relative $lineNumber $line
        }
        if ($line -match 'RepLazyProperty|ForceNetUpdate|DOREPLIFETIME|Replicated') {
            Add-Symbol $symbols 'replication' 'replication-usage' $relative $lineNumber $line
        }
        if ($line -match 'UIManager|UserWidget|AddToViewport|RemoveFromParent|Widget') {
            Add-Symbol $symbols 'ui' 'ui-usage' $relative $lineNumber $line
        }
        if ($line -match 'require\s*[\( ]\s*["'']([^"'']+)["'']') {
            Add-Symbol $symbols 'require' $Matches[1] $relative $lineNumber $line
        }
    }
}

$filesTsvPath = Join-Path $outputRootFull 'files.tsv'
$symbolsTsvPath = Join-Path $outputRootFull 'symbols.tsv'
$summaryPath = Join-Path $outputRootFull 'summary.md'
$manifestPath = Join-Path $outputRootFull 'manifest.json'

$fileRows |
    ForEach-Object { "$(Escape-Tsv $_.Path)`t$(Escape-Tsv $_.Extension)`t$($_.Size)`t$(Escape-Tsv $_.LastWriteTime)`t$(Escape-Tsv $_.Hash)" } |
    Set-Content -LiteralPath $filesTsvPath -Encoding UTF8

$symbols |
    Sort-Object File, Line, Kind, Name |
    ForEach-Object { "$(Escape-Tsv $_.Kind)`t$(Escape-Tsv $_.Name)`t$(Escape-Tsv $_.File)`t$($_.Line)`t$(Escape-Tsv $_.Snippet)" } |
    Set-Content -LiteralPath $symbolsTsvPath -Encoding UTF8

$topApis = $apiCounts.GetEnumerator() | Sort-Object Value -Descending | Select-Object -First 20
$importantFiles = $fileRows |
    Where-Object { $_.Path -match '(?i)(UGCGameMode|UGCGameState|UGCPlayerController|UGCPlayerState|UGCPlayerPawn|GlobalConfig|EventDefine|UIManager|GameConfig)' } |
    Select-Object -First 40

$summaryLines = New-Object System.Collections.Generic.List[string]
$summaryLines.Add('# Oasis Project Index') | Out-Null
$summaryLines.Add('') | Out-Null
$summaryLines.Add(('- Project root: `' + $projectRootFull + '`')) | Out-Null
$summaryLines.Add(('- Local cache root: `' + $projectCache.CacheRoot + '`')) | Out-Null
$summaryLines.Add(('- Cache key: `' + $projectCache.CacheKey + '`')) | Out-Null
$summaryLines.Add("- Generated at UTC: $((Get-Date).ToUniversalTime().ToString('o'))") | Out-Null
$summaryLines.Add("- Indexed files: $($fileRows.Count)") | Out-Null
$summaryLines.Add("- Lua files: $($luaFiles.Count)") | Out-Null
$summaryLines.Add("- Symbols: $($symbols.Count)") | Out-Null
$summaryLines.Add('') | Out-Null
$summaryLines.Add('## High-Signal Files') | Out-Null
if ($importantFiles.Count -eq 0) {
    $summaryLines.Add('- No standard high-signal files matched by name. Search files.tsv before broad scans.') | Out-Null
} else {
    foreach ($row in $importantFiles) {
        $summaryLines.Add(('- `' + $row.Path + '`')) | Out-Null
    }
}
$summaryLines.Add('') | Out-Null
$summaryLines.Add('## Frequent APIs') | Out-Null
if ($topApis.Count -eq 0) {
    $summaryLines.Add('- No tracked Oasis API names found in indexed text files.') | Out-Null
} else {
    foreach ($api in $topApis) {
        $summaryLines.Add(('- `' + $api.Key + '`: ' + $api.Value)) | Out-Null
    }
}
$summaryLines.Add('') | Out-Null
$summaryLines.Add('## UI Hints') | Out-Null
if ($uiHints.Count -eq 0) {
    $summaryLines.Add('- No UI-like file paths matched by name.') | Out-Null
} else {
    foreach ($hint in ($uiHints | Select-Object -Unique | Select-Object -First 40)) {
        $summaryLines.Add(('- `' + $hint + '`')) | Out-Null
    }
}
$summaryLines.Add('') | Out-Null
$summaryLines.Add('## Search Next') | Out-Null
$summaryLines.Add('') | Out-Null
$summaryLines.Add('```powershell') | Out-Null
$summaryLines.Add(('rg --line-number --smart-case "ServerRPC|UIManager|EventDefine|RepLazyProperty" "' + $outputRootFull + '"')) | Out-Null
$summaryLines.Add('```') | Out-Null
$summaryLines.Add('') | Out-Null
$summaryLines.Add('Use this cache to locate likely files, then open real source files before giving exact edit guidance.') | Out-Null

$summaryLines | Set-Content -LiteralPath $summaryPath -Encoding UTF8

$manifest = [pscustomobject]@{
    projectRoot = $projectRootFull
    projectName = $projectCache.ProjectName
    cacheKey = $projectCache.CacheKey
    cacheRoot = $projectCache.CacheRoot
    outputRoot = $outputRootFull
    generatedAtUtc = (Get-Date).ToUniversalTime().ToString('o')
    indexedExtensions = $allowedExtensions
    textExtensions = $textExtensions
    skippedDirectories = $skipDirNames
    fileCount = $fileRows.Count
    luaFileCount = $luaFiles.Count
    symbolCount = $symbols.Count
    files = $fileRows
}

$manifest | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath $manifestPath -Encoding UTF8

Write-Output "Wrote Oasis project index:"
Write-Output "  $summaryPath"
Write-Output "  $symbolsTsvPath"
Write-Output "  $filesTsvPath"
Write-Output "  $manifestPath"
