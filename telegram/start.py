from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.auth import is_authorized

def register_start(app):

    @app.on_message(filters.command("start"))
    async def start(_, msg):
        if not is_authorized(msg.from_user.id):
            return

        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("About", callback_data="about"),
                InlineKeyboardButton("Help", callback_data="help")
            ]
        ])

        await msg.reply("Hey Welcome To Video Encoder Bot", reply_markup=keyboard)

    @app.on_callback_query(filters.regex("^about$"))
    async def about(_, q):
        await q.message.edit_text(
            "Name: Video Encoder 📷\n"
            "Code: Python 🐍\n"
            "Version: Latest 😏\n"
            "Creator: @RealxAJAY"
        )

    @app.on_callback_query(filters.regex("^help$"))
    async def help(_, q):
        await q.message.edit_text(
            "HEVC & x264\nAAC / Opus / EAC3\n\nUpload a video to encode."
        )
