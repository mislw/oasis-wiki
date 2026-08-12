param(
    [string]$SkillPath = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
)

$ErrorActionPreference = 'Stop'

$root = Resolve-Path -LiteralPath $SkillPath

$allowedDirs = @(
    'agents',
    'assets',
    'references',
    'scripts',
    'tests'
)

$allowedFiles = @(
    '.gitattributes',
    '.gitignore',
    '.skill-version',
    'AGENTS.md',
    'LICENSE',
    'LICENSE.md',
    'license.txt',
    'SKILL.md',
    'VERSION'
)

$ignoredNames = @(
    '.git',
    '.DS_Store',
    '__pycache__'
)

$entries = Get-ChildItem -LiteralPath $root -Force
$unexpected = New-Object System.Collections.Generic.List[string]
$markdownClutter = New-Object System.Collections.Generic.List[string]

foreach ($entry in $entries) {
    if ($ignoredNames -contains $entry.Name) {
        continue
    }

    if ($entry.PSIsContainer) {
        if ($allowedDirs -notcontains $entry.Name) {
            $unexpected.Add("$($entry.Name)/")
        }
        continue
    }

    if ($allowedFiles -notcontains $entry.Name) {
        $unexpected.Add($entry.Name)
    }

    if ($entry.Extension -ieq '.md' -and @('SKILL.md', 'AGENTS.md') -notcontains $entry.Name) {
        $markdownClutter.Add($entry.Name)
    }
}

if ($markdownClutter.Count -gt 0) {
    Write-Error ("Extraneous top-level Markdown file(s): {0}. Keep core instructions in SKILL.md/AGENTS.md; put necessary supporting docs under references/." -f ($markdownClutter -join ', '))
}

if ($unexpected.Count -gt 0) {
    $allowed = @($allowedFiles + ($allowedDirs | ForEach-Object { "$_/" })) | Sort-Object
    Write-Error ("Unexpected top-level skill file(s): {0}. Allowed top-level entries are: {1}" -f ($unexpected -join ', '), ($allowed -join ', '))
}

Write-Output "Skill folder hygiene is clean."
