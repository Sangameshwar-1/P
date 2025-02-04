# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Upgrade pip to the latest version
RUN pip install --upgrade pip

# Copy the current directory contents into the container at /app
COPY . /app

# Install dependencies
RUN pip install -r requirements.txt

# Expose the Flask app port (default is 5000)
EXPOSE 5000

# Define the command to run the Flask app
CMD ["python", "main.py"]
