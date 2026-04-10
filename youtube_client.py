import os
import requests

YOUTUBE_UPLOAD_URL = "https://www.googleapis.com/upload/youtube/v3/videos"
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
YOUTUBE_ACCESS_TOKEN = os.getenv("YOUTUBE_ACCESS_TOKEN")

class YouTubeClient:
    def upload_video(self, filepath, title, description):
        headers = {
            "Authorization": f"Bearer {YOUTUBE_ACCESS_TOKEN}",
            "Content-Type": "application/octet-stream"
        }

        params = {
            "part": "snippet,status"
        }

        snippet = {
            "snippet": {
                "title": title,
                "description": description
            },
            "status": {"privacyStatus": "public"}
        }

        upload = requests.post(
            YOUTUBE_UPLOAD_URL,
            headers=headers,
            params=params,
            data=open(filepath, "rb")
        )

        if upload.status_code not in [200, 201]:
            print("Upload failed:", upload.text)
            return None

        video_id = upload.json()["id"]
        return f"https://youtube.com/watch?v={video_id}"
