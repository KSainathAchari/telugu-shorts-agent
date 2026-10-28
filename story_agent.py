import os
from pathlib import Path
from google import genai

api_key = os.environ.get("GEMINI_API_KEY")

if not api_key: raise RuntimeError("GEMINI_API_KEY is missing.")

client = genai.Client(api_key=api_key)

prompt = """
Create an original 45-60 second Telugu 3D cartoon moral story.
Include two characters, three visual scenes, simple Telugu narration,
a positive ending, a moral, a YouTube description and hashtags.
Write the story in Telugu.
"""

print("Generating Telugu story...")

response = client.models.generate_content(
model="gemini-3.5-flash-lite",
contents=prompt
)

story = response.text

if not story: raise RuntimeError("Gemini returned an empty response.")

output_dir = Path("stories")
output_dir.mkdir(parents=True, exist_ok=True)

output_file = output_dir / "latest-story.md"
output_file.write_text(story, encoding="utf-8")

print("\n--- TELUGU STORY ---\n")
print(story)
print("\nStory saved to:", output_file)
