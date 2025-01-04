# Linkwarden Telegram Bot

A Telegram bot that integrates with Linkwarden to save and manage bookmarks directly from Telegram.

## Features

- Save links to your Linkwarden collection
- Search your bookmarks
- Manage collections
- Automated link metadata extraction

## Installation

## Using Docker

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/linkwarden-telegram-bot.git
cd linkwarden-telegram-bot
```

### 2. Build the Docker image

```bash
docker build -t linkwarden-telegram-bot .
```

### 3. Copy a .env.example to .env file

```bash
cp .env.example .env
```

### 4. Edit the .env file and set the required environment variables

```bash
TELEGRAM_TOKEN=your_bot_token
LINKWARDEN_API_URL=https://your-linkwarden-instance.com/api
LINKWARDEN_API_KEY=your_api_key
LINKWARDEN_COLLECTION_ID=your_collection_id
```

### 5. Run the Docker compose file

```bash
docker-compose up -d
```

## Manual Installation

```bash
pip install -r requirements.txt
```

### Set up environment variables

```bash
export TELEGRAM_TOKEN=your_bot_token 
export LINKWARDEN_API_URL=https://your-linkwarden-instance.com/api 
export LINKWARDEN_API_KEY=your_api_key 
export LINKWARDEN_COLLECTION_ID=your_collection_id
```

### Run the bot

```bash
python bot.py
```

## Usage

### Adding Links

To add a link to your Linkwarden collection, simply send a message containing the link to the bot. The bot will automatically extract the link and add it to your specified collection.

### Example

1. Send a message to the bot with a link:

```plaintext
Check out this cool website: https://example.com
```

2. The bot will respond with a confirmation message:

```plaintext
Links added to Linkwarden:
https://example.com
```

### Error Handling

If the bot encounters an error while adding a link, it will notify you with a message indicating the failed link and the reason for the failure.

## Badges

![Build Status](https://img.shields.io/github/actions/workflow/status/yourusername/linkwarden-telegram-bot/docker-publish.yml?branch=main)
![Code Coverage](https://img.shields.io/codecov/c/github/yourusername/linkwarden-telegram-bot)
![License](https://img.shields.io/github/license/yourusername/linkwarden-telegram-bot)
