def validate_state(state):
    if state.resolution not in [1440, 1080, 720, 480]:
        raise ValueError("Invalid resolution")

    if state.video_codec == "libx264" and state.pixel_format == "yuv420p10le":
        raise ValueError("x264 10bit unsupported")

    return True
