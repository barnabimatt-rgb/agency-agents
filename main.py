import time
import schedule
import requests
import os

from youtube_agent import youtube_upload_agent
from youtube_metadata_agent import (
    generate_youtube_metadata,
    generate_thumbnail
)
from youtube_analytics_agent import youtube_analytics_agent


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
            "tags": [t["name"] for t in props.get("Tags", {}).get("multi_select", [])],
            "video_id": props.get("Video ID", {}).get("rich_text", [{}])[0].get("plain_text", ""),
            "url": props.get("URL", {}).get("url", "")
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

    if task_type == "youtube_analytics":
        return handle_youtube_analytics(task)

    print(f"[Orchestrator] Unknown task type: {task_type}")
    return None


# =========================================================
# 3. HANDLERS (MULTI-AGENT COLLAB)
# =========================================================
def handle_youtube_metadata(task):
    topic = task.get("topic")

    print(f"[YouTube Metadata] Generating metadata for: {topic}")

    title, description, tags = generate_youtube_metadata(topic)
    thumbnail_path = generate_thumbnail(topic, title_for_text=title)

    result = {
        "title": title,
        "description": description,
        "tags": tags,
        "thumbnail_path": thumbnail_path
    }

    print("[YouTube Metadata] Metadata generation complete.")
    return result


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


def handle_youtube_analytics(task):
    video_id = task.get("video_id")
    url = task.get("url")

    if not video_id and url and "v=" in url:
        video_id = url.split("v=")[-1].split("&")[0]

    if not video_id:
        print("[Analytics] No video_id provided.")
        return None

    print(f"[Analytics] Fetching stats for video: {video_id}")
    stats = youtube_analytics_agent(video_id, url or f"https://www.youtube.com/watch?v={video_id}")
    return stats


def handle_youtube_full_auto(task):
    topic = task.get("topic")
    video_path = task.get("video_path")

    print(f"[Full Auto] Starting full YouTube pipeline for: {topic}")

    meta = handle_youtube_metadata({
        "type": "youtube_metadata",
        "topic": topic
    })

    upload = handle_youtube_upload({
        "type": "youtube_upload",
        "video_path": video_path,
        "title": meta["title"],
        "description": meta["description"],
        "tags": meta["tags"]
    })

    analytics = handle_youtube_analytics({
        "type": "youtube_analytics",
        "video_id": upload["video_id"],
        "url": upload["video_url"]
    })

    return {
        "title": meta["title"],
        "description": meta["description"],
        "tags": meta["tags"],
        "thumbnail_path": meta["thumbnail_path"],
        "youtube_url": upload["video_url"],
        "video_id": upload["video_id"],
        "analytics": analytics
    }


# =========================================================
# 4. SCHEDULER
# =========================================================
def scheduled_cycle():
    print("[Scheduler] Checking Notion for tasks...")
    tasks = fetch_tasks_from_notion()

    for task in tasks:
        print(f"[Scheduler] Running task: {task['type']}")
        run_task(task)


def start_scheduler():
    schedule.every(4).hours.do(scheduled_cycle)

    print("[Orchestrator] Scheduler started. Running tasks...")

    while True:
        schedule.run_pending()
        time.sleep(5)


# =========================================================
# 5. ENTRY POINT
# =========================================================
if __name__ == "__main__":
    print("[Orchestrator] Starting service...")
    start_scheduler()
