from fastapi import APIRouter

router = APIRouter()

@router.get("/api/recent-hourly")
async def get_recent_hourly_data():
    # Dummy data for now; replace with actual database query
    data = [
        {"timestamp": "2025-03-05T08:00:00", "flow_rate": 150.5, "cod": 40.2, "water_quality": "good"},
        {"timestamp": "2025-03-05T09:00:00", "flow_rate": 148.7, "cod": 39.8, "water_quality": "excellent"},
    ]
    return {"data": data}
