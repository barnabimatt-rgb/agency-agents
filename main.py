import time
import schedule
import requests
import os

# -----------------------------
# Agent Imports
# -----------------------------
from youtube_agent import youtube_upload_agent
from youtube_metadata_agent import (
    generate_youtube_metadata,
    generate_thumbnail
)


# =========================================================
# 1. NOTION → TASK INGESTION
# =========================================================
def fetch_tasks_from_notion():
    notion_key = os.getenv("NOTION_API_KEY")
    db_id = os.getenv("NOTION_DATABASE_ID")

    url = f"https://api.notion.com/v1/databases/{db_id}/query"
    headers = {
        "Authorization": f"Bearer {notion_key}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }

    response = requests.post(url, headers=headers).json()
    tasks = []

    for page in response.get("results", []):
        props = page["properties"]

        if "Type" not in props or props["Type"]["select"] is None:
            continue

        task_type = props["Type"]["select"]["name"]

        task = {
            "id": page["id"],
            "type": task_type,
            "topic": props.get("Topic", {}).get("rich_text", [{}])[0].get("plain_text", ""),
            "video_path": props.get("Video Path", {}).get("rich_text", [{}])[0].get("plain_text", ""),
            "title": props.get("Title", {}).get("rich_text", [{}])[0].get("plain_text", ""),
            "description": props.get("Description", {}).get("rich_text", [{}])[0].get("plain_text", ""),
            "tags": [t["name"] for t in props.get("Tags", {}).get("multi_select", [])]
        }

        tasks.append(task)

    return tasks


# =========================================================
# 2. TASK ROUTER
# =========================================================
def run_task(task):
    task_type = task.get("type")

    if task_type == "youtube_metadata":
        return handle_youtube_metadata(task)

    if task_type == "youtube_upload":
        return handle_youtube_upload(task)

    if task_type == "youtube_full_auto":
        return handle_youtube_full_auto(task)

    print(f"[Orchestrator] Unknown task type: {task_type}")
    return None


# =========================================================
# 3. HANDLERS
# =========================================================

# -----------------------------
# Auto Title / Description / Thumbnail
# -----------------------------
def handle_youtube_metadata(task):
    topic = task.get("topic")

    print(f"[YouTube Metadata] Generating metadata for: {topic}")

    title, description = generate_youtube_metadata(topic)
    thumbnail_path = generate_thumbnail(topic)

    result = {
        "title": title,
        "description": description,
        "thumbnail_path": thumbnail_path
    }

    print("[YouTube Metadata] Metadata generation complete.")
    return result


# -----------------------------
# YouTube Upload
# -----------------------------
def handle_youtube_upload(task):
    video_path = task.get("video_path")
    title = task.get("title")
    description = task.get("description")
    tags = task.get("tags", [])

    print(f"[YouTube] Uploading video: {title}")

    result = youtube_upload_agent(
        video_path=video_path,
        title=title,
        description=description,
        tags=tags
    )

    print(f"[YouTube] Upload complete: {result['video_url']}")
    return result


# -----------------------------
# Full Auto Pipeline (Metadata → Upload)
# -----------------------------
def handle_youtube_full_auto(task):
    topic = task.get("topic")
    video_path = task.get("video_path")

    print(f"[Full Auto] Starting full YouTube pipeline for: {topic}")

    # Step 1: Metadata
    meta = handle
