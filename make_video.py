
from pathlib import Path
import numpy as np
from PIL import Image, ImageOps, ImageDraw
from moviepy import ImageClip, AudioFileClip, concatenate_videoclips

folder = Path("stories")
image_path = folder / "characters.jpeg"
audio_path = folder / "latest-voice.mp3"
video_path = folder / "latest-short.mp4"

if not image_path.exists():
    raise FileNotFoundError("Missing characters.jpeg")

if not audio_path.exists():
    raise FileNotFoundError("Missing latest-voice.mp3")

audio = AudioFileClip(str(audio_path))
image = Image.open(image_path).convert("RGB")

# Create a vertical background
image = ImageOps.contain(image, (680, 850))
base = Image.new("RGB", (720, 1280), (20, 35, 75))
base.paste(image, ((720-image.width)//2, 170))

# Create 4 scenes with different camera positions
scenes = []
duration = audio.duration / 4

for i in range(4):
    frame = base.copy()
    draw = ImageDraw.Draw(frame)

    titles = [
        "చింటూ కథ",
        "ఒక కొత్త స్నేహం",
        "మంచి పని",
        "నీతి కథ"
    ]

    draw.rounded_rectangle(
        (35, 40, 685, 135),
        radius=25,
        fill=(35, 75, 140)
    )
    draw.text(
        (360, 85),
        titles[i],
        fill="white",
        anchor="mm"
    )

    # Slight zoom effect
    zoom = 1.0 + (i * 0.035)
    w = int(720 * zoom)
    h = int(1280 * zoom)
    zoomed = frame.resize((w, h))

    left = (w - 720) // 2
    top = (h - 1280) // 2
    zoomed = zoomed.crop((left, top, left+720, top+1280))

    clip = ImageClip(np.array(zoomed)).with_duration(duration)
    scenes.append(clip)

video = concatenate_videoclips(scenes, method="compose")
video = video.with_audio(audio)

video.write_videofile(
    str(video_path),
    fps=24,
    codec="libx264",
    audio_codec="aac"
)

audio.close()
video.close()

for scene in scenes:
    scene.close()

print("Multi-scene video created:", video_path)
