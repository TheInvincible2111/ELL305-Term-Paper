$ErrorActionPreference = 'Stop'

$projectRoot = Split-Path -Parent $PSScriptRoot
$submissionRoot = Join-Path $projectRoot 'submissions'
$packageDir = Join-Path $submissionRoot 'Draft-1'
$zipPath = Join-Path $submissionRoot 'ELL305-Draft-1-Submission.zip'

New-Item -ItemType Directory -Force -Path $packageDir | Out-Null

function Read-ProjectFile {
    param([Parameter(Mandatory = $true)][string]$RelativePath)
    return Get-Content -Raw -LiteralPath (Join-Path $projectRoot $RelativePath)
}

function Add-SourceBoundary {
    param(
        [Parameter(Mandatory = $true)][string]$Label,
        [Parameter(Mandatory = $true)][string]$Content
    )
    return "% ==================== $Label ====================`r`n$Content"
}

$format = Read-ProjectFile 'paper\styles\ell305-format.tex'
$format = $format.Replace(
    '\addbibresource{../references/references.bib}',
    '\addbibresource{references.bib}'
)

$frontMatter = Read-ProjectFile 'Draft 1\front-matter.tex'
$frontMatter = $frontMatter.Replace(
    '{assets/iit-delhi-logo.png}',
    '{iit-delhi-logo.png}'
)

$mappingFigure = Read-ProjectFile 'Draft 1\figures\textbook-topic-map.tex'
$mappingSection = Read-ProjectFile 'Draft 1\sections\02-textbook-mapping.tex'
$mappingSection = $mappingSection.Replace(
    '\input{"../Draft 1/figures/textbook-topic-map.tex"}',
    $mappingFigure.TrimEnd()
)

$ganttFigure = Read-ProjectFile 'Draft 1\figures\gantt-chart.tex'
$scheduleSection = Read-ProjectFile 'Draft 1\sections\06-semester-schedule.tex'
$scheduleSection = $scheduleSection.Replace(
    '\input{"../Draft 1/figures/gantt-chart.tex"}',
    $ganttFigure.TrimEnd()
)

$parts = @(
    '\documentclass[12pt,a4paper,twoside]{article}',
    '',
    '% Consolidated submission source generated from the modular Draft 1 project.',
    '% Edit the modular project files for future revisions; regenerate this file for submission.',
    (Add-SourceBoundary 'SHARED FORMAT' $format.TrimEnd()),
    (Add-SourceBoundary 'DRAFT 1 PREAMBLE' (Read-ProjectFile 'Draft 1\preamble.tex').TrimEnd()),
    (Add-SourceBoundary 'DRAFT 1 METADATA' (Read-ProjectFile 'Draft 1\metadata.tex').TrimEnd()),
    '',
    '\begin{document}',
    (Add-SourceBoundary 'FRONT MATTER' $frontMatter.TrimEnd()),
    (Add-SourceBoundary 'WORK DONE HEADING' (Read-ProjectFile 'Draft 1\sections\00-work-done.tex').TrimEnd()),
    (Add-SourceBoundary 'TOPIC AND SCOPE' (Read-ProjectFile 'Draft 1\sections\01-topic-and-scope.tex').TrimEnd()),
    (Add-SourceBoundary 'TEXTBOOK MAPPING' $mappingSection.TrimEnd()),
    (Add-SourceBoundary 'PRELIMINARY SURVEY' (Read-ProjectFile 'Draft 1\sections\03-preliminary-survey.tex').TrimEnd()),
    (Add-SourceBoundary 'RESEARCH DIRECTIONS' (Read-ProjectFile 'Draft 1\sections\04-research-directions.tex').TrimEnd()),
    (Add-SourceBoundary 'WORK PACKAGES' (Read-ProjectFile 'Draft 1\sections\05-work-packages.tex').TrimEnd()),
    (Add-SourceBoundary 'SEMESTER SCHEDULE' $scheduleSection.TrimEnd()),
    (Add-SourceBoundary 'SOURCES' (Read-ProjectFile 'Draft 1\sections\07-sources.tex').TrimEnd()),
    (Add-SourceBoundary 'NEXT STEPS' (Read-ProjectFile 'Draft 1\sections\08-next-steps.tex').TrimEnd()),
    '\end{document}',
    ''
)

$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
$combinedTex = [string]::Join("`r`n`r`n", $parts).TrimEnd() + "`r`n"
$texPath = Join-Path $packageDir 'ELL305-Draft-1.tex'
[System.IO.File]::WriteAllText($texPath, $combinedTex, $utf8NoBom)

Copy-Item -LiteralPath (Join-Path $projectRoot 'references\references.bib') `
    -Destination (Join-Path $packageDir 'references.bib') -Force
Copy-Item -LiteralPath (Join-Path $projectRoot 'paper\assets\iit-delhi-logo.png') `
    -Destination (Join-Path $packageDir 'iit-delhi-logo.png') -Force
Copy-Item -LiteralPath (Join-Path $projectRoot 'build\pdf\ELL305-Draft-1.pdf') `
    -Destination (Join-Path $packageDir 'ELL305-Draft-1.pdf') -Force

$readme = @'
ELL305 Draft 1 submission package
=================================

Submit-ready file:
- ELL305-Draft-1.pdf

Reproducible source:
- ELL305-Draft-1.tex      Consolidated LaTeX source (all Draft 1 modules and TikZ figures inlined)
- references.bib          Zotero/Better BibTeX bibliography export
- iit-delhi-logo.png      Only external image required by the LaTeX source

Build sequence (MiKTeX or TeX Live):
1. pdflatex ELL305-Draft-1.tex
2. biber ELL305-Draft-1
3. pdflatex ELL305-Draft-1.tex
4. pdflatex ELL305-Draft-1.tex

Research PDFs, Obsidian notes, source templates, SVG originals, and generated auxiliary files are intentionally excluded because they are not required to compile or submit Draft 1.
'@
[System.IO.File]::WriteAllText(
    (Join-Path $packageDir 'README.txt'),
    $readme.TrimStart(),
    $utf8NoBom
)

if (Test-Path -LiteralPath $zipPath) {
    Remove-Item -LiteralPath $zipPath -Force
}
Compress-Archive -Path (Join-Path $packageDir '*') -DestinationPath $zipPath -CompressionLevel Optimal

Write-Host "Created $texPath"
Write-Host "Created $zipPath"
