from notion_client_wrapper import NotionWrapper


class StatusUpdater:
    """
    Updates Notion task statuses:
    - Pending
    - In Progress
    - Done
    - Failed
    """

    def __init__(self):
        self.notion = NotionWrapper()

    def set_status(self, page_id, status: str):
        valid = ["Pending", "In Progress", "Done", "Failed"]
        if status not in valid:
            print(f"[StatusUpdater] Invalid status: {status}")
            return

        self.notion.set_status(page_id, status)
        print(f"[StatusUpdater] Set {page_id} → {status}")
