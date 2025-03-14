# Define base directory
$baseDir = "maxops"

# Create directories
New-Item -ItemType Directory -Path "$baseDir"
New-Item -ItemType Directory -Path "$baseDir\app"
New-Item -ItemType Directory -Path "$baseDir\app\routes"
New-Item -ItemType Directory -Path "$baseDir\app\utils"
New-Item -ItemType Directory -Path "$baseDir\exports"
New-Item -ItemType Directory -Path "$baseDir\exports\intermediate"
New-Item -ItemType Directory -Path "$baseDir\gui"
New-Item -ItemType Directory -Path "$baseDir\static"
New-Item -ItemType Directory -Path "$baseDir\static\css"
New-Item -ItemType Directory -Path "$baseDir\static\js"
New-Item -ItemType Directory -Path "$baseDir\templates"
New-Item -ItemType Directory -Path "$baseDir\tests"

# Create placeholder files
New-Item -ItemType File -Path "$baseDir\pyproject.toml" -Force
New-Item -ItemType File -Path "$baseDir\poetry.lock" -Force
New-Item -ItemType File -Path "$baseDir\shell.py" -Force
New-Item -ItemType File -Path "$baseDir\Dockerfile" -Force
New-Item -ItemType File -Path "$baseDir\docker-compose.yml" -Force
New-Item -ItemType File -Path "$baseDir\app\__init__.py" -Force
New-Item -ItemType File -Path "$baseDir\app\main.py" -Force
New-Item -ItemType File -Path "$baseDir\app\routes\__init__.py" -Force
New-Item -ItemType File -Path "$baseDir\app\routes\forms.py" -Force
New-Item -ItemType File -Path "$baseDir\app\routes\queries.py" -Force
New-Item -ItemType File -Path "$baseDir\app\utils\__init__.py" -Force
New-Item -ItemType File -Path "$baseDir\app\utils\helpers.py" -Force
New-Item -ItemType File -Path "$baseDir\exports\intermediate\shift_data.csv" -Force
New-Item -ItemType File -Path "$baseDir\exports\intermediate\shift_data.json" -Force
New-Item -ItemType File -Path "$baseDir\gui\local_gui.py" -Force
New-Item -ItemType File -Path "$baseDir\static\css\styles.css" -Force
New-Item -ItemType File -Path "$baseDir\static\js\script.js" -Force
New-Item -ItemType File -Path "$baseDir\templates\dashboard.html" -Force
New-Item -ItemType File -Path "$baseDir\templates\flows_and_cod_hourly_form.html" -Force
New-Item -ItemType File -Path "$baseDir\templates\daily_form.html" -Force
New-Item -ItemType File -Path "$baseDir\tests\test_main.py" -Force
New-Item -ItemType File -Path "$baseDir\tests\test_queries.py" -Force
New-Item -ItemType File -Path "$baseDir\README.md" -Force

# Write basic content for the README file
Set-Content -Path "$baseDir\README.md" -Value "# pavops-maxops
This is a modular, Python-based FastAPI web application.
"
