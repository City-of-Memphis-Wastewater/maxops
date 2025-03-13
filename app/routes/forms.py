from fastapi import APIRouter, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
from typing import Optional

import app.utils.helpers as helpers

# Initialize router and templates
router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/hourly-form", response_class=HTMLResponse)
async def render_hourly_form(request: Request):
    return templates.TemplateResponse("hourly_form.html", {"request": request})

@router.post("/submit-hourly")
async def submit_hourly_data(
    request: Request,
    #timestamp_entry_ISO: str = Form(...),
    timestamp_intended_ISO: str = Form(...),
    influent_flow_rate_MGD: Optional[float] = Form(None),
    after_wet_well_flow_rate_MGD: Optional[float] = Form(None),
    effluent_flow_rate_MGD: Optional[float] = Form(None),
    was_flow_rate_MGD: Optional[float] = Form(None),
    cod_predisinfection_mgPerLiter: Optional[float] = Form(None),
    operator: Optional[str] = Form(None),
    ):
    referer = request.headers.get("referer")
    data = {
        "timestamp_entry_ISO": helpers.nowtime(),
        "timestamp_intended_ISO": helpers.sanitize_time(timestamp_intended_ISO),
        "influent_flow_rate_MGD": influent_flow_rate_MGD,
        "after_wet_well_flow_rate_MGD": after_wet_well_flow_rate_MGD,
        "effluent_flow_rate_MGD": effluent_flow_rate_MGD,
        "was_flow_rate_MGD": was_flow_rate_MGD,
        "cod_predisinfection_mgPerLiter":cod_predisinfection_mgPerLiter,
        "operator": operator,
        "source": "web-post-Python-FastAPI",
    }
    helpers.local_save_data_hourly(data)
    # Process the data (you can save it to a database or log it)
    print(f"Received hourly data: {data}")
    # Check if the request comes from an API (e.g., curl) or browser
    # Generalized check for API or non-browser requests
    user_agent = request.headers.get("user-agent", "").lower()
    if not user_agent or any(keyword in user_agent for keyword in ["curl", "httpie", "postman", "powershell", "wget", "python", "api"]):
        return JSONResponse(content={"message": "Hourly data submitted successfully!"})
    else:
        return templates.TemplateResponse(
            "submission_success.html",
            {"request": request, "header": "Hourly Data Submitted Successfully", "data": data, "message": "Hourly data submitted successfully!","previous_page":referer }
            )


@router.post("/submit-daily")
async def submit_daily_data(
    request: Request,
    #timestamp_entry_ISO: str = Form(...),
    timestamp_intended_ISO: str = Form(...),
    flow_rate: float = Form(...),
    cod: float = Form(...),
    water_quality: str = Form(...)
    ):
    referer = request.headers.get("referer")
    data = {
        "timestamp_entry_ISO": helpers.nowtime(),
        "timestamp_intended_ISO": helpers.sanitize_time(timestamp_intended_ISO),
        "flow_rate": flow_rate,
        "cod": cod,
        "water_quality": water_quality,
    }
    helpers.local_save_data_daily(data)
    # Process the data (you can save it to a database or log it)
    print(f"Received hourly data: {timestamp_intended_ISO}, {flow_rate}, {cod}, {water_quality}")
    # Check if the request comes from an API (e.g., curl) or browser
    # Generalized check for API or non-browser requests
    user_agent = request.headers.get("user-agent", "").lower()
    if not user_agent or any(keyword in user_agent for keyword in ["curl", "httpie", "postman", "powershell", "wget", "python", "api"]):
        return JSONResponse(content={"message": "Daily data submitted successfully!"})
    else:
        return templates.TemplateResponse(
            "submission_success.html",
            {"request": request, "header": "Daily Data Submitted Successfully", "data": data, "message": "Daily data submitted successfully!","previous_page":referer}
            )
    

@router.post("/submit-outfall")
async def submit_outfall_data(
    request: Request,
    #timestamp_entry_ISO: str = Form(...),
    timestamp_intended_ISO: str = Form(...),
    safe_to_make_observation: bool = Form(...),
    floatable_present: bool = Form(...),
    scum_present: bool = Form(...),
    foam_present: bool = Form(...),
    oil_present: bool = Form(...),
    operator: Optional[str] = Form(None),
    ):
    referer = request.headers.get("referer")

    data = {
        "timestamp_entry_ISO": helpers.nowtime(),
        "timestamp_intended_ISO": helpers.sanitize_time(timestamp_intended_ISO),
        "safe_to_make_observation": safe_to_make_observation,
        "floatable_present": floatable_present,
        "scum_present": scum_present,
        "foam_present": foam_present,
        "oil_present": oil_present,
        "operator": operator,
        "source": "web-post-Python-FastAPI",
    }

    # Save the data using the appropriate helper method
    helpers.local_save_data_outfall(data)

    # Log for debugging
    print(f"Received outfall data: {data}")
    # Check if the request comes from an API (e.g., curl) or browser
    # Generalized check for API or non-browser requests
    user_agent = request.headers.get("user-agent", "").lower()
    if not user_agent or any(keyword in user_agent for keyword in ["curl", "httpie", "postman", "powershell", "wget", "python", "api"]):
        return JSONResponse(content={"message": "Outfall data submitted successfully!"})
    else:
        return templates.TemplateResponse(
            "submission_success.html",
            {"request": request, "header": "Outfall Data Submitted Successfully", "data": data, "message": "Outfall data submitted successfully!","previous_page":referer}
            )

