
# Use Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy app code and dependencies
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8000
EXPOSE 5000

# Run the FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]
