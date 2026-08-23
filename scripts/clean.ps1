$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $projectRoot

Get-ChildItem -LiteralPath 'build\aux' -Force -ErrorAction SilentlyContinue | Remove-Item -Force -Recurse
Write-Host 'Removed temporary LaTeX build files. The finished PDF was retained.'
