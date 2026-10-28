
from pathlib import Path
from PIL import Image, ImageDraw
from moviepy import ImageClip, AudioFileClip, concatenate_videoclips

folder = Path("stories")
audio_path = folder / "latest-voice.mp3"
video_path = folder / "latest-short.mp4"

if not audio_path.exists():
    raise FileNotFoundError("Missing stories/latest-voice.mp3")

# Make three colourful cartoon-style scene cards
scenes = [
    ("చింటూ మరియు బుజ్జి", "ఒక అందమైన కథ"),
    ("మాయా పెన్", "సహాయం చేసే అద్భుతం"),
    ("మంచి మనసు", "సహాయమే నిజమైన ఆనందం"),
]

clips = []

for title, subtitle in scenes:
    image = Image.new("RGB", (720, 1280), (25, 40, 90))
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((45, 300, 675, 900), radius=40,
                           fill=(255, 210, 90))
    draw.text((85, 480), title, fill=(20, 30, 70), spacing=20)
    draw.text((85, 620), subtitle, fill=(20, 30, 70))
    clips.append(ImageClip(image).with_duration(5))

audio = AudioFileClip(str(audio_path))
total = audio.duration
durations = [total / 3] * 3

clips = []
for (title, subtitle), duration in zip(scenes, durations):
    image = Image.new("RGB", (720, 1280), (25, 40, 90))
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((45, 300, 675, 900), radius=40,
                           fill=(255, 210, 90))
    draw.text((85, 480), title, fill=(20, 30, 70))
    draw.text((85, 620), subtitle, fill=(20, 30, 70))
    clips.append(ImageClip(image).with_duration(duration))

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
  
