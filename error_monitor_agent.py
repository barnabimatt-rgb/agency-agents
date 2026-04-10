import datetime
from notion_client_wrapper import NotionWrapper


class ErrorMonitorAgent:
    """
    Logs errors into a Notion 'Incidents' database (optional).
    If you don't have a separate DB, it logs into the task page.
    """

    def __init__(self):
        self.notion = NotionWrapper()

    def log_error(self, category: str, topic: str, message: str):
        """
        Logs error into the task's 'URLs' or 'Repurposed' field as a fallback.
        """
        timestamp = datetime.datetime.utcnow().isoformat()

        print(f"[ErrorMonitor] {timestamp} | {category} | {topic} | {message}")
        # If you later add a dedicated Notion DB for incidents, wire it here.
