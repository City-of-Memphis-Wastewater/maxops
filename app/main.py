from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
from fastapi.responses import HTMLResponse

from app.routes import forms, queries

# Initialize FastAPI app
app = FastAPI()

# Mount static files for CSS, JS, and other assets
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include routers for modular routes
app.include_router(forms.router)
app.include_router(queries.router)

# Initialize templates
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def root():
    return {"message": "Welcome to MaxOps Forms!"}

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("static/favicon.ico")


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

# Route for the Daily Form
@app.get("/daily-form", response_class=HTMLResponse)
def get_daily_form(request: Request):
    return templates.TemplateResponse("daily_form.html", {"request": request})

# Route for the Hourly Form
@app.get("/hourly-form", response_class=HTMLResponse)
def get_hourly_form(request: Request):
    return templates.TemplateResponse("hourly_form.html", {"request": request})

# Route for the Dashboard
@app.get("/dashboard", response_class=HTMLResponse)
def get_dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

# Route for the outfall_daily_form
@app.get("/outfall-daily-form", response_class=HTMLResponse)
def get_dashboard(request: Request):
    return templates.TemplateResponse("outfall_daily_form.html", {"request": request})
