import datetime
from notion_client_wrapper import NotionWrapper


class SchedulerAgent:
    """
    Determines which tasks should run right now.
    Simple version:
    - Runs tasks with Status = Pending
    - Future upgrade: add scheduled timestamps, time windows, batching, etc.
    """

    def __init__(self):
        self.notion = NotionWrapper()

    def get_tasks_to_run(self, notion=None):
        """
        Returns tasks with Status = Pending.
        """
        if notion:
            wrapper = notion
        else:
            wrapper = self.notion

        tasks = wrapper.get_tasks(filter_status="Pending")
        return tasks
