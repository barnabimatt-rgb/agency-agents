import os
from notion_client import Client


class NotionWrapper:
    """
    Unified Notion wrapper for:
    - Reading tasks
    - Writing URLs
    - Writing repurposed assets
    - Writing product + funnel data
    - Updating statuses
    """

    def __init__(self):
        self.client = Client(auth=os.getenv("NOTION_API_KEY"))
        self.db_id = os.getenv("NOTION_DATABASE_ID")

    # ---------------------------------------------------------
    # Fetch tasks
    # ---------------------------------------------------------
    def get_tasks(self, filter_status=None):
        """
        Returns all tasks, optionally filtered by Status.
        """
        query = {"database_id": self.db_id}

        if filter_status:
            query["filter"] = {
                "property": "Status",
                "select": {"equals": filter_status}
            }

        results = self.client.databases.query(**query)
        return results.get("results", [])

    # ---------------------------------------------------------
    # Write video URLs
    # ---------------------------------------------------------
    def write_video_urls(self, page_id, urls: dict):
        """
        Writes uploaded platform URLs into a 'URLs' rich_text property.
        """
        formatted = "\n".join([f"{k}: {v}" for k, v in urls.items() if v])

        self.client.pages.update(
            page_id=page_id,
            properties={
                "URLs": {
                    "rich_text": [{"text": {"content": formatted}}]
                }
            }
        )

    # ---------------------------------------------------------
    # Write repurposed assets
    # ---------------------------------------------------------
    def write_repurposed_assets(self, page_id, assets: dict):
        """
        Writes repurposed content (threads, posts, newsletter snippets).
        """
        text = ""
        for k, v in assets.items():
            text += f"{k.upper()}:\n{v}\n\n"

        self.client.pages.update(
            page_id=page_id,
            properties={
                "Repurposed": {
                    "rich_text": [{"text": {"content": text}}]
                }
            }
        )

    # ---------------------------------------------------------
    # Write product + funnel
    # ---------------------------------------------------------
    def write_product_and_funnel(self, page_id, product_url, funnel_assets, upsells=None):
        """
        Writes product URL + funnel copy + upsells.
        """
        funnel_text = ""

        funnel_text += f"PRODUCT URL:\n{product_url}\n\n"

        funnel_text += "FUNNEL ASSETS:\n"
        for k, v in funnel_assets.items():
            funnel_text += f"{k.upper()}:\n{v}\n\n"

        if upsells:
            funnel_text += "UPSELLS:\n"
            for u in upsells:
                funnel_text += f"- {u}\n"

        self.client.pages.update(
            page_id=page_id,
            properties={
                "Product/Funnel": {
                    "rich_text": [{"text": {"content": funnel_text}}]
                }
            }
        )

    # ---------------------------------------------------------
    # Update status
    # ---------------------------------------------------------
    def set_status(self, page_id, status: str):
        self.client.pages.update(
            page_id=page_id,
            properties={
                "Status": {"select": {"name": status}}
            }
        )
