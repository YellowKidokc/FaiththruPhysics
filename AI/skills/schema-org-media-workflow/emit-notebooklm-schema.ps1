[CmdletBinding()]
param()
$canonical = 'D:\GitHub\Python-WEB\AI\skills\schema-org-media-workflow\emit-notebooklm-schema.ps1'
if (-not (Test-Path -LiteralPath $canonical)) {
    throw "Canonical script not found: $canonical"
}
& powershell -ExecutionPolicy Bypass -File $canonical @args
