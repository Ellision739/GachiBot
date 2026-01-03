import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
VK_TOKEN = os.getenv("VK_USER_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))