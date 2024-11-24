FROM python:3.9-slim

# Install Redis
RUN apt-get update && apt-get install -y redis-server && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy requirements.txt if you have one
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# If you don't have a requirements.txt, you can install directly
# RUN pip install --no-cache-dir python-telegram-bot>=20.0

# Copy the rest of your application code
COPY . .

# Start Redis and run the bot
CMD ["sh", "-c", "redis-server --daemonize yes && python bot.py"]
