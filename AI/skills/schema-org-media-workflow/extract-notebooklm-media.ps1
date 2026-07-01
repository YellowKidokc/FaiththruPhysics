param(
    [string]$DataRoot = "D:\GitHub\faiththruphysics-site-data",
    [string]$OutputRoot = "D:\GitHub\faiththruphysics-site-data\_staging\notebooklm-media-2026-06-30",
    [string]$LedgerPath = "D:\GitHub\faiththruphysics-site-data\docs\notebooklm-media-manual-ledger-2026-06-30.md",
    [string[]]$TargetManifestFolders
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

if (-not (Test-Path $DataRoot)) {
  throw "DataRoot not found: $DataRoot"
}

$mergedPath = Join-Path $DataRoot "docs\notebooklm-manifests-merged.csv"
$defaultManifestFolders = @(
  "one-page-stories\\truth-and-pushback\\notebooklm\\irony",
  "one-page-stories\\truth-and-pushback\\notebooklm\\character-of-god-from-physics",
  "one-page-stories\\truth-and-pushback\\notebooklm\\physics-of-the-adversary",
  "one-page-stories\\truth-and-pushback\\notebooklm\\the-logos-thesis-v3",
  "one-page-stories\\truth-and-pushback\\notebooklm\\truth-and-pushback",
  "one-page-stories\\Math all\\notebooklm\\math-all",
  "one-page-stories\\Math all\\notebooklm\\convergence-series-scientific-method",
  "one-page-stories\\Math all\\notebooklm\\lean4-theophysics-corpus"
)

if (-not $TargetManifestFolders -or $TargetManifestFolders.Count -eq 0) {
  $TargetManifestFolders = $defaultManifestFolders
}

$manifestFiles = @()
foreach ($folder in $TargetManifestFolders) {
  $fullFolder = Join-Path $DataRoot $folder
  $manifest = Join-Path $fullFolder "notebooklm-manifest.json"
  if (Test-Path $manifest) {
    $manifestFiles += [pscustomobject]@{
      Folder = $folder
      Path = $manifest
    }
  }
}

if ($manifestFiles.Count -eq 0) {
  throw "No notebooklm-manifest.json files found for the provided targets."
}

if (Test-Path $OutputRoot) {
  Remove-Item -Recurse -Force $OutputRoot
}
New-Item -ItemType Directory -Path $OutputRoot | Out-Null

$merged = @{}
if (Test-Path $mergedPath) {
  foreach ($row in (Import-Csv $mergedPath)) {
    if (-not $row.Manifest -or -not $row.File) {
      continue
    }
    $m = $row.Manifest.ToLowerInvariant()
    if (-not $merged.ContainsKey($m)) {
      $merged[$m] = @{}
    }
    if (-not $merged[$m].ContainsKey($row.File)) {
      $merged[$m][$row.File] = @($row)
    } else {
      $merged[$m][$row.File] += $row
    }
  }
}

function Convert-To-CanonicalName {
  param(
    [string]$SourceFileName,
    [string]$TypeCode
  )

  $ext = [IO.Path]::GetExtension($SourceFileName)
  $base = [IO.Path]::GetFileNameWithoutExtension($SourceFileName)
  $titlePart = $base
  if ($base -match "__[A-Z]{1,3}__(.+)$") {
    $titlePart = $Matches[1]
  }
  $safeTitle = ($titlePart -replace "[^A-Za-z0-9\-_\. ]", " ")
  $safeTitle = $safeTitle -replace "\s+", " "
  $safeTitle = $safeTitle.Trim()
  if ($safeTitle.Length -gt 100) {
    $safeTitle = $safeTitle.Substring(0, 100).Trim()
  }
  if ($TypeCode) {
    return "${TypeCode}_$safeTitle$ext"
  }
  return "$base$ext"
}

function Resolve-TypeCode {
  param(
    [psobject]$MergedRow,
    [string]$RawFile,
    [string]$SourceType
  )

  $typeCode = $null
  if ($MergedRow -and $MergedRow.Type) {
    $candidate = $MergedRow.Type.Trim()
    if ($candidate) {
      $typeCode = $candidate
    }
  }
  if (-not $typeCode) {
    if ($RawFile -match "__VO__") { $typeCode = "4V_Explainer" }
    elseif ($RawFile -match "__DD__") { $typeCode = "2DS" }
    elseif ($RawFile -match "__SD__") { $typeCode = "SD" }
    elseif ($SourceType -eq "VO") { $typeCode = "4V_Explainer" }
    elseif ($SourceType -eq "DD") { $typeCode = "2DS" }
    elseif ($SourceType -eq "SD") { $typeCode = "SD" }
  }
  return $typeCode
}

function Get-SeriesScope {
  param([string]$NotebookFolder)
  if ($NotebookFolder -match "convergence-series-scientific-method|lean4-theophysics-corpus") {
    return "folder"
  }
  return "page"
}

$rows = @()

foreach ($manifest in $manifestFiles) {
    $manifestObj = Get-Content $manifest.Path -Raw | ConvertFrom-Json
    $notebookTitle = $manifestObj.title
  $allEntries = @()
  if ($manifestObj.downloads) {
    $allEntries += @($manifestObj.downloads)
  }
  if ($manifestObj.PSObject.Properties["slideDeck"] -and $manifestObj.slideDeck -and $manifestObj.slideDeck.downloads) {
    $allEntries += @($manifestObj.slideDeck.downloads)
  }

  if ($allEntries.Count -eq 0) {
    $rows += [pscustomobject]@{
      NotebookName = $notebookTitle
      Folder = $manifest.Folder
      MediaType = "unknown"
      SourceTitle = $notebookTitle
      OriginalFile = ""
      CanonicalFile = ""
      SourcePath = ""
      DestinationPath = ""
      SharedAcrossPages = if (Get-SeriesScope -NotebookFolder $manifest.Folder -eq "folder") { "yes" } else { "no" }
      Status = "blocked"
      Blocker = "No export entries were present in manifest (slides/downloads unavailable)."
    }
    continue
  }

  foreach ($entry in $allEntries) {
    $entryDest = if ($entry.PSObject.Properties["destPath"]) { $entry.destPath } else { "" }
    $rawFile = ""
    if ($entryDest) {
      $rawFile = [IO.Path]::GetFileName($entryDest)
    }

    $manifestLookup = $merged[$manifest.Path.ToLowerInvariant()]
    $mergedRows = @()
    if ($manifestLookup -and $rawFile -and $manifestLookup.ContainsKey($rawFile)) {
      $mergedRows = $manifestLookup[$rawFile] | Where-Object { $_ }
    }
    $mergedRow = if ($mergedRows.Count -gt 0) { $mergedRows[0] } else { $null }

    $entryType = if ($entry.PSObject.Properties["type"]) { $entry.type } else { "" }
    $entryDownload = if ($entry.PSObject.Properties["sourceDownload"]) { $entry.sourceDownload } else { "" }

    $typeCode = Resolve-TypeCode -MergedRow $mergedRow -RawFile $rawFile -SourceType $entryType
    if (-not $typeCode) {
      if ($entryType) { $typeCode = $entryType }
    }

    $sourceCandidate = @()
    if ($entryDownload) { $sourceCandidate += $entryDownload }
    if ($entryDest) { $sourceCandidate += $entryDest }
    if ($manifestObj.destRoot) { $sourceCandidate += (Join-Path $manifestObj.destRoot ([IO.Path]::GetFileName($entryDest)) ) }

    $sourcePath = $null
    foreach ($cand in $sourceCandidate) {
      if ([string]::IsNullOrWhiteSpace($cand)) { continue }
      if (Test-Path -LiteralPath $cand -PathType Leaf) {
        $sourcePath = $cand
        break
      }
    }

    if (-not $sourcePath -and -not [string]::IsNullOrWhiteSpace($rawFile)) {
      $folderFallback = Split-Path -Parent $manifest.Path
      $alt = Get-ChildItem -Path $folderFallback -Recurse -File -Filter $rawFile -ErrorAction SilentlyContinue | Select-Object -First 1
      if ($alt) { $sourcePath = $alt.FullName }
    }

    $blocker = ""
    $status = "blocked"
    $downloadedFile = ""
    if ($sourcePath) {
      $canonicalFile = Convert-To-CanonicalName -SourceFileName $rawFile -TypeCode $typeCode
      if (-not $canonicalFile) {
        $canonicalFile = $rawFile
      }

      $targetPath = Join-Path $OutputRoot (Join-Path $manifest.Folder $canonicalFile)
      $targetDir = Split-Path $targetPath -Parent
      if (-not (Test-Path $targetDir)) {
        New-Item -ItemType Directory -Path $targetDir -Force | Out-Null
      }

      if (-not (Test-Path $targetPath)) {
        Copy-Item -LiteralPath $sourcePath -Destination $targetPath
        $status = "downloaded"
      } else {
        $sourceSize = (Get-Item -LiteralPath $sourcePath).Length
        $destSize = (Get-Item -LiteralPath $targetPath).Length
        if ($sourceSize -ne $destSize) {
          $status = "exists(size-mismatch)"
          $blocker = "Existing staged file differs in size; not overwritten."
        } else {
          $status = "already-present"
        }
      }
      $downloadedFile = $canonicalFile
    } else {
      $status = "blocked"
      if ($entryDownload) {
        $blocker = "Source download path is not currently reachable (`"$($entryDownload)`")."
      } elseif ($entryDest) {
        $blocker = "Destination export path in manifest is not present and no local source found."
      } else {
        $blocker = "No export entry payload for this card in manifest."
      }
      $typeCode = if ($typeCode) { "$typeCode (uncertain)" } else { "uncertain" }
    }

    $scope = Get-SeriesScope -NotebookFolder $manifest.Folder
    $rows += [pscustomobject]@{
      NotebookName = $notebookTitle
      Folder = $manifest.Folder
      MediaType = $typeCode
      SourceTitle = if ($mergedRow -and $mergedRow.Card) { $mergedRow.Card } else { $manifestObj.title }
      OriginalFile = $rawFile
      CanonicalFile = if ($downloadedFile) { $downloadedFile } else { Convert-To-CanonicalName -SourceFileName $rawFile -TypeCode $typeCode }
      SourcePath = if ($sourcePath) { $sourcePath } else { if ($entryDownload) { $entryDownload } else { $entryDest } }
      DestinationPath = if ($sourcePath) { Join-Path $OutputRoot (Join-Path $manifest.Folder (Convert-To-CanonicalName -SourceFileName $rawFile -TypeCode $typeCode)) } else { "" }
      SharedAcrossPages = if ($scope -eq "folder") { "yes" } else { "no" }
      Status = $status
      Blocker = $blocker
    }
  }
}

$dateStamp = Get-Date -Format "yyyy-MM-dd"
$lines = @()
$lines += "# NotebookLM media extraction ledger"
$lines += ""
$lines += "Generated: $dateStamp"
$lines += ""
$lines += "| Notebook | Folder | Media Type | Source Title | Original | Canonical | Source Path | Staging Path | Shared | Status | Blocker |"
$lines += "|---|---|---|---|---|---|---|---|---|---|"
foreach ($r in $rows | Sort-Object Folder, NotebookName, OriginalFile) {
  $lines += "| $($r.NotebookName) | $($r.Folder) | $($r.MediaType) | $($r.SourceTitle) | $($r.OriginalFile) | $($r.CanonicalFile) | $($r.SourcePath) | $($r.DestinationPath) | $($r.SharedAcrossPages) | $($r.Status) | $($r.Blocker) |"
}
New-Item -ItemType Directory -Path (Split-Path $LedgerPath -Parent) -Force | Out-Null
Set-Content -Path $LedgerPath -Value ($lines -join [Environment]::NewLine)

Write-Output "STAGING_PATH=$OutputRoot"
Write-Output "LEDGER_PATH=$LedgerPath"

$downloaded = $rows | Where-Object { $_.Status -eq "downloaded" -or $_.Status -eq "already-present" } | Sort-Object CanonicalFile
Write-Output "DOWNLOADED_FILES_START"
foreach ($d in $downloaded) {
  Write-Output $d.CanonicalFile
}
Write-Output "DOWNLOADED_FILES_END"

$blocked = $rows | Where-Object { $_.Status -eq "blocked" -and $_.Blocker }
Write-Output "BLOCKERS_START"
foreach ($b in $blocked) {
  Write-Output "$($b.NotebookName) :: $($b.Blocker)"
}
Write-Output "BLOCKERS_END"
