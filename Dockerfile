FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code and seed data
COPY . .

# Set default port
ENV PORT=8000
EXPOSE 8000

# Start command
CMD ["python", "main.py"]
