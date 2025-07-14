#!/usr/bin/env python3
import os
import subprocess
import telebot
from dotenv import load_dotenv
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Load config
load_dotenv('/opt/n8n_bot/n8n_bot_config.env')
BOT_TOKEN = os.getenv("BOT_TOKEN")
AUTHORIZED_USER = int(os.getenv("AUTHORIZED_USER"))
DOMAIN = os.getenv("DOMAIN")
BACKUP_DIR = "/opt/n8n_backups"

bot = telebot.TeleBot(BOT_TOKEN)
os.makedirs(BACKUP_DIR, exist_ok=True)

def is_authorized(message):
    return message.from_user.id == AUTHORIZED_USER

# /help and /start
@bot.message_handler(commands=["help", "start"])
def help_cmd(message):
    if not is_authorized(message): return
    bot.reply_to(message, """🤖 *n8n Bot Control Panel*

📦 Backup Commands:
/createbackup – Save a new backup
/showbackup – Send latest backup with Restore button
📤 Upload a backup file (.tar.gz) to restore it automatically

⚙️ Management:
/status – Check if container is running
/logs – Show recent logs
/restart – Restart n8n
/update – Update n8n to latest
/restore – Restore last saved backup

/help – Show this message again
""", parse_mode="Markdown")

# /status
@bot.message_handler(commands=["status"])
def status(message):
    if not is_authorized(message): return
    out = subprocess.getoutput("docker ps --filter name=n8n")
    bot.reply_to(message, f"📦 *n8n Status:*\n```\n{out}\n```", parse_mode="Markdown")

# /logs
@bot.message_handler(commands=["logs"])
def logs(message):
    if not is_authorized(message): return
    out = subprocess.getoutput("docker logs --tail 50 n8n")
    bot.reply_to(message, f"📄 *n8n Logs:*\n```\n{out}\n```", parse_mode="Markdown")

# /restart
@bot.message_handler(commands=["restart"])
def restart(message):
    if not is_authorized(message): return
    subprocess.run(["docker", "restart", "n8n"])
    bot.reply_to(message, "🔁 n8n restarted!")

# /update
@bot.message_handler(commands=["update"])
def update(message):
    if not is_authorized(message): return
    subprocess.run("docker pull n8nio/n8n:latest", shell=True)
    subprocess.run("docker rm -f n8n", shell=True)
    subprocess.run(
        f"docker run -d --restart unless-stopped --name n8n -p 5678:5678 "
        f"-e N8N_HOST='{DOMAIN}' -e WEBHOOK_URL='https://{DOMAIN}/' "
        f"-e WEBHOOK_TUNNEL_URL='https://{DOMAIN}/' "
        f"-v /var/n8n:/home/node/.n8n n8nio/n8n:latest",
        shell=True
    )
    bot.reply_to(message, "✅ n8n updated and restarted!")

# /createbackup
@bot.message_handler(commands=["createbackup"])
def create_backup(message):
    if not is_authorized(message): return
    backup_path = f"{BACKUP_DIR}/n8n-backup-$(date +%F).tar.gz"
    subprocess.run(f"tar -czf {backup_path} /var/n8n", shell=True)
    bot.reply_to(message, f"📦 Backup created:\n`{backup_path}`", parse_mode="Markdown")

# /showbackup
@bot.message_handler(commands=["showbackup"])
def show_backup(message):
    if not is_authorized(message): return
    latest = subprocess.getoutput(f"ls -t {BACKUP_DIR}/*.tar.gz | head -n 1")
    if os.path.exists(latest):
        bot.send_document(message.chat.id, open(latest, "rb"))
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("🔁 Restore this Backup", callback_data="restore_backup"))
        bot.send_message(message.chat.id, "📂 Tap below to restore the above backup:", reply_markup=markup)
    else:
        bot.reply_to(message, "⚠️ No backup found.")

# /restore (manual)
@bot.message_handler(commands=["restore"])
def manual_restore(message):
    if not is_authorized(message): return
    latest = subprocess.getoutput(f"ls -t {BACKUP_DIR}/*.tar.gz | head -n 1")
    if os.path.exists(latest):
        subprocess.run(f"tar -xzf {latest} -C /", shell=True)
        subprocess.run("docker restart n8n", shell=True)
        bot.reply_to(message, "✅ Restored from latest backup.")
    else:
        bot.reply_to(message, "⚠️ No backup found.")

# Restore from inline button
@bot.callback_query_handler(func=lambda call: call.data == "restore_backup")
def restore_button(call):
    if call.from_user.id != AUTHORIZED_USER:
        bot.answer_callback_query(call.id, "❌ Unauthorized")
        return
    latest = subprocess.getoutput(f"ls -t {BACKUP_DIR}/*.tar.gz | head -n 1")
    if os.path.exists(latest):
        subprocess.run(f"tar -xzf {latest} -C /", shell=True)
        subprocess.run("docker restart n8n", shell=True)
        bot.send_message(call.message.chat.id, "✅ Backup restored successfully.")
        bot.answer_callback_query(call.id, "✅ Restored!")
    else:
        bot.send_message(call.message.chat.id, "⚠️ No backup to restore.")
        bot.answer_callback_query(call.id, "❌ No backup found.")

# Handle uploaded backup files
@bot.message_handler(content_types=["document"])
def upload_backup(message):
    if not is_authorized(message): return
    doc = message.document
    if not doc.file_name.endswith(".tar.gz"):
        bot.reply_to(message, "⚠️ Only .tar.gz backup files are supported.")
        return
    try:
        file_info = bot.get_file(doc.file_id)
        downloaded = bot.download_file(file_info.file_path)
        path = f"{BACKUP_DIR}/{doc.file_name}"
        with open(path, "wb") as f:
            f.write(downloaded)
        subprocess.run(f"tar -xzf {path} -C /", shell=True)
        subprocess.run("docker restart n8n", shell=True)
        bot.reply_to(message, f"✅ Backup `{doc.file_name}` restored and n8n restarted!", parse_mode="Markdown")
    except Exception as e:
        bot.reply_to(message, f"❌ Restore failed: {str(e)}")

# Start bot polling
bot.polling()
