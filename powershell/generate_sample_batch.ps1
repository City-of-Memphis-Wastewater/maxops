# Define batch directory and file
$batchDir = ".\batch"
$sampleFile = "$batchDir\afternoon_workflow.txt"

# Ensure batch directory exists
if (-Not (Test-Path $batchDir)) {
    New-Item -ItemType Directory -Path $batchDir -Force
    Write-Host "Created batch directory: $batchDir"
}

# Write sample batch commands
$batchCommands = @"
# Spoof hourly data entries for the afternoon
spoof_hourly 2025-03-05T13:00:00 120.5 38.1 good
spoof_hourly 2025-03-05T14:00:00 125.0 37.9 excellent
spoof_hourly 2025-03-05T15:00:00 115.3 39.2 fair

# Submit the daily summary
spoof_daily 2025-03-05 operational "Routine maintenance completed in the afternoon."

# List export files
list_exports

# Clear the export directory
clear_exports
"@

Set-Content -Path $sampleFile -Value $batchCommands
Write-Host "Sample batch script generated: $sampleFile"
