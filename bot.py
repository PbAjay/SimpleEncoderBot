import asyncio
import os
from pyrogram import Client

from config import *
from utils.logger import log
from ffmpeg.installer import ensure_ffmpeg

from telegram.start import register_start
from telegram.uploads import register_uploads
from telegram.callbacks import register_callbacks
from telegram.processor import process_job

from jobqueue.scheduler import start_worker, enqueue
from database.jobs import resume_jobs
from utils.keepalive import start_keepalive

# ensure folders exist
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

    # 🔥 START FAKE HTTP SERVER FOR RENDER FREE TIER
    await start_keepalive()

    await ensure_ffmpeg()
    await app.start()
    
    # register telegram handlers
    register_start(app)
    register_uploads(app)
    register_callbacks(app)

    # 🔥 SAFE RESUME LOGIC (NO CIRCULAR IMPORT)
    async def process_wrapper(job):
        # job["settings"] already contains state dict
        await process_job(app, job, job["settings"])

    await resume_jobs(enqueue, process_wrapper)

    # start background worker
    asyncio.create_task(start_worker())

    log("Bot fully operational")

    # keep process alive
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
