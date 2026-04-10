import os
import datetime
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import requests


def get_youtube_client():
    # DEBUG: Check if Railway actually loaded the refresh token
    print("REFRESH TOKEN LOADED:", os.getenv("YOUTUBE_REFRESH_TOKEN"))

    refresh_token = os.getenv("YOUTUBE_REFRESH_TOKEN")
    client_id = os.getenv("YOUTUBE_CLIENT_ID")
    client_secret = os.getenv("YOUTUBE_CLIENT_SECRET")

    if not refresh_token or not client_id or not client_secret:
        print("❌ Missing YouTube OAuth environment variables.")
        return None

    creds = Credentials(
        None,
        refresh_token=refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=client_id,
        client_secret=client_secret,
        scopes=["https://www.googleapis.com/auth/youtube.upload"]
    )

    # Attempt to refresh the access token
    try:
        creds.refresh(requests.Request())
    except Exception as e:
        print("❌ Failed to refresh YouTube token:", e)
        return None

    return build("youtube", "v3", credentials=creds)


def upload_to_youtube(video_path, title, description, tags=None, category_id="22", privacy="public"):
    youtube = get_youtube_client()

    if youtube is None:
        print("❌ YouTube client not initialized — upload aborted.")
        return None

    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags or [],
            "categoryId": category_id
        },
        "status": {
            "privacyStatus": privacy
        }
    }

    media = MediaFileUpload(video_path, chunks
