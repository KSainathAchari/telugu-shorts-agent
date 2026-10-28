
import os
from pathlib import Path
from google import genai
from gtts import gTTS

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("GEMINI_API_KEY is missing.")

client = genai.Client(api_key=api_key)

prompt = """
Create an original 45-60 second Telugu 3D cartoon moral story.
Include two characters, three visual scenes, simple Telugu narration,
a positive ending, a moral, a YouTube description and hashtags.
Write everything in Telugu.
"""

print("Generating Telugu story...")

response = client.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents=prompt
)

story = response.text
if not story:
    raise RuntimeError("Gemini returned an empty response.")

output_dir = Path("stories")
output_dir.mkdir(parents=True, exist_ok=True)

story_file = output_dir / "latest-story.md"
story_file.write_text(story, encoding="utf-8")

# Extract narration for voice generation
narration = story
for marker in ["YouTube description", "యూట్యూబ్ వివరణ", "Hashtags", "హ్యాష్‌ట్యాగ్స్"]:
    narration = narration.split(marker)[0]

# Remove common scene headings and markdown formatting
lines = []
for line in narration.splitlines():
    clean = line.strip()
    if clean and not clean.startswith("#") and not clean.startswith("---"):
        lines.append(clean.replace("**", "").replace("*", ""))

narration = " ".join(lines)

print("Creating Telugu voice...")

tts = gTTS(text=narration, lang="te")
audio_file = output_dir / "latest-voice.mp3"
tts.save(str(audio_file))

print("Story saved:", story_file)
print("Voice saved:", audio_file)
