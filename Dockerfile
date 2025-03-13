# Stage 1: Build dependencies
FROM python:3.10-slim AS builder

# Install Poetry
RUN pip install poetry

# Set the working directory
WORKDIR /app

# Copy pyproject.toml and poetry.lock
COPY pyproject.toml poetry.lock /app/

# Install dependencies
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

# Stage 2: Build production image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file from the builder stage
COPY --from=builder /app/requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . /app/

# Run the app
CMD ["python", "main.py"]
