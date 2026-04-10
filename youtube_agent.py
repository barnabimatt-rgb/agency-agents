import os
import datetime
import requests
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request


class YouTubeAgent:
    """
    Wrapper around your existing OAuth-based YouTube uploader.
    Fully compatible with the new multi-agent architecture.
    """

    def __init__(self):
        self.refresh_token = os.getenv("YOUTUBE_REFRESH_TOKEN")
        self.client_id = os.getenv("YOUTUBE_CLIENT_ID")
        self.client_secret = os.getenv("YOUTUBE_CLIENT_SECRET")
        self.notion_key = os.getenv("NOTION_API_KEY")
        self.notion_db = os.getenv("NOTION_LOG_DB")

    # ---------------------------------------------------------
    # YouTube OAuth Client
    # ---------------------------------------------------------
    def get_youtube_client(self):
        print("REFRESH TOKEN LOADED:", self.refresh_token)

        if not self.refresh_token or not self.client_id or not self.client_secret:
            print("❌ Missing YouTube OAuth environment variables.")
            return None

        creds = Credentials(
            None,
            refresh_token=self.refresh_token,
            token_uri="https://oauth2.googleapis.com/token",
            client_id=self.client_id,
            client_secret=self.client_secret,
            scopes=["https://www.googleapis.com/auth/youtube.upload"]
        )

        try:
            creds.refresh(Request())
        except Exception as e:
            print("❌ Failed to refresh YouTube token:", e)
            return None

        return build("youtube", "v3", credentials=creds)

    # ---------------------------------------------------------
    # Upload to YouTube
    # ---------------------------------------------------------
    def upload(self, video_path, title, description, tags=None):
        youtube = self.get_youtube_client()

        if youtube is None:
            print("❌ YouTube client not initialized — upload aborted.")
            return None

        body = {
            "snippet": {
                "title": title,
                "description": description,
                "tags": tags or [],
                "categoryId": "22"
            },
            "status": {
                "privacyStatus": "public"
            }
        }

        media = MediaFileUpload(video_path, chunksize=-1, resumable=True)

        try:
            request = youtube.videos().insert(
                part="snippet,status",
                body=body,
                media_body=media
            )

            response = None
            while response is None:
                status, response = request.next_chunk()

            video_id = response["id"]
            video_url = f"https://www.youtube.com/watch?v={video_id}"

            # Log to Notion
            self.log_to_notion({
                "video_id": video_id,
                "video_url": video_url,
                "title": title,
                "description": description
            })

            return video_url

        except Exception as e:
            print("❌ Upload failed:", e)
            return None

    # ---------------------------------------------------------
    # Log to Notion
    # ---------------------------------------------------------
    def log_to_notion(self, video_data):
        if video_data is None:
            print("❌ No video data to log — skipping Notion.")
            return

        url = "https://api.notion.com/v1/pages"
        headers = {
            "Authorization": f"Bearer {self.notion_key}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }

        payload = {
            "parent": {"database_id": self.notion_db},
            "properties": {
                "Name": {"title": [{"text": {"content": video_data["title"]}}]},
                "URL": {"url": video_data["video_url"]},
                "Uploaded": {"date": {"start": datetime.datetime.utcnow().isoformat()}},
            }
        }

        requests.post(url, headers=headers, json=payload)
