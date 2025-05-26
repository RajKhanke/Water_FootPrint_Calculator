# Base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy application files
COPY . /app

# Ensure the uploads folder exists and is writable
RUN mkdir -p static/uploads && chmod -R 777 static/uploads

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port your app runs on
EXPOSE 7860

# Command to run the application
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:7860", "app:app"]
