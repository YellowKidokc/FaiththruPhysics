param(
  [Parameter(Mandatory = $true)]
  [string]$SeriesRoot
)

$ErrorActionPreference = "Stop"

$seriesPath = (Resolve-Path -LiteralPath $SeriesRoot).Path
$seriesName = Split-Path -Leaf $seriesPath
$repoRoot = "D:\GitHub\faiththruphysics-site"
$outputDir = Join-Path $repoRoot ("reports\" + $seriesName + "-math")
$scriptPath = Join-Path $PSScriptRoot "extract_series_math.py"

Write-Host "Series root: $seriesPath"
Write-Host "Output dir : $outputDir"

python $scriptPath --series-root $seriesPath --output-dir $outputDir

Write-Host ""
Write-Host "Done."
Write-Host "Summary: $(Join-Path $outputDir 'series_math_summary.md')"
