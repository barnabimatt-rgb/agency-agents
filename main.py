from notion_client_wrapper import NotionWrapper
from topic_agent import TopicAgent
from youtube_agent import youtube_upload_agent
from vid_agents import HybridAgent  # your video generator

notion = NotionWrapper()
topics = TopicAgent()
hybrid = HybridAgent()


def process_tasks():
    # STEP 1 — Auto-generate new topics
    print("Generating new content topics...")
    topics.run(n=3)

    # STEP 2 — Fetch pending tasks from Notion
    tasks = notion.get_pending_tasks()

    if not tasks:
        print("No pending tasks.")
        return

    # STEP 3 — Process each task
    for task in tasks:
        page_id = task["id"]
        props = task["properties"]

        # Extract topic from Notion
        name_prop = props.get("Name", {})
        title_array = name_prop.get("title", [])
        if not title_array:
            print(f"Skipping page {page_id}: no Name title text.")
            continue

        topic = title_array[0].get("plain_text", "").strip()
        if not topic:
            print(f"Skipping page {page_id}: empty Name text.")
            continue

        print(f"Generating video for: {topic}")

        # STEP 4 — Generate video using HybridAgent
        try:
            video_path, script = hybrid.run(topic)
        except Exception as e:
            print(f"Error generating video for '{topic}': {e}")
            continue

        # STEP 5 — Upload to YouTube
        print("Uploading to YouTube...")
        result = youtube_upload_agent(
            video_path,
            topic,
            script
        )

        url = result["video_url"] if result else None

        # STEP 6 — Log result to Notion
        if url:
            try:
                notion.write_video_url(page_id, url)
                print(f"Uploaded and logged URL: {url}")
            except Exception as e:
                print(f"Video uploaded but failed to write URL to Notion: {e}")
        else:
            print("Upload failed, not updating Notion.")


if __name__ == "__main__":
    process_tasks()
