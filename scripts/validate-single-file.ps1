$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
$validationRoot = Join-Path $projectRoot 'build\single-file-validation'
$validationAux = Join-Path $validationRoot 'aux'
$baseName = 'ELL305-Draft-1'
$embeddedBibliography = Join-Path $validationRoot "$baseName-references.bib"

$miktexCandidates = @(
    'C:\Program Files\MiKTeX-25.12\miktex\bin\x64',
    'C:\Program Files\MiKTeX\miktex\bin\x64',
    (Join-Path $env:LOCALAPPDATA 'Programs\MiKTeX\miktex\bin\x64')
)

if (-not (Get-Command pdflatex -ErrorAction SilentlyContinue)) {
    $miktexBin = $miktexCandidates | Where-Object { Test-Path (Join-Path $_ 'pdflatex.exe') } | Select-Object -First 1
    if ($miktexBin) {
        $env:Path = "$miktexBin;$env:Path"
    }
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

New-Item -ItemType Directory -Force -Path $validationAux | Out-Null
$resolvedProjectRoot = [IO.Path]::GetFullPath($projectRoot)
$resolvedValidationRoot = [IO.Path]::GetFullPath($validationRoot)
$resolvedValidationAux = [IO.Path]::GetFullPath($validationAux)
if (-not $resolvedValidationAux.StartsWith($resolvedProjectRoot + [IO.Path]::DirectorySeparatorChar, [StringComparison]::OrdinalIgnoreCase)) {
    throw 'The validation auxiliary directory resolved outside the project workspace.'
}
if (Test-Path -LiteralPath $embeddedBibliography) {
    $resolvedEmbeddedBibliography = [IO.Path]::GetFullPath($embeddedBibliography)
    if (-not $resolvedEmbeddedBibliography.StartsWith($resolvedValidationRoot + [IO.Path]::DirectorySeparatorChar, [StringComparison]::OrdinalIgnoreCase)) {
        throw 'The generated bibliography resolved outside the validation workspace.'
    }
    Remove-Item -LiteralPath $resolvedEmbeddedBibliography -Force
}

& (Join-Path $PSScriptRoot 'package-draft1.ps1') -ValidationOnly

Get-ChildItem -LiteralPath $validationAux -Force -ErrorAction SilentlyContinue | Remove-Item -Force -Recurse

Push-Location $validationRoot
try {
    $latexArgs = @(
        '-interaction=nonstopmode',
        '-file-line-error',
        '-output-directory=aux',
        "$baseName.tex"
    )

    & pdflatex @latexArgs
    if ($LASTEXITCODE -ne 0) { throw "The first consolidated pdflatex pass failed with exit code $LASTEXITCODE." }

    & biber --input-directory aux --output-directory aux $baseName
    if ($LASTEXITCODE -ne 0) { throw "The consolidated biber pass failed with exit code $LASTEXITCODE." }

    $makeindexExe = (Get-Command makeindex).Source
    $glossaryProcess = Start-Process -FilePath $makeindexExe `
        -ArgumentList @('-s', "$baseName.ist", '-t', "$baseName.glg", '-o', "$baseName.gls", "$baseName.glo") `
        -WorkingDirectory $validationAux -Wait -PassThru -WindowStyle Hidden
    if ($glossaryProcess.ExitCode -ne 0) { throw "Consolidated glossary generation failed with exit code $($glossaryProcess.ExitCode)." }

    $indexProcess = Start-Process -FilePath $makeindexExe `
        -ArgumentList @("$baseName.idx", '-o', "$baseName.ind") `
        -WorkingDirectory $validationAux -Wait -PassThru -WindowStyle Hidden
    if ($indexProcess.ExitCode -ne 0) { throw "Consolidated index generation failed with exit code $($indexProcess.ExitCode)." }

    & pdflatex @latexArgs
    if ($LASTEXITCODE -ne 0) { throw "The second consolidated pdflatex pass failed with exit code $LASTEXITCODE." }
    & pdflatex @latexArgs
    if ($LASTEXITCODE -ne 0) { throw "The final consolidated pdflatex pass failed with exit code $LASTEXITCODE." }

    Copy-Item -LiteralPath (Join-Path $validationAux "$baseName.pdf") `
        -Destination (Join-Path $validationRoot "$baseName-single-file-validation.pdf") -Force
}
finally {
    Pop-Location
}

Write-Host "Validated consolidated source at $(Join-Path $validationRoot "$baseName.tex")"
Write-Host "Built validation PDF at $(Join-Path $validationRoot "$baseName-single-file-validation.pdf")"
Write-Host 'No submission ZIP was created or modified.'
