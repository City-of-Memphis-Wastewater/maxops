$uri = "http://localhost:8000/submit-hourly"
$body = @{
    timestamp_entry_ISO = "2025-03-10T13:24:00"
    timestamp_intended_ISO = "2025-03-10T14:00:00"
    influent_flow_rate_MGD = 1.5
    after_wet_well_flow_rate_MGD = 2.0
    effluent_flow_rate_MGD = 1.8
    was_flow_rate_MGD = 0.5
    operator = "JohnDoe"
}
$response = Invoke-WebRequest -Uri $uri -Method Post -Body $body -ContentType "application/x-www-form-urlencoded"
Write-Output $response.Content
