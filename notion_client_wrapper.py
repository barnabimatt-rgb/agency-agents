from notion_client import Client
import os

NOTION_API_KEY = os.getenv("NOTION_API_KEY")
NOTION_DB = os.getenv("NOTION_DB")  # Passive Income HQ DB ID

notion = Client(auth=NOTION_API_KEY)

class NotionWrapper:
    def get_pending_tasks(self):
        response = notion.databases.query(
            **{
                "database_id": NOTION_DB,
                "filter": {
                    "property": "Status",
                    "select": {"equals": "Pending"}
                }
            }
        )
        return response.get("results", [])

    def write_video_url(self, page_id, url):
        notion.pages.update(
            **{
                "page_id": page_id,
                "properties": {
                    "Video URL": {"url": url},
                    "Status": {"select": {"name": "Done"}}
                }
            }
        )
