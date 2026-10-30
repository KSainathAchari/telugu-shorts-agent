
import os
import re
from pathlib import Path
from google import genai
from gtts import gTTS

api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError("GEMINI_API_KEY is missing")

client = genai.Client(api_key=api_key)

prompt = """
Create one original Telugu moral story for children.

STRICT RULES:
- Story must take about 45 to 60 seconds to narrate.
- Use simple, natural Telugu.
- Main characters: Chintu, a little boy wearing a blue shirt
  and brown shorts; Bujji, a cute white rabbit with pink ears.
- Create exactly 5 scenes.
- Each scene must have:
  SCENE: A short visual description in English.
  NARRATION: One or two short Telugu sentences.
- Keep the same characters in all scenes.
- End with one positive moral in Telugu.
- No introduction, no YouTube description, no hashtags.
- Return only this format:

TITLE: Telugu title

SCENE 1:
VISUAL: English visual description
NARRATION: Telugu narration

Continue until SCENE 5.

MORAL: Telugu moral
"""

print("Generating Telugu cartoon story...")

response = client.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents=prompt
)

story = response.text

if not story:
    raise RuntimeError("Gemini returned an empty story")

# Extract only Telugu narration
narration_parts = re.findall(
    r"NARRATION:\s*(.*)",
    story
)

if len(narration_parts) != 5:
    raise RuntimeError(
        "Story must contain exactly 5 narration scenes"
    )

narration = " ".join(narration_parts)

moral = re.search(r"MORAL:\s*(.*)", story)

if moral:
    narration += " నీతి: " + moral.group(1)

output_dir = Path("stories")
output_dir.mkdir(exist_ok=True)

story_file = output_dir / "latest-story.md"
voice_file = output_dir / "latest-voice.mp3"

story_file.write_text(story, encoding="utf-8")

print("Creating Telugu narration...")

tts = gTTS(text=narration, lang="te")
tts.save(str(voice_file))

print("Story created:", story_file)
print("Telugu voice created:", voice_file)
print("Story generation completed!")
