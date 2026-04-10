from notion_client_wrapper import NotionWrapper
from youtube_agent import youtube_upload_agent
from vid_agents import HybridAgent  # updated to match your filename

notion = NotionWrapper()
hybrid = HybridAgent()


def process_tasks():
    tasks = notion.get_pending_tasks()

    if not tasks:
        print("No pending tasks.")
        return

    for task in tasks:
        page_id = task["id"]
        props = task["properties"]

        # Safely extract the topic from the Name property
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

        # Run hybrid agent (currently falls back to Simple generator)
        try:
            video_path, script = hybrid.run(topic)
        except Exception as e:
            print(f"Error generating video for '{topic}': {e}")
            continue

        print("Uploading to YouTube...")
        result = youtube_upload_agent(
            video_path,
            topic,
            script
        )

        url = result["video_url"] if result else None

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
