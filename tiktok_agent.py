import os
import requests


class TikTokAgent:
    """
    Uploads videos to TikTok using TikTok's Open API.
    Requires:
    - TIKTOK_ACCESS_TOKEN
    """

    def __init__(self):
        self.access_token = os.getenv("TIKTOK_ACCESS_TOKEN")

    def upload(self, video_path, title, description):
        if not self.access_token:
            print("[TikTokAgent] Missing access token.")
            return None

        upload_url = "https://open.tiktokapis.com/v2/post/publish/video/"

        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }

        with open(video_path, "rb") as f:
            files = {"video": f}
            data = {"title": title}

            resp = requests.post(upload_url, headers=headers, files=files, data=data)

        if resp.status_code != 200:
            print("[TikTokAgent] Upload error:", resp.text)
            return None

        data = resp.json()
        post_id = data.get("data", {}).get("id")

        if not post_id:
            return None

        return f"https://www.tiktok.com/@me/video/{post_id}"
