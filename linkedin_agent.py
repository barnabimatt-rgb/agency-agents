import os
import requests


class LinkedInAgent:
    """
    Uploads native videos to LinkedIn.
    Requires:
    - LINKEDIN_ACCESS_TOKEN
    - LINKEDIN_URN (your user or organization URN)
    """

    def __init__(self):
        self.token = os.getenv("LINKEDIN_ACCESS_TOKEN")
        self.urn = os.getenv("LINKEDIN_URN")

    def upload(self, video_path, title, description):
        if not self.token or not self.urn:
            print("[LinkedInAgent] Missing credentials.")
            return None

        # Placeholder — LinkedIn requires multi-step upload
        print("[LinkedInAgent] Upload stub — implement multi-step upload here.")
        return None
