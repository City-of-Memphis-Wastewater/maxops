# Run the FastAPI web app
Write-Host "Starting the FastAPI web app..."
try {
    poetry run python -m uvicorn app.main:app --reload
} catch {
    Write-Host "Error starting the web app. Please ensure all dependencies are installed and the app is correctly set up."
}
