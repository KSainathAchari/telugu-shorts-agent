
import os
from pathlib import Path
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

def main():
    video_file = Path("stories/latest-short.mp4")

    if not video_file.exists():
        raise FileNotFoundError("Video not found: stories/latest-short.mp4")

    refresh_token = os.environ["YOUTUBE_REFRESH_TOKEN"]
    client_id = os.environ["YOUTUBE_CLIENT_ID"]
    client_secret = os.environ["YOUTUBE_CLIENT_SECRET"]

    credentials = Credentials(
        token=None,
        refresh_token=refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=client_id,
        client_secret=client_secret,
        scopes=["https://www.googleapis.com/auth/youtube.upload"],
    )
    credentials.refresh(Request())

    youtube = build("youtube", "v3", credentials=credentials)

    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": "Telugu Cartoon Story | Chintu & Bujji #Shorts",
                "description": "An original Telugu cartoon story for learning and fun. #TeluguStories #Shorts",
                "tags": ["TeluguStories", "CartoonStories", "Shorts"],
                "categoryId": "27",
            },
            "status": {"privacyStatus": "private"},
        },
        media_body=MediaFileUpload(
            str(video_file),
            mimetype="video/mp4",
            resumable=True,
        ),
    )

    result = request.execute()
    print("Upload successful. Video ID:", result["id"])

if __name__ == "__main__":
    main()
  
