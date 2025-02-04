# Use official Python image
FROM python:3.10

# Set working directory
WORKDIR /app

# Copy requirements.txt
COPY requirements.txt .

# Upgrade pip, install dependencies
RUN pip install --upgrade pip
RUN apt-get update && apt-get install -y build-essential libpq-dev
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files
COPY . .

# Expose FastAPI default port
EXPOSE 8000

# Start FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
