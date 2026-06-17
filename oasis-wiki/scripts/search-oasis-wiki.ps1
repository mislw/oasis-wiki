param(
    [Parameter(Mandatory = $true)]
    [string] $Query,

    [int] $MaxResults = 40,

    [int] $Context = 0
)

$ErrorActionPreference = 'Stop'

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$skillRoot = Split-Path -Parent $scriptDir
$wikiRoot = Join-Path $skillRoot 'references\wiki'

if (-not (Test-Path -LiteralPath $wikiRoot)) {
    throw "Wiki root not found: $wikiRoot"
}

$rg = Get-Command rg -ErrorAction SilentlyContinue
if ($rg) {
    $args = @(
        '--line-number',
        '--smart-case',
        '--glob', '*.md'
    )
    if ($Context -gt 0) {
        $args += @('--context', [string]$Context)
    }
    $args += @($Query, $wikiRoot)
    $results = & rg @args
    $rgExit = $LASTEXITCODE
    $results | Select-Object -First $MaxResults
    if ($rgExit -eq 1 -and -not $results) {
        exit 1
    }
    exit 0
}

Get-ChildItem -LiteralPath $wikiRoot -Filter '*.md' -Recurse |
    Select-String -Pattern $Query -CaseSensitive:$false -Context $Context |
    Select-Object -First $MaxResults |
    ForEach-Object {
        "$($_.Path):$($_.LineNumber):$($_.Line)"
    }
