param (
    [string]$BatchFile = "afternoon_workflow.txt" # Default batch file
)

# Set batch file path
$batchFilePath = ".\batch\$BatchFile"

if (Test-Path $batchFilePath) {
    Write-Host "Executing batch script: $BatchFile"
    Get-Content $batchFilePath | ForEach-Object {
        $command = $_.Trim()
        if ($command -ne "" -and -not $command.StartsWith("#")) {
            Write-Host "Executing: $command"
            Invoke-Expression $command
        }
    }
} else {
    Write-Host "Batch file not found: $BatchFile"
}
