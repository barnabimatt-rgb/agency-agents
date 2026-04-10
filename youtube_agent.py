import os
import datetime
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import requests


# ---------------------------------------------------------
# 1. Build YouTube API client using refresh token
# ---------------------------------------------------------
def get_youtube_client():
    creds = Credentials(
        None,
        refresh_token=os.getenv("YOUTUBE_REFRESH_TOKEN"),
        token_uri="https://oauth2.googleapis.com/token",
        client_id=os.getenv("YOUTUBE_CLIENT_ID"),
        client_secret=os.getenv("YOUTUBE_CLIENT_SECRET"),
        scopes=["https://www.googleapis.com/auth/youtube.upload"]
    )
    return build("youtube", "v3", credentials=creds)


# ---------------------------------------------------------
# 2. Upload video to YouTube
# ---------------------------------------------------------
def upload_to_youtube(video_path, title, description, tags=None, category_id="22", privacy="public"):
    youtube = get_youtube_client()

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


# ---------------------------------------------------------
# 3. Log upload to Notion (matches your schema)
# ---------------------------------------------------------
def log_to_notion(video_data):
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


# ---------------------------------------------------------
# 4. Main agent function
# ---------------------------------------------------------
def youtube_upload_agent(video_path, title, description, tags=None):
    print("Uploading to YouTube...")
    result = upload_to_youtube(video_path, title, description, tags)

    print("Logging to Notion...")
    log_to_notion(result)

    print("Upload complete.")
    return result
