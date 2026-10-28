
import os
from google import genai

client = genai.Client(
    api_key=os.environ["GEMINI_API_KEY"]
)

prompt = """
Create an original 45-60 second Telugu 3D cartoon story.
Include:
1. An exciting opening
2. Two cartoon characters
3. Simple Telugu narration
4. Three scene descriptions
5. A positive ending and moral

Return the story in Telugu.
"""

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt
)

print(response.text)
