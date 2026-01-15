# Use a small Python image
FROM python:3.12-slim

# Set working directory inside container
WORKDIR /app

# Copy requirements first (faster rebuilds)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your code
COPY . .

# Expose the port your app uses
EXPOSE 5000

# Run the app
CMD ["python", "devops-project-quote-api/app.py"]