import time
import schedule
from youtube_agent import youtube_upload_agent


# ---------------------------------------------------------
# 1. Task Router
# ---------------------------------------------------------
def run_task(task):
    task_type = task.get("type")

    if task_type == "youtube_upload":
        return handle_youtube_upload(task)

    print(f"[Orchestrator] Unknown task type: {task_type}")
    return None


# ---------------------------------------------------------
# 2. YouTube Upload Handler
# ---------------------------------------------------------
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


# ---------------------------------------------------------
# 3. Example Scheduled YouTube Job (optional)
# ---------------------------------------------------------
def scheduled_youtube_job():
    task = {
        "type": "youtube_upload",
        "video_path": "output/video.mp4",
        "title": "Automated Upload",
        "description": "Uploaded automatically by the orchestrator.",
        "tags": ["automation", "ai"]
    }
    run_task(task)


# ---------------------------------------------------------
# 4. Scheduler Loop (Railway-safe)
# ---------------------------------------------------------
def start_scheduler():
    # Example: run every 4 hours (your preferred cadence)
    schedule.every(4).hours.do(scheduled_youtube_job)

    print("[Orchestrator] Scheduler started. Running tasks...")

    while True:
        schedule.run_pending()
        time.sleep(5)


# ---------------------------------------------------------
# 5. Entry Point
# ---------------------------------------------------------
if __name__ == "__main__":
    print("[Orchestrator] Starting service...")
    start_scheduler()
