$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $projectRoot

$miktexCandidates = @(
    (Join-Path $env:LOCALAPPDATA 'Programs\MiKTeX\miktex\bin\x64'),
    'C:\Program Files\MiKTeX\miktex\bin\x64'
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

New-Item -ItemType Directory -Force -Path 'build\aux\chapters', 'build\pdf' | Out-Null
Set-Location (Join-Path $projectRoot 'paper')

$canUseLatexmk = (Get-Command latexmk -ErrorAction SilentlyContinue) -and (Get-Command perl -ErrorAction SilentlyContinue)
if ($canUseLatexmk) {
    latexmk -r ..\.latexmkrc main.tex
    if ($LASTEXITCODE -ne 0) { throw "latexmk failed with exit code $LASTEXITCODE." }
} else {
    $latexArgs = @('-interaction=nonstopmode', '-file-line-error', '-synctex=1', '-output-directory=../build/aux', 'main.tex')
    & pdflatex @latexArgs
    if ($LASTEXITCODE -ne 0) { throw "The first pdflatex pass failed with exit code $LASTEXITCODE." }

    & biber --input-directory ../build/aux --output-directory ../build/aux main
    if ($LASTEXITCODE -ne 0) { throw "biber failed with exit code $LASTEXITCODE." }

    & pdflatex @latexArgs
    if ($LASTEXITCODE -ne 0) { throw "The second pdflatex pass failed with exit code $LASTEXITCODE." }
    & pdflatex @latexArgs
    if ($LASTEXITCODE -ne 0) { throw "The final pdflatex pass failed with exit code $LASTEXITCODE." }

    Copy-Item -LiteralPath '../build/aux/main.pdf' -Destination '../build/pdf/ELL305-Draft-1.pdf' -Force
}

$output = Join-Path $projectRoot 'build\pdf\ELL305-Draft-1.pdf'
if (-not (Test-Path $output)) { throw "Build completed but expected output was not found: $output" }
Write-Host "Built $output"
