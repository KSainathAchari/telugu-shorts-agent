import os
import time
from pathlib import Path
from google import genai

Read the API key from GitHub Secrets

api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
raise RuntimeError("GEMINI_API_KEY is missing.")

Connect to Gemini

client = genai.Client(api_key=api_key)

Story generation prompt

prompt = """
Create an original 45-60 second Telugu cartoon story.

Include:

1. An exciting opening
2. Two cartoon characters
3. Simple Telugu narration
4. Three visual scene descriptions
5. A positive ending and moral
6. A YouTube description and hashtags

Return the title, characters, scenes, Telugu narration,
moral, and YouTube description in Telugu.
"""

Generate the story with retries

for attempt in range(3):
try:
print(f"Generating story: attempt {attempt + 1}/3")

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    if not response.text:
        raise RuntimeError("Gemini returned an empty response.")

    story = response.text

    # Create the stories folder
    output_dir = Path("stories")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Save the generated story
    output_file = output_dir / "latest-story.md"
    output_file.write_text(story, encoding="utf-8")

    # Display the result
    print("\n--- TELUGU STORY ---\n")
    print(story)
    print(f"\nStory saved to: {output_file}")

    break

except Exception as error:
    print(f"Attempt {attempt + 1} failed: {error}")

    if attempt == 2:
        raise

    wait_seconds = 5 * (attempt + 1)
    print(f"Retrying in {wait_seconds} seconds...")
    time.sleep(wait_seconds)
