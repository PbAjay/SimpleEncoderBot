import subprocess
from config import FFPROBE_BIN

def get_duration(path):
    cmd = [
        FFPROBE_BIN, "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        path
    ]
    result = subprocess.check_output(cmd).decode().strip()
    return int(float(result))
