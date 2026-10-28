
import os
from google import genai
from google.genai import errors

api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError(
        "GEMINI_API_KEY is missing from GitHub Secrets."
    )

client = genai.Client(api_key=api_key)

prompt = """
Create an original 45-60 second Telugu 3D cartoon story.

Requirements:
1. Start with an exciting hook.
2. Include two cartoon characters.
3. Write natural, simple Telugu narration.
4. Describe three visual scenes.
5. End with a positive twist and moral.
6. Keep the narration suitable for a 45-60 second video.

Return:
TITLE:
CHARACTERS:
SCENE 1:
SCENE 2:
SCENE 3:
TELUGU NARRATION:
MORAL:
YOUTUBE DESCRIPTION:
"""

try:
    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=prompt
    )

    if response.text:
        print(response.text)
    else:
        raise RuntimeError("Gemini returned an empty response.")

except errors.APIError as e:
    print(f"Gemini API error: {e}")
    raise
    
