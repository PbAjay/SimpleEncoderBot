def build_ffmpeg_command(input_path, output_path, state):
    return [
        "ffmpeg", "-y",
        "-i", input_path,
        "-vf", f"scale=-2:{state.resolution}",
        "-c:v", state.video_codec,
        "-pix_fmt", state.pixel_format,
        "-crf", str(state.crf),
        "-c:a", state.audio_codec,
        "-b:a", state.audio_bitrate,
        "-ac", "2",
        "-progress", "pipe:1",
        "-nostats",
        output_path
    ]
