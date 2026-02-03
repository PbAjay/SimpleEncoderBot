import os
from config import DOWNLOAD_DIR, ENCODE_DIR
from download.downloader import download_file
from ffmpeg.command import build_ffmpeg_command
from ffmpeg.runner import run_ffmpeg
from ffmpeg.probe import get_duration
from database.jobs import update_status

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
