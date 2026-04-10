import os
import datetime
import requests
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build


def get_youtube_analytics_client():
    creds = Credentials(
        None,
        refresh_token=os.getenv("YOUTUBE_REFRESH_TOKEN"),
        token_uri="https://oauth2.googleapis.com/token",
        client_id=os.getenv("YOUTUBE_CLIENT_ID"),
        client_secret=os.getenv("YOUTUBE_CLIENT_SECRET"),
        scopes=["https://www.googleapis.com/auth/youtube.readonly"]
    )
    return build("youtube", "v3", credentials=creds)


def fetch_video_stats(video_id):
    youtube = get_youtube_analytics_client()

    response = youtube.videos().list(
        part="statistics",
        id=video_id
    ).execute()

    items = response.get("items", [])
    if not items:
        return None

    stats = items[0]["statistics"]

    return {
        "views": int(stats.get("viewCount", 0)),
        "likes": int(stats.get("likeCount", 0)),
        "comments": int(stats.get("commentCount", 0)),
    }


def log_analytics_to_notion(video_id, video_url, stats):
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
            "Name": {"title": [{"text": {"content": f"Analytics: {video_id}"}}]},
            "URL": {"url": video_url},
            "Views": {"number": stats["views"]},
            "Likes": {"number": stats["likes"]},
            "Comments": {"number": stats["comments"]},
            "Checked": {"date": {"start": datetime.datetime.utcnow().isoformat()}},
        }
    }

    requests.post(url, headers=headers, json=payload)


def youtube_analytics_agent(video_id, video_url):
    stats = fetch_video_stats(video_id)
    if not stats:
        print("[Analytics] No stats found for video:", video_id)
        return None

    log_analytics_to_notion(video_id, video_url, stats)
    print("[Analytics] Logged analytics for:", video_url)
    return stats
