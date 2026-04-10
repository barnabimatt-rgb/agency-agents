import os
import requests


class InstagramAgent:
    """
    Uploads Reels to Instagram via the Facebook Graph API.
    Requires:
    - IG_ACCESS_TOKEN
    - IG_USER_ID
    """

    def __init__(self):
        self.token = os.getenv("IG_ACCESS_TOKEN")
        self.user_id = os.getenv("IG_USER_ID")

    def upload(self, video_path, title, description):
        if not self.token or not self.user_id:
            print("[InstagramAgent] Missing credentials.")
            return None

        # Step 1: Upload container
        upload_url = f"https://graph.facebook.com/v18.0/{self.user_id}/media"

        with open(video_path, "rb") as f:
            files = {"video_file": f}
            data = {
                "media_type": "REELS",
                "caption": f"{title}\n\n{description}",
                "access_token": self.token
            }

            resp = requests.post(upload_url, files=files, data=data)

        if resp.status_code != 200:
            print("[InstagramAgent] Upload error:", resp.text)
            return None

        container_id = resp.json().get("id")
        if not container_id:
            return None

        # Step 2: Publish
        publish_url = f"https://graph.facebook.com/v18.0/{self.user_id}/media_publish"
        publish = requests.post(publish_url, data={"creation_id": container_id, "access_token": self.token})

        if publish.status_code != 200:
            print("[InstagramAgent] Publish error:", publish.text)
            return None

        return f"https://instagram.com/reel/{container_id}"
