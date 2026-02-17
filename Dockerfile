FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY availability_scanner.py .
COPY availability_scanner_discord.py .

# Set environment variables (can be overridden at runtime)
ENV DISCORD_WEBHOOK_URL=""
ENV CHECK_INTERVAL=300

# Run the scanner
CMD ["python", "-u", "availability_scanner_discord.py"]
