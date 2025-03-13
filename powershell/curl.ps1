curl -X POST http://localhost:8000/submit-hourly \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "timestamp_entry_ISO=2025-03-10T13:24:00" \
-d "timestamp_intended_ISO=2025-03-10T14:00:00" \
-d "influent_flow_rate_MGD=1.5" \
-d "after_wet_well_flow_rate_MGD=2.0" \
-d "effluent_flow_rate_MGD=1.8" \
-d "was_flow_rate_MGD=0.5" \
-d "operator=JohnDoe"
