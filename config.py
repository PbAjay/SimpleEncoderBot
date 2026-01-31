import os

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID"))

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = "video_encoder"

DOWNLOAD_DIR = "downloads"
ENCODE_DIR = "encoded"

FFMPEG_BIN = "ffmpeg"
FFPROBE_BIN = "ffprobe"
