$ErrorActionPreference = 'Stop'

$projectRoot = Split-Path -Parent $PSScriptRoot
$zipPath = Join-Path $projectRoot 'submissions\ELL305-Draft-1-Submission.zip'
$validationRoot = Join-Path $projectRoot 'build\submission-validation'
$extractedRoot = Join-Path $validationRoot 'extracted'
$auxRoot = Join-Path $validationRoot 'aux'
$baseName = 'ELL305-Draft-1'

if (-not (Test-Path -LiteralPath $zipPath)) {
    throw "Submission ZIP was not found: $zipPath"
}

$resolvedProjectRoot = [IO.Path]::GetFullPath($projectRoot)
$resolvedValidationRoot = [IO.Path]::GetFullPath($validationRoot)
if (-not $resolvedValidationRoot.StartsWith($resolvedProjectRoot + [IO.Path]::DirectorySeparatorChar, [StringComparison]::OrdinalIgnoreCase)) {
    throw 'The submission-validation directory resolved outside the project workspace.'
}

if (Test-Path -LiteralPath $validationRoot) {
    Remove-Item -LiteralPath $validationRoot -Recurse -Force
}
New-Item -ItemType Directory -Force -Path $extractedRoot, $auxRoot | Out-Null
Expand-Archive -LiteralPath $zipPath -DestinationPath $extractedRoot -Force

$expectedFiles = @(
    'ELL305-Draft-1.pdf',
    'ELL305-Draft-1.tex',
    'iit-delhi-logo.png',
    'grammarly-plagiarism-report-2026-08-24.png',
    'readability-indices-2026-08-24.png',
    'README.txt'
)
$actualFiles = Get-ChildItem -LiteralPath $extractedRoot -File | Select-Object -ExpandProperty Name
$missingFiles = $expectedFiles | Where-Object { $_ -notin $actualFiles }
$unexpectedFiles = $actualFiles | Where-Object { $_ -notin $expectedFiles }
if ($missingFiles) { throw "Submission ZIP is missing: $($missingFiles -join ', ')" }
if ($unexpectedFiles) { throw "Submission ZIP has unexpected files: $($unexpectedFiles -join ', ')" }

$texPath = Join-Path $extractedRoot "$baseName.tex"
$texSource = Get-Content -LiteralPath $texPath -Raw
if ($texSource -match '(?m)^[^%]*\\(input|include)\b') {
    throw 'The submission source still contains an external LaTeX input/include command.'
}
if ($texSource -notmatch '\\begin\{filecontents\*\}\{ELL305-Draft-1-references\.bib\}') {
    throw 'The submission source does not contain the embedded Zotero bibliography.'
}

$miktexCandidates = @(
    'C:\Program Files\MiKTeX-25.12\miktex\bin\x64',
    'C:\Program Files\MiKTeX\miktex\bin\x64',
    (Join-Path $env:LOCALAPPDATA 'Programs\MiKTeX\miktex\bin\x64')
)
if (-not (Get-Command pdflatex -ErrorAction SilentlyContinue)) {
    $miktexBin = $miktexCandidates | Where-Object { Test-Path (Join-Path $_ 'pdflatex.exe') } | Select-Object -First 1
    if ($miktexBin) { $env:Path = "$miktexBin;$env:Path" }
}
foreach ($requiredTool in 'pdflatex', 'biber', 'makeindex') {
    if (-not (Get-Command $requiredTool -ErrorAction SilentlyContinue)) {
        throw "$requiredTool was not found. Install it through MiKTeX or TeX Live, then try again."
    }
}

if (Get-Command miktex -ErrorAction SilentlyContinue) {
    & miktex fontmaps configure
    if ($LASTEXITCODE -ne 0) { throw "MiKTeX font-map configuration failed with exit code $LASTEXITCODE." }
}

Push-Location $extractedRoot
try {
    $latexArgs = @(
        '-interaction=nonstopmode',
        '-file-line-error',
        "-output-directory=$auxRoot",
        "$baseName.tex"
    )

    & pdflatex @latexArgs
    if ($LASTEXITCODE -ne 0) { throw "The first packaged pdflatex pass failed with exit code $LASTEXITCODE." }

    & biber --input-directory $auxRoot --output-directory $auxRoot $baseName
    if ($LASTEXITCODE -ne 0) { throw "The packaged biber pass failed with exit code $LASTEXITCODE." }

    $makeindexExe = (Get-Command makeindex).Source
    $glossaryProcess = Start-Process -FilePath $makeindexExe `
        -ArgumentList @('-s', "$baseName.ist", '-t', "$baseName.glg", '-o', "$baseName.gls", "$baseName.glo") `
        -WorkingDirectory $auxRoot -Wait -PassThru -WindowStyle Hidden
    if ($glossaryProcess.ExitCode -ne 0) { throw "Packaged glossary generation failed with exit code $($glossaryProcess.ExitCode)." }
    $indexProcess = Start-Process -FilePath $makeindexExe `
        -ArgumentList @("$baseName.idx", '-o', "$baseName.ind") `
        -WorkingDirectory $auxRoot -Wait -PassThru -WindowStyle Hidden
    if ($indexProcess.ExitCode -ne 0) { throw "Packaged index generation failed with exit code $($indexProcess.ExitCode)." }

    & pdflatex @latexArgs
    if ($LASTEXITCODE -ne 0) { throw "The second packaged pdflatex pass failed with exit code $LASTEXITCODE." }
    & pdflatex @latexArgs
    if ($LASTEXITCODE -ne 0) { throw "The final packaged pdflatex pass failed with exit code $LASTEXITCODE." }
}
finally {
    Pop-Location
}

$logPath = Join-Path $auxRoot "$baseName.log"
$warningPattern = 'LaTeX Error|Undefined control sequence|undefined references|Citation.*undefined|Overfull|Underfull|Package .* Warning|LaTeX Warning|pdfTeX warning'
$problems = Select-String -Path $logPath -Pattern $warningPattern -CaseSensitive:$false
if ($problems) {
    throw "The packaged build log contains errors or warnings:`n$($problems.Line -join "`n")"
}

Copy-Item -LiteralPath (Join-Path $auxRoot "$baseName.pdf") `
    -Destination (Join-Path $validationRoot "$baseName-package-validation.pdf") -Force

Write-Host "Validated submission ZIP at $zipPath"
Write-Host "Built independent validation PDF at $(Join-Path $validationRoot "$baseName-package-validation.pdf")"
