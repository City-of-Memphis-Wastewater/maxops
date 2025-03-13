# Test the /api/recent-hourly endpoint
$response = Invoke-RestMethod -Uri "http://localhost:8000/api/recent-hourly" -Method GET
Write-Host "Recent Hourly Data:"
Write-Host ($response | ConvertTo-Json -Depth 10)

# Test the /submit-hourly endpoint
$data = @{
    "timestamp" = "2025-03-05T16:00:00"
    "flow_rate" = 130.5
    "cod" = 37.0
    "water_quality" = "excellent"
}
$response = Invoke-RestMethod -Uri "http://localhost:8000/submit-hourly" -Method POST -Body $data -ContentType "application/x-www-form-urlencoded"
Write-Host "Submit Hourly Data Response:"
Write-Host ($response | ConvertTo-Json -Depth 10)
