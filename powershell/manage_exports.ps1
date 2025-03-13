# Run without parameters to list files: .\manage_exports.ps1
#
# Add the -Clear flag to clear files: .\manage_exports.ps1 -Clear
#
param (
    [switch]$Clear = $false # Default: Do not clear files
)

$exportDir = ".\exports\intermediate"

if (Test-Path $exportDir) {
    Write-Host "Listing files in export directory:"
    Get-ChildItem $exportDir | ForEach-Object { Write-Host $_.Name }

    if ($Clear) {
        Write-Host "Clearing export files..."
        Get-ChildItem $exportDir | Remove-Item -Force
        Write-Host "All files cleared from export directory."
    }
} else {
    Write-Host "Export directory does not exist: $exportDir"
}
