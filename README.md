BOT_TOKEN=your_telegram_bot_token
OWNER_ID=your_telegram_user_id
API_ID=your_api_id
API_HASH=your_api_hash
MONGODB_URI=your_mongodb_atlas_uri
```

## Deployment Commands

1. Update system and install requirements:
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3 python3-pip git -y
```

2. Clone and setup:
```bash
git clone <repository-url>
cd telegram-bio-link-bot
```

3. Create service file:
```bash
sudo nano /etc/systemd/system/telegram-bot.service
```

[Unit]
Description=Telegram Bio Link Detection Bot
After=network.target

[Service]
Type=simple
User=your_username        # Replace with your actual system username
WorkingDirectory=/home/your_username/telegram-bio-link-bot   # Replace with actual path where you cloned the bot
Environment="BOT_TOKEN=your_bot_token"                       # Replace with your actual bot token
Environment="API_ID=your_api_id"                            # Replace with your API ID
Environment="API_HASH=your_api_hash"                        # Replace with your API hash
Environment="OWNER_ID=your_owner_id"                        # Replace with your Telegram user ID
Environment="MONGODB_URI=your_mongodb_uri"                  # Replace with your MongoDB connection string
ExecStart=/usr/bin/python3 bot.py
Restart=always

[Install]
WantedBy=multi-user.target

4. Start bot:
```bash
sudo systemctl start telegram-bot
sudo systemctl enable telegram-bot
```

5. Check logs:
```bash
sudo journalctl -u telegram-bot -f
