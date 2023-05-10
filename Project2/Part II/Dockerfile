# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 80 for the server
EXPOSE 80

# Run the server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
