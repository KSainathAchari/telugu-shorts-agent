
import os
import time
from google import genai

api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError("GEMINI_API_KEY is missing.")

client = genai.Client(api_key=api_key)

prompt = """
Create an original 45-60 second Telugu cartoon story.
Include:
1. An exciting opening
2. Two cartoon characters
3. Simple Telugu narration
4. Three visual scene descriptions
5. A positive ending and moral

Return the title, characters, scenes, Telugu narration,
moral and YouTube description in Telugu.
"""

for attempt in range(3):
    try:
        print(f"Generating story: attempt {attempt + 1}/3")

        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt
        )

        if response.text:
            print("\n--- TELUGU STORY ---\n")
            print(response.text)
            break

        raise RuntimeError("Gemini returned an empty response.")

    except Exception as error:
        print(f"Attempt {attempt + 1} failed: {error}")

        if attempt == 2:
            raise

        time.sleep(5 * (attempt + 1))
        
