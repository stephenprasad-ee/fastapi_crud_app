FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the application code
COPY . .

# Expose app port
EXPOSE 8000

# Default command (runs app)
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
