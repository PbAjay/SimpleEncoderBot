import asyncio
import os
from pyrogram import Client

from config import *
from utils.logger import log
from ffmpeg.installer import ensure_ffmpeg
from telegram.start import register_start
from telegram.uploads import register_uploads
from telegram.callbacks import register_callbacks
from jobqueue.scheduler import start_worker
from database.jobs import resume_jobs

os.makedirs(DOWNLOAD_DIR, exist_ok=True)
os.makedirs(ENCODE_DIR, exist_ok=True)

app = Client(
    "video-encoder-bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

async def main():
    log("Boot sequence started")

    await ensure_ffmpeg()
    await app.start()

    register_start(app)
    register_uploads(app)
    register_callbacks(app)

    await resume_jobs(app)

    asyncio.create_task(start_worker())

    log("Bot fully operational")
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
