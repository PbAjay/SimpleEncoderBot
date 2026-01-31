from pyrogram import filters
from telegram.buttons import encode_buttons
from utils.auth import is_authorized
from core.state import EncodeState

USER_STATES = {}

def register_uploads(app):

    @app.on_message(filters.video | filters.document)
    async def receive(_, msg):
        if not is_authorized(msg.from_user.id):
            return

        USER_STATES[msg.from_user.id] = EncodeState(msg)

        await msg.reply(
            "Select encoding options below:",
            reply_markup=encode_buttons()
        )
