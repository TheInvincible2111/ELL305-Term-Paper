param(
    [switch]$ValidationOnly
)

$ErrorActionPreference = 'Stop'

$projectRoot = Split-Path -Parent $PSScriptRoot
$submissionRoot = Join-Path $projectRoot 'submissions'
$packageDir = if ($ValidationOnly) {
    Join-Path $projectRoot 'build\single-file-validation'
} else {
    Join-Path $submissionRoot 'Draft-1'
}
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
    '\addbibresource{ELL305-Draft-1-references.bib}'
)

$bibliography = Read-ProjectFile 'references\references.bib'
$embeddedBibliography = @"
\begin{filecontents*}{ELL305-Draft-1-references.bib}
$($bibliography.TrimEnd())
\end{filecontents*}
"@

$draftPreamble = Read-ProjectFile 'Draft 1\preamble.tex'
$draftPreamble = $draftPreamble.Replace(
    '\input{"../Draft 1/glossary.tex"}',
    (Read-ProjectFile 'Draft 1\glossary.tex').TrimEnd()
)

$frontMatter = Read-ProjectFile 'Draft 1\front-matter.tex'
$frontMatter = $frontMatter.Replace(
    '\input{"../Draft 1/front-matter/copyright-assignment.tex"}',
    (Read-ProjectFile 'Draft 1\front-matter\copyright-assignment.tex').TrimEnd()
)
$frontMatter = $frontMatter.Replace(
    '\input{"../Draft 1/front-matter/acknowledgements.tex"}',
    (Read-ProjectFile 'Draft 1\front-matter\acknowledgements.tex').TrimEnd()
)
$frontMatter = $frontMatter.Replace(
    '{assets/iit-delhi-logo.png}',
    '{iit-delhi-logo.png}'
)

$plagiarismAppendix = Read-ProjectFile 'Draft 1\appendices\appendix-a-plagiarism-report.tex'
$plagiarismAppendix = $plagiarismAppendix.Replace(
    '{"../Draft 1/appendices/assets/grammarly-plagiarism-report-2026-08-24.png"}',
    '{grammarly-plagiarism-report-2026-08-24.png}'
)

$readingIndicesAppendix = Read-ProjectFile 'Draft 1\appendices\appendix-b-reading-indices.tex'
$readingIndicesAppendix = $readingIndicesAppendix.Replace(
    '{"../Draft 1/appendices/assets/readability-indices-2026-08-24.png"}',
    '{readability-indices-2026-08-24.png}'
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
    (Add-SourceBoundary 'EMBEDDED ZOTERO BIBLIOGRAPHY' $embeddedBibliography.TrimEnd()),
    (Add-SourceBoundary 'SHARED FORMAT' $format.TrimEnd()),
    (Add-SourceBoundary 'DRAFT 1 PREAMBLE' $draftPreamble.TrimEnd()),
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
    (Add-SourceBoundary 'APPENDIX A - PLAGIARISM REPORT' $plagiarismAppendix.TrimEnd()),
    (Add-SourceBoundary 'APPENDIX B - READING INDICES' $readingIndicesAppendix.TrimEnd()),
    '\clearpage',
    '\phantomsection',
    '\addcontentsline{toc}{section}{Index}',
    '\setlength{\columnsep}{24pt}',
    '\printindex',
    '\end{document}',
    ''
)

$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
$combinedTex = [string]::Join("`r`n`r`n", $parts).TrimEnd() + "`r`n"
$texPath = Join-Path $packageDir 'ELL305-Draft-1.tex'
[System.IO.File]::WriteAllText($texPath, $combinedTex, $utf8NoBom)

Copy-Item -LiteralPath (Join-Path $projectRoot 'paper\assets\iit-delhi-logo.png') `
    -Destination (Join-Path $packageDir 'iit-delhi-logo.png') -Force
Copy-Item -LiteralPath (Join-Path $projectRoot 'Draft 1\appendices\assets\grammarly-plagiarism-report-2026-08-24.png') `
    -Destination (Join-Path $packageDir 'grammarly-plagiarism-report-2026-08-24.png') -Force
Copy-Item -LiteralPath (Join-Path $projectRoot 'Draft 1\appendices\assets\readability-indices-2026-08-24.png') `
    -Destination (Join-Path $packageDir 'readability-indices-2026-08-24.png') -Force

if ($ValidationOnly) {
    Write-Host "Created validation-only consolidated source at $texPath"
    Write-Host 'No submission PDF or ZIP was created or modified.'
    return
}

$legacyBibliography = Join-Path $packageDir 'references.bib'
if (Test-Path -LiteralPath $legacyBibliography) {
    Remove-Item -LiteralPath $legacyBibliography -Force
}

Copy-Item -LiteralPath (Join-Path $projectRoot 'build\pdf\ELL305-Draft-1.pdf') `
    -Destination (Join-Path $packageDir 'ELL305-Draft-1.pdf') -Force

$readme = @'
ELL305 Draft 1 submission package
=================================

Submit-ready file:
- ELL305-Draft-1.pdf

Reproducible source:
- ELL305-Draft-1.tex      Single consolidated LaTeX source. All Draft 1 modules,
                          TikZ figures, and Zotero-exported bibliography data are inlined.

Required image assets:
- iit-delhi-logo.png      Institutional image used on the cover
- grammarly-plagiarism-report-2026-08-24.png
                          Evidence image reproduced in Appendix A
- readability-indices-2026-08-24.png
                          Evidence image reproduced in Appendix B

Build sequence (MiKTeX or TeX Live):
1. pdflatex ELL305-Draft-1.tex
2. biber ELL305-Draft-1
3. makeindex -s ELL305-Draft-1.ist -t ELL305-Draft-1.glg -o ELL305-Draft-1.gls ELL305-Draft-1.glo
4. makeindex ELL305-Draft-1.idx -o ELL305-Draft-1.ind
5. pdflatex ELL305-Draft-1.tex
6. pdflatex ELL305-Draft-1.tex

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
$packageFiles = @(
    'ELL305-Draft-1.pdf',
    'ELL305-Draft-1.tex',
    'iit-delhi-logo.png',
    'grammarly-plagiarism-report-2026-08-24.png',
    'readability-indices-2026-08-24.png',
    'README.txt'
) | ForEach-Object { Join-Path $packageDir $_ }
Compress-Archive -LiteralPath $packageFiles -DestinationPath $zipPath -CompressionLevel Optimal

Write-Host "Created $texPath"
Write-Host "Created $zipPath"
