Absolutely! Here's a clean, professional `README.md` for your GitHub repo.

---

## ✅ `README.md` — n8n Telegram Bot Installer

````markdown
# 🤖 n8n Telegram Bot Installer (Pro Version)

Easily manage, backup, and restore your **n8n workflows** using a secure **Telegram bot**. This installer is designed for **non-coders** and works even on low-resource VPS like **Google Cloud free-tier**, **Hetzner**, or **DigitalOcean**.

---

## 🚀 Features

- 🔧 Install & configure the Telegram bot automatically
- 🔁 Restart, update, or check n8n status via Telegram
- 📦 Create weekly & on-demand backups
- 📤 Download or upload backup files directly via Telegram
- ✅ Restore backups — even across different servers!
- 🔐 Secure: Only one authorized user can access the bot

---

## 📥 One-Line Installation

```bash
sudo apt update -y && sudo apt upgrade -y && sudo apt install -y bash curl || sudo yum update -y && sudo yum install -y bash curl || sudo dnf update -y && sudo dnf install -y bash curl

curl -fsSL https://raw.githubusercontent.com/webclasher/n8n-Telegram-Bot-Installer-Final-Version-Pro/refs/heads/main/install.sh | sudo bash -s \
  "n8n.yourdomain.com" \
  "you@example.com" \
  "YOUR_TELEGRAM_BOT_TOKEN" \
  "YOUR_TELEGRAM_USER_ID"
````

> Replace each field with your own values:
>
> * **yourdomain.com** – the full domain where n8n is running
> * **[you@example.com](mailto:you@example.com)** – your email (used for SSL certificate)
> * **TELEGRAM\_BOT\_TOKEN** – from [@BotFather](https://t.me/BotFather)
> * **TELEGRAM\_USER\_ID** – your numeric Telegram ID (see below)

---

## 🧠 How to Get Your Telegram Credentials

### 🔹 Get a Bot Token

1. Open [@BotFather](https://t.me/BotFather)
2. Use `/newbot` and follow the instructions
3. Copy the bot token (e.g., `123456789:ABCDefGhIjKlMnOpQrStUvWxYz`)

### 🔹 Get Your Telegram User ID

1. Open [@userinfobot](https://t.me/userinfobot)
2. Start the bot
3. It will show:
   `Your Telegram ID: 123456789`

---

## 🤖 Bot Commands (in Telegram)

Once installed, just type any of these in your bot chat:

| Command         | Description                            |
| --------------- | -------------------------------------- |
| `/status`       | Show if n8n is running                 |
| `/logs`         | Show recent Docker logs                |
| `/restart`      | Restart the n8n container              |
| `/update`       | Pull the latest n8n version            |
| `/createbackup` | Create a backup of your workflows      |
| `/showbackup`   | Send latest backup + one-click restore |
| `/restore`      | Restore the latest backup              |
| `/help`         | Show all available commands            |

---

## 📦 Backup & Restore Workflows

### 🔹 From Same Server:

1. `/createbackup`
2. `/restore` or use restore button after `/showbackup`

### 🔹 From One Server to Another:

1. On old server: `/createbackup` → `/showbackup` → Download the file
2. On new server: run install script with new domain
3. Upload the backup `.tar.gz` file to the new bot
4. ✅ It will auto-restore and restart n8n

---

## 📂 File Structure (Generated Automatically)

| Path                              | Description                |
| --------------------------------- | -------------------------- |
| `/opt/n8n_bot/n8n_bot.py`         | Telegram bot logic         |
| `/opt/n8n_bot/n8n_bot_config.env` | Auto-generated credentials |
| `/opt/n8n_backups/`               | Where backups are stored   |
| `n8n-bot.service`                 | Systemd service manager    |

---

## 🛑 Security Notes

* Only the Telegram user you specify can control the bot.
* Backup files are stored **locally on the server**, never sent to the cloud.
* You don't need to manually edit any files — just run the script.

---

## 💬 Support

Have a question or request?
[Message @webclasher on Telegram](https://t.me/webclasher)

---

## 📜 License

MIT — Free to use, modify, and share.

```
