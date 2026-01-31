import asyncio
from ffmpeg.progress import parse_progress

async def run_ffmpeg(cmd, duration, callback):
    proc = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.DEVNULL
    )

    async for data in parse_progress(proc.stdout):
        if "out_time_ms" in data:
            sec = int(data["out_time_ms"]) // 1_000_000
            percent = min((sec / duration) * 100, 100)
            speed = data.get("speed", "0x")
            await callback(percent, speed)

    await proc.wait()
