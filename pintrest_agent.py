import os
import requests


class PinterestAgent:
    """
    Uploads Idea Pins or video pins to Pinterest.
    Requires:
    - PINTEREST_ACCESS_TOKEN
    - PINTEREST_BOARD_ID
    """

    def __init__(self):
        self.token = os.getenv("PINTEREST_ACCESS_TOKEN")
        self.board_id = os.getenv("PINTEREST_BOARD_ID")

    def upload(self, video_path, title, description):
        if not self.token or not self.board_id:
            print("[PinterestAgent] Missing credentials.")
            return None

        url = "https://api.pinterest.com/v5/pins"

        with open(video_path, "rb") as f:
            files = {"media_source": f}
            data = {
                "board_id": self.board_id,
                "title": title,
                "description": description
            }

            resp = requests.post(url, headers={"Authorization": f"Bearer {self.token}"}, files=files, data=data)

        if resp.status_code != 200:
            print("[PinterestAgent] Upload error:", resp.text)
            return None

        pin_id = resp.json().get("id")
        if not pin_id:
            return None

        return f"https://pinterest.com/pin/{pin_id}"
