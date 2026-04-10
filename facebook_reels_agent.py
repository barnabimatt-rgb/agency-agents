import os
import requests


class FacebookReelsAgent:
    """
    Uploads Reels to Facebook Pages.
    Requires:
    - FB_PAGE_ID
    - FB_PAGE_ACCESS_TOKEN
    """

    def __init__(self):
        self.page_id = os.getenv("FB_PAGE_ID")
        self.token = os.getenv("FB_PAGE_ACCESS_TOKEN")

    def upload(self, video_path, title, description):
        if not self.page_id or not self.token:
            print("[FacebookReelsAgent] Missing credentials.")
            return None

        upload_url = f"https://graph.facebook.com/v18.0/{self.page_id}/video_reels"

        with open(video_path, "rb") as f:
            files = {"video_file": f}
            data = {
                "description": f"{title}\n\n{description}",
                "access_token": self.token
            }

            resp = requests.post(upload_url, files=files, data=data)

        if resp.status_code != 200:
            print("[FacebookReelsAgent] Upload error:", resp.text)
            return None

        video_id = resp.json().get("id")
        if not video_id:
            return None

        return f"https://facebook.com/reel/{video_id}"
