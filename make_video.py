
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw
from moviepy import ImageClip, AudioFileClip, concatenate_videoclips

folder = Path("stories")
audio_path = folder / "latest-voice.mp3"
video_path = folder / "latest-short.mp4"

if not audio_path.exists():
    raise FileNotFoundError("Missing stories/latest-voice.mp3")

scenes = [
    ("చింటూ మరియు బుజ్జి", "ఒక అందమైన కథ"),
    ("మాయా పెన్", "సహాయం చేసే అద్భుతం"),
    ("మంచి మనసు", "సహాయమే నిజమైన ఆనందం"),
]

audio = AudioFileClip(str(audio_path))
clips = []

def make_scene(title, subtitle, duration):
    image = Image.new("RGB", (720, 1280), (25, 40, 90))
    draw = ImageDraw.Draw(image)

    draw.rounded_rectangle(
        (40, 300, 680, 900),
        radius=40,
        fill=(255, 210, 90)
    )

    draw.text((75, 480), title, fill=(20, 30, 70))
    draw.text((75, 620), subtitle, fill=(20, 30, 70))

    # Convert PIL image to a NumPy array for MoviePy
    frame = np.array(image)

    return ImageClip(frame).with_duration(duration)

duration = audio.duration / len(scenes)

for title, subtitle in scenes:
    clips.append(make_scene(title, subtitle, duration))

video = concatenate_videoclips(clips, method="compose")
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
