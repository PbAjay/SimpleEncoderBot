import time
from utils.timefmt import seconds_to_hms

async def download_file(message, output, status):
    start = time.time()

    async def progress(cur, total):
        elapsed = time.time() - start
        speed = cur / elapsed if elapsed else 0
        eta = int((total - cur) / speed) if speed else 0
        percent = cur * 100 / total

        await status.edit_text(
            f"⬇️ Downloading\n\n"
            f"{percent:.2f}%\n"
            f"Speed: {speed/1024/1024:.2f} MB/s\n"
            f"ETA: {seconds_to_hms(eta)}"
        )

    return await message.download(output, progress=progress)
