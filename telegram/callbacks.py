from pyrogram import filters
from utils.auth import is_authorized
from core.validator import validate_state
from database.jobs import create_job, save_job
from jobqueue.scheduler import enqueue
from telegram.uploads import USER_STATES
from telegram.processor import process_job   # ✅ NEW IMPORT

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
