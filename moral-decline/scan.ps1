$files = Get-ChildItem -Recurse -Filter *.html
$allFiles = @()
foreach ($f in $files) {
    $allFiles += $f.FullName.ToLower()
    $allFiles += (Join-Path $f.DirectoryName $f.Name).ToLower()
}

$broken = @()
foreach ($file in $files) {
    $content = Get-Content $file.FullName -Raw
    $matches = [regex]::Matches($content, 'href="([^"]+\.html)"')
    foreach ($m in $matches) {
        $href = $m.Groups[1].Value
        if ($href -match '^https?://' -or $href -match '^//') { continue }
        
        $target = $null
        if ($href -match '^/') {
            $target = "\\192.168.1.177\Desktop\faiththruphysics.com" + $href
        } elseif ($href -match '^\.\./') {
            $base = $file.DirectoryName
            $parts = $href -split '/'
            foreach ($part in $parts) {
                if ($part -eq '..') { $base = Split-Path $base -Parent }
                elseif ($part -ne '' -and $part -ne '.') { $base = Join-Path $base $part }
            }
            $target = $base
        } else {
            $target = Join-Path $file.DirectoryName $href
        }
        
        if ($target -and ($allFiles -notcontains $target.ToLower())) {
            $relFile = $file.FullName.Replace('\\192.168.1.177\Desktop\faiththruphysics.com\moral-decline\','')
            $broken += "$relFile | $href"
        }
    }
}
$broken | Sort-Object -Unique