@router.post("/submit-basin-clarifier-hourly")
async def submit_basin_clarifier_hourly(
    request: Request,
    timestamp_intended_ISO: str = Form(...),
    north_basin_1_MGD: float = Form(...),
    north_basin_3_MGD: float = Form(...),
    north_basin_5_MGD: float = Form(...),
    north_basin_7_MGD: float = Form(...),
    north_basin_9_MGD: float = Form(...),
    north_basin_11_MGD: float = Form(...),
    north_basin_13_MGD: float = Form(...),

    south_basin_1_MGD: float = Form(...),
    south_basin_3_MGD: float = Form(...),
    south_basin_5_MGD: float = Form(...),
    south_basin_7_MGD: float = Form(...),
    south_basin_9_MGD: float = Form(...),
    south_basin_11_MGD: float = Form(...),
    south_basin_13_MGD: float = Form(...),

    north_clarifier_1_MGD: float = Form(...),
    north_clarifier_2_MGD: float = Form(...),
    north_clarifier_3_MGD: float = Form(...),
    north_clarifier_4_MGD: float = Form(...),

    south_clarifier_1_MGD: float = Form(...),
    south_clarifier_2_MGD: float = Form(...),
    south_clarifier_3_MGD: float = Form(...),
    south_clarifier_4_MGD: float = Form(...),

    north_ras_1_MGD: float = Form(...),
    north_ras_2_MGD: float = Form(...),
    north_ras_3_MGD: float = Form(...),
    north_ras_4_MGD: float = Form(...),

    south_ras_1_MGD: float = Form(...),
    south_ras_2_MGD: float = Form(...),
    south_ras_3_MGD: float = Form(...),
    south_ras_4_MGD: float = Form(...),
    operator: Optional[str] = Form(None)
    ):
    referer = request.headers.get("referer")

    
    data = {
        "timestamp_entry_ISO": helpers.nowtime(),
        "timestamp_intended_ISO": helpers.sanitize_time(timestamp_intended_ISO),
        "operator": operator,
        "source": "web-post-Python-FastAPI",
        "north_basin_1_MGD":north_basin_1_MGD,
        "north_basin_3_MGD":north_basin_3_MGD,
        "north_basin_5_MGD":north_basin_5_MGD,
        "north_basin_7_MGD":north_basin_7_MGD,
        "north_basin_9_MGD":north_basin_9_MGD,
        "north_basin_11_MGD":north_basin_11_MGD,
        "north_basin_13_MGD":north_basin_13_MGD,

        "south_basin_1_MGD":south_basin_1_MGD,
        "south_basin_3_MGD":south_basin_3_MGD,
        "south_basin_5_MGD":south_basin_5_MGD,
        "south_basin_7_MGD":south_basin_7_MGD,
        "south_basin_9_MGD":south_basin_9_MGD,
        "south_basin_11_MGD":south_basin_11_MGD,
        "south_basin_13_MGD":south_basin_13_MGD,

        "north_clarifier_1_MGD":north_clarifier_1_MGD,
        "north_clarifier_2_MGD":north_clarifier_2_MGD,
        "north_clarifier_3_MGD":north_clarifier_3_MGD,
        "north_clarifier_4_MGD":north_clarifier_4_MGD,

        "south_clarifier_1_MGD":south_clarifier_1_MGD,
        "south_clarifier_2_MGD":south_clarifier_2_MGD,
        "south_clarifier_3_MGD":south_clarifier_3_MGD,
        "south_clarifier_4_MGD":south_clarifier_4_MGD,

        "north_ras_1_MGD":north_ras_1_MGD,
        "north_ras_2_MGD":north_ras_2_MGD,
        "north_ras_3_MGD":north_ras_3_MGD,
        "north_ras_4_MGD":north_ras_4_MGD,

        "south_ras_1_MGD":south_ras_1_MGD,
        "south_ras_2_MGD":south_ras_2_MGD,
        "south_ras_3_MGD":south_ras_3_MGD,
        "south_ras_4_MGD":south_ras_4_MGD,
    }

    # Save the data using the appropriate helper method
    helpers.local_save_data_basin_clarifier_hourly(data)

    # Log for debugging
    print(f"Received basin and clarifier hourly data: {data}")
    # Check if the request comes from an API (e.g., curl) or browser
    # Generalized check for API or non-browser requests
    user_agent = request.headers.get("user-agent", "").lower()
    if not user_agent or any(keyword in user_agent for keyword in ["curl", "httpie", "postman", "powershell", "wget", "python", "api"]):
        return JSONResponse(content={"message": "Basin and clarifier hourly data submitted successfully!"})
    else:
        return templates.TemplateResponse(
            "submission_success.html",
            {"request": request, "header": "Basin and Clarifier Data Submitted Successfully", "data": data, "message": "Outfall data submitted successfully!","previous_page":referer}
            )

