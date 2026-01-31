from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def encode_buttons():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Media", "mode_media"),
         InlineKeyboardButton("Document", "mode_doc")],

        [InlineKeyboardButton("1440p", "res_1440"),
         InlineKeyboardButton("1080p", "res_1080")],

        [InlineKeyboardButton("720p", "res_720"),
         InlineKeyboardButton("480p", "res_480")],

        [InlineKeyboardButton("x265 (HEVC)", "v_x265"),
         InlineKeyboardButton("x264", "v_x264")],

        [InlineKeyboardButton("AAC 192k", "a_aac"),
         InlineKeyboardButton("Opus 192k", "a_opus"),
         InlineKeyboardButton("EAC3 192k", "a_eac3")],

        [InlineKeyboardButton("10bit", "bit_10"),
         InlineKeyboardButton("8bit", "bit_8")],

        [InlineKeyboardButton("Start Encode", "start_encode")]
    ])
