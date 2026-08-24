$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $projectRoot

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

if (-not (Get-Command pdflatex -ErrorAction SilentlyContinue)) {
    throw 'pdflatex was not found. Install MiKTeX or TeX Live, then try again.'
}

foreach ($requiredTool in 'biber', 'makeindex') {
    if (-not (Get-Command $requiredTool -ErrorAction SilentlyContinue)) {
        throw "$requiredTool was not found. Install it through MiKTeX or TeX Live, then try again."
    }
}

# MiKTeX may install font packages on demand during an earlier build. Refreshing
# its font maps here prevents the next PDF pass from seeing unregistered fonts.
if (Get-Command miktex -ErrorAction SilentlyContinue) {
    & miktex fontmaps configure
    if ($LASTEXITCODE -ne 0) { throw "MiKTeX font-map configuration failed with exit code $LASTEXITCODE." }
}

New-Item -ItemType Directory -Force -Path 'build\aux\chapters', 'build\pdf' | Out-Null
Set-Location (Join-Path $projectRoot 'paper')

$canUseLatexmk = (Get-Command latexmk -ErrorAction SilentlyContinue) -and (Get-Command perl -ErrorAction SilentlyContinue)

function Update-GeneratedReportApparatus {
    $auxPath = Join-Path $projectRoot 'build\aux'
    $makeindexExe = (Get-Command makeindex).Source
    $glossaryProcess = Start-Process -FilePath $makeindexExe `
        -ArgumentList @('-s', 'main.ist', '-t', 'main.glg', '-o', 'main.gls', 'main.glo') `
        -WorkingDirectory $auxPath -Wait -PassThru -WindowStyle Hidden
    if ($glossaryProcess.ExitCode -ne 0) { throw "Glossary generation failed with exit code $($glossaryProcess.ExitCode)." }

    $indexProcess = Start-Process -FilePath $makeindexExe `
        -ArgumentList @('main.idx', '-o', 'main.ind') `
        -WorkingDirectory $auxPath -Wait -PassThru -WindowStyle Hidden
    if ($indexProcess.ExitCode -ne 0) { throw "makeindex failed with exit code $($indexProcess.ExitCode)." }
}

if ($canUseLatexmk) {
    latexmk -r ..\.latexmkrc main.tex
    if ($LASTEXITCODE -ne 0) { throw "latexmk failed with exit code $LASTEXITCODE." }

    Update-GeneratedReportApparatus

    latexmk -r ..\.latexmkrc main.tex
    if ($LASTEXITCODE -ne 0) { throw "latexmk failed after generating the glossary and index with exit code $LASTEXITCODE." }
    Copy-Item -LiteralPath '../build/aux/main.pdf' -Destination '../build/pdf/ELL305-Draft-1.pdf' -Force
} else {
    $latexArgs = @('-interaction=nonstopmode', '-file-line-error', '-synctex=1', '-output-directory=../build/aux', 'main.tex')
    & pdflatex @latexArgs
    if ($LASTEXITCODE -ne 0) { throw "The first pdflatex pass failed with exit code $LASTEXITCODE." }

    & biber --input-directory ../build/aux --output-directory ../build/aux main
    if ($LASTEXITCODE -ne 0) { throw "biber failed with exit code $LASTEXITCODE." }

    Update-GeneratedReportApparatus

    & pdflatex @latexArgs
    if ($LASTEXITCODE -ne 0) { throw "The second pdflatex pass failed with exit code $LASTEXITCODE." }
    & pdflatex @latexArgs
    if ($LASTEXITCODE -ne 0) { throw "The final pdflatex pass failed with exit code $LASTEXITCODE." }

    Copy-Item -LiteralPath '../build/aux/main.pdf' -Destination '../build/pdf/ELL305-Draft-1.pdf' -Force
}

$output = Join-Path $projectRoot 'build\pdf\ELL305-Draft-1.pdf'
if (-not (Test-Path $output)) { throw "Build completed but expected output was not found: $output" }
Write-Host "Built $output"
