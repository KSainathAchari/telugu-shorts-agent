
from pathlib import Path
import numpy as np
from PIL import Image, ImageOps
from moviepy import ImageClip, AudioFileClip

folder = Path("stories")
image_path = folder / "characters.jpeg"
audio_path = folder / "latest-voice.mp3"
video_path = folder / "latest-short.mp4"

if not image_path.exists():
    raise FileNotFoundError("Missing stories/characters.jpeg")

if not audio_path.exists():
    raise FileNotFoundError("Missing stories/latest-voice.mp3")

# Create a vertical 9:16 background
image = Image.open(image_path).convert("RGB")
image = ImageOps.contain(image, (700, 900))

canvas = Image.new("RGB", (720, 1280), (25, 40, 90))
x = (720 - image.width) // 2
y = (1280 - image.height) // 2
canvas.paste(image, (x, y))

frame = np.array(canvas)

audio = AudioFileClip(str(audio_path))
video = ImageClip(frame).with_duration(audio.duration)
video = video.with_audio(audio)

video.write_videofile(
    str(video_path),
    fps=24,
    codec="libx264",
    audio_codec="aac"
)

audio.close()
video.close()

print("Video created:", video_path)
