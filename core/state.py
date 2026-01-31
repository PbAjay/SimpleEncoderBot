class EncodeState:
    """
    Represents one user's full encoding intent.
    NOTHING is assumed.
    """

    def __init__(self, message):
        self.source_message = message

        self.upload_mode = "media"
        self.resolution = 720

        self.video_codec = "libx265"
        self.pixel_format = "yuv420p10le"
        self.crf = 23

        self.audio_codec = "aac"
        self.audio_bitrate = "192k"

    def as_dict(self):
        return {
            "upload_mode": self.upload_mode,
            "resolution": self.resolution,
            "video_codec": self.video_codec,
            "pixel_format": self.pixel_format,
            "crf": self.crf,
            "audio_codec": self.audio_codec,
            "audio_bitrate": self.audio_bitrate
        }
