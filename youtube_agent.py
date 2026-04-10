import os
import datetime
import requests
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request


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

    # Correct refresh call
    try:
        creds.refresh(Request())
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

        return {
            "video_id": video_id,
            "video_url": video_url,
            "title": title,
            "description": description
        }

    except Exception as e:
        print("❌ Upload failed:", e)
        return None


def log_to_notion(video_data):
    if video_data is None:
        print("❌ No video data to log — skipping Notion.")
        return

    notion_key = os.getenv("NOTION_API_KEY")
    db_id = os.getenv("NOTION_LOG_DB")

    url = "https://api.notion.com/v1/pages"
    headers = {
        "Authorization": f"Bearer {notion_key}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }

    payload = {
        "parent": {"database_id": db_id},
        "properties": {
            "Name": {"title": [{"text": {"content": video_data["title"]}}]},
            "URL": {"url": video_data["video_url"]},
            "Uploaded": {"date": {"start": datetime.datetime.utcnow().isoformat()}},
        }
    }

    requests.post(url, headers=headers, json=payload)


def youtube_upload_agent(video_path, title, description, tags=None):
    print("Uploading to YouTube...")
    result = upload_to_youtube(video_path, title, description, tags)

    if result:
        print("Logging to Notion...")
        log_to_notion(result)
        print("Upload complete.")
    else:
        print("Upload failed, not updating Notion.")

    return result
