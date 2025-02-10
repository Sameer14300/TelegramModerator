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
pip3 install -r requirements.txt
```

3. Create service file:
```bash
sudo nano /etc/systemd/system/telegram-bot.service
```

Add this content:
```ini
[Unit]
Description=Telegram Bio Link Detection Bot
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/path/to/bot
ExecStart=/usr/bin/python3 bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```

4. Start bot:
```bash
sudo systemctl start telegram-bot
sudo systemctl enable telegram-bot
```

5. Check logs:
```bash
sudo journalctl -u telegram-bot -f