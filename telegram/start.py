from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.auth import is_authorized
from utils.logger import log


def register_start(app):

    @app.on_message(filters.command("start"))
    async def start(_, msg):
        uid = msg.from_user.id

        # 🔍 LOG for debugging (very important)
        log(f"/start received from {uid}")

        # 🔒 AUTH CHECK
        if not is_authorized(uid):
            await msg.reply(
                "🚫 You are not authorized to use this bot."
            )
            return

        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("About", callback_data="about"),
                InlineKeyboardButton("Help", callback_data="help")
            ]
        ])

        await msg.reply(
            "👋 Hey Welcome To Video Encoder Bot\n\n"
            "Choose an option below:",
            reply_markup=keyboard
        )

    @app.on_callback_query(filters.regex("^about$"))
    async def about(_, q):
        await q.message.edit_text(
            "📛 Name: Video Encoder 📷\n"
            "💻 Code: Python 🐍\n"
            "🚀 Version: Latest 😏\n"
            "👤 Creator: @RealxAJAY"
        )

    @app.on_callback_query(filters.regex("^help$"))
    async def help(_, q):
        await q.message.edit_text(
            "🎞 Supported Codecs:\n"
            "• HEVC (x265)\n"
            "• AVC (x264)\n\n"
            "🎧 Audio:\n"
            "• AAC\n"
            "• Opus\n"
            "• EAC3\n\n"
            "📤 Upload a video to start encoding."
        )
