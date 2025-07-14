#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────
# n8n Telegram Bot Installer – Final Version (Pro)
# Usage:
# curl -fsSL https://raw.githubusercontent.com/webclasher/n8n-Telegram-Bot-Installer-Final-Version-Pro/main/install.sh | sudo bash -s \
#   "n8n.yourdomain.com" "you@example.com" "BOT_TOKEN" "USER_ID"
# ─────────────────────────────────────────────────────────────

set -euo pipefail

# Ensure essential tools are installed
echo -e "\n🔍 Checking for required tools (bash, curl, sudo)..."
REQUIRED_PKGS=(bash curl sudo)
for pkg in "${REQUIRED_PKGS[@]}"; do
  if ! command -v "$pkg" &>/dev/null; then
    echo "🔧 Installing missing package: $pkg"
    apt update -y && apt install -y "$pkg"
  fi
done

# Parse input arguments
DOMAIN=${1:-}
EMAIL=${2:-}
BOT_TOKEN=${3:-}
USER_ID=${4:-}

if [[ -z "$DOMAIN" || -z "$EMAIL" || -z "$BOT_TOKEN" || -z "$USER_ID" ]]; then
  echo -e "\n❌ Missing arguments!"
  echo "Usage:"
  echo "  bash install.sh \"your-domain.com\" \"your@email.com\" \"BOT_TOKEN\" \"USER_ID\""
  exit 1
fi

BOT_DIR="/opt/n8n_bot"
BACKUP_DIR="/opt/n8n_backups"

# Install required system packages
echo -e "\n📦 Installing Python and required libraries..."
apt update -y
apt install -y python3 python3-pip unzip curl

# Fix for Debian 12: bypass PEP 668
pip3 install --break-system-packages python-telegram-bot telebot python-dotenv

# Create directories
mkdir -p "$BOT_DIR"
mkdir -p "$BACKUP_DIR"

# Download bot script
echo -e "\n📥 Downloading bot script from GitHub..."
curl -fsSL https://raw.githubusercontent.com/webclasher/n8n-Telegram-Bot-Installer-Final-Version-Pro/refs/heads/main/n8n_bot.py -o "$BOT_DIR/n8n_bot.py"

# Save bot credentials to env file
echo -e "\n🔐 Writing bot configuration..."
cat > "$BOT_DIR/n8n_bot_config.env" <<EOF
BOT_TOKEN=$BOT_TOKEN
AUTHORIZED_USER=$USER_ID
DOMAIN=$DOMAIN
EOF

chmod +x "$BOT_DIR/n8n_bot.py"

# Create systemd service for persistent bot
echo -e "\n⚙️ Creating systemd service..."
cat > /etc/systemd/system/n8n-bot.service <<EOF
[Unit]
Description=n8n Telegram Bot Service
After=network.target docker.service

[Service]
ExecStart=/usr/bin/python3 $BOT_DIR/n8n_bot.py
WorkingDirectory=$BOT_DIR
Restart=always
EnvironmentFile=$BOT_DIR/n8n_bot_config.env

[Install]
WantedBy=multi-user.target
EOF

# Start the service
echo -e "\n🚀 Starting bot service..."
systemctl daemon-reexec
systemctl daemon-reload
systemctl enable --now n8n-bot.service

# Success message
echo -e "\n✅ Telegram Bot is now installed and running!"
echo -e "🌐 n8n Domain: https://$DOMAIN"
echo -e "🤖 Send /help to your bot to begin!"
echo -e "📦 Bot location: $BOT_DIR"
echo -e "🗃️ Backups location: $BACKUP_DIR"
echo -e "🧾 To view logs: journalctl -u n8n-bot -f"
