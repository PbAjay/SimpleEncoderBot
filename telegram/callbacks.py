import os
from pyrogram import filters
from utils.auth import is_authorized
from core.validator import validate_state
from download.downloader import download_file
from ffmpeg.command import build_ffmpeg_command
from ffmpeg.runner import run_ffmpeg
from ffmpeg.probe import get_duration
from database.jobs import create_job, save_job, update_status
from jobqueue.scheduler import enqueue
from config import DOWNLOAD_DIR, ENCODE_DIR
from telegram.uploads import USER_STATES

def register_callbacks(app):

    @app.on_callback_query()
    async def callback(_, q):
        uid = q.from_user.id
        if not is_authorized(uid) or uid not in USER_STATES:
            return

        state = USER_STATES[uid]
        data = q.data

        if data.startswith("res_"):
            state.resolution = int(data.split("_")[1])

        elif data == "v_x265":
            state.video_codec = "libx265"
        elif data == "v_x264":
            state.video_codec = "libx264"

        elif data == "bit_10":
            state.pixel_format = "yuv420p10le"
        elif data == "bit_8":
            state.pixel_format = "yuv420p"

        elif data == "a_aac":
            state.audio_codec = "aac"
        elif data == "a_opus":
            state.audio_codec = "libopus"
        elif data == "a_eac3":
            state.audio_codec = "eac3"

        elif data == "mode_media":
            state.upload_mode = "media"
        elif data == "mode_doc":
            state.upload_mode = "document"

        elif data == "start_encode":
            validate_state(state)
            await create_and_enqueue_job(app, q.message, state)

        await q.answer("Updated")

async def create_and_enqueue_job(app, message, state):
    job = create_job(
        chat_id=message.chat.id,
        file_id=state.source_message.id,
        settings=state.as_dict()
    )

    await save_job(job)

    async def task():
        await process_job(app, job, state)

    await enqueue(task)

async def process_job(app, job, state):
    status = await app.send_message(job["chat_id"], "⬇️ Downloading...")

    input_path = os.path.join(DOWNLOAD_DIR, f"{job['_id']}.input")
    output_path = os.path.join(ENCODE_DIR, f"{job['_id']}.mkv")

    await update_status(job["_id"], "downloading")

    await download_file(state.source_message, input_path, status)

    duration = get_duration(input_path)

    await update_status(job["_id"], "encoding")

    async def progress(percent, speed):
        await status.edit_text(
            f"🎞 Encoding\n\n"
            f"{percent:.2f}%\n"
            f"Speed: {speed}\n"
            f"{state.resolution}p | {state.video_codec}\n"
            f"{state.audio_codec} 192k"
        )

    cmd = build_ffmpeg_command(input_path, output_path, state)
    await run_ffmpeg(cmd, duration, progress)

    await update_status(job["_id"], "done")

    if state.upload_mode == "media":
        await app.send_video(job["chat_id"], output_path)
    else:
        await app.send_document(job["chat_id"], output_path)

    await status.edit_text("✅ Encoding completed")
