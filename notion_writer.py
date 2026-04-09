import os
import logging
from notion_client import Client

logger = logging.getLogger(__name__)

NOTION_API_KEY = os.getenv("NOTION_API_KEY")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

notion = Client(auth=NOTION_API_KEY)


def log_entry(title: str, item_type: str, status: str, notes: str):
    logger.info(f"📝 Logging to Notion: {title} ({item_type})")

    notion.pages.create(
        parent={"database_id": NOTION_DATABASE_ID},
        properties={
            "Name": {"title": [{"text": {"content": title}}]},
            "Type": {"select": {"name": item_type}},
            "Status": {"select": {"name": status}},
        },
        children=[
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {"content": notes[:1900]},
                        }
                    ]
                },
            }
        ],
    )

    logger.info("✅ Logged to Notion.")
