
from pathlib import Path
import numpy as np
from PIL import Image
from moviepy import (
    ImageClip,
    AudioFileClip,
    CompositeVideoClip,
    concatenate_videoclips
)

folder = Path("stories")
image_path = folder / "characters.jpeg"
audio_path = folder / "latest-voice.mp3"
video_path = folder / "latest-short.mp4"

if not image_path.exists():
    raise FileNotFoundError("characters.jpeg not found")

if not audio_path.exists():
    raise FileNotFoundError("latest-voice.mp3 not found")

# Open the character/story image
image = Image.open(image_path).convert("RGB")

# Crop the three story panels from the bottom
panels = [
    image.crop((10, 565, 412, 1235)),
    image.crop((421, 565, 827, 1235)),
    image.crop((837, 565, 1238, 1235))
]

audio = AudioFileClip(str(audio_path))

# Five shots using the three available story panels
scene_order = [0, 1, 2, 1, 2]
scene_duration = audio.duration / len(scene_order)

clips = []

for index in scene_order:
    panel = panels[index]

    # Fit image to vertical 9:16 format
    panel = panel.resize((720, 1200))

    canvas = Image.new("RGB", (720, 1280), (20, 35, 65))
    canvas.paste(panel, (0, 40))

    frame = np.array(canvas)

    clip = ImageClip(frame).with_duration(scene_duration)

    # Gentle camera zoom
    clip = clip.resized(
        lambda t: 1 + 0.04 * t
    )

    scene = CompositeVideoClip(
        [clip.with_position("center")],
        size=(720, 1280)
    ).with_duration(scene_duration)

    clips.append(scene)

video = concatenate_videoclips(clips, method="compose")
video = video.with_audio(audio)

video.write_videofile(
    str(video_path),
    fps=24,
    codec="libx264",
    audio_codec="aac",
    preset="ultrafast"
)

audio.close()
video.close()

print("Telugu story video created:", video_path)
    
