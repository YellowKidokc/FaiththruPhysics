# Copy NotebookLM studio snapshots to the desktop share.
# Run from this folder on a Windows machine on your LAN.

$Source = $PSScriptRoot
$Dest   = '\\192.168.2.50\h_hp\Desktop\Notebook LM'

if (-not (Test-Path $Dest)) {
    New-Item -ItemType Directory -Path $Dest -Force | Out-Null
    Write-Host "Created: $Dest"
}

$items = @(
    (Join-Path $Source 'mda'),
    (Join-Path $Source 'one-page-stories'),
    (Join-Path $Source 'notebooklm-output-audit-2026-06-22.md'),
    (Join-Path $Source 'README.md')
)

foreach ($item in $items) {
    if (-not (Test-Path $item)) {
        Write-Warning "Missing: $item"
        continue
    }
    $name = Split-Path $item -Leaf
    $target = Join-Path $Dest $name
    if (Test-Path $item -PathType Container) {
        Copy-Item -Path $item -Destination $target -Recurse -Force
    } else {
        Copy-Item -Path $item -Destination $target -Force
    }
    Write-Host "Copied: $name -> $Dest"
}

Write-Host ""
Write-Host "Done. Files are in: $Dest"
Get-ChildItem -Path $Dest -Recurse -File | Select-Object FullName, Length, LastWriteTime
