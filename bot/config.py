import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

ADMIN_IDS_RAW = os.getenv("ADMIN_IDS", "")

ADMIN_IDS = [
    int(admin_id.strip())
    for admin_id in ADMIN_IDS_RAW.split(",")
    if admin_id.strip()
]

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не найден. Проверь файл .env")