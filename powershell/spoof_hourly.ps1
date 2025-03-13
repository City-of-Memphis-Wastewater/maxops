# Define sample data
$data = @{
	"timestamp_entry_ISO" = "2025-03-10T13:24:00"
    "timestamp_intended_ISO" = "2025-03-10T14:00:00"
    "influent_flow_rate_MGD" = 1.5
    "after_wet_well_flow_rate_MGD" = 2.0
    "effluent_flow_rate_MGD" = 1.8
    "was_flow_rate_MGD" = 0.5
    "operator" = "JohnDoe"
}

# Send POST request to the FastAPI endpoint
$response = Invoke-RestMethod -Uri "http://localhost:8000/submit-hourly" -Method POST -Body $data -ContentType "application/x-www-form-urlencoded"

# Output response from server
Write-Host "Server response: $($response | ConvertTo-Json -Depth 10)"

