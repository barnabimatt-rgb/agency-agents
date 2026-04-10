import os
import random
from typing import Dict, Any

import requests


class MediaResolver:
    """
    Resolves media for actions produced by ScriptParser.

    Implements Option D:
    - 80% stock B-roll (Pexels)
    - 20% AI-generated clips (placeholder hook for Runway/Pika/etc.)

    For now, AI clip generation is a stub you can wire later.
    """

    def __init__(self):
        self.pexels_api_key = os.getenv("PEXELS_API_KEY")
        self.temp_dir = os.getenv("TEMP_DIR", "/app/tmp")

        os.makedirs(self.temp_dir, exist_ok=True)

    def _download_file(self, url: str, suffix: str) -> str:
        resp = requests.get(url, stream=True)
        resp.raise_for_status()

        path = os.path.join(self.temp_dir, f"clip_{random.randint(100000, 999999)}{suffix}")
        with open(path, "wb") as f:
            for chunk in resp.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        return path

    def _resolve_pexels_broll(self, query: str) -> str | None:
        """
        Use Pexels video API to get a short clip for the query.
        """
        if not self.pexels_api_key:
            print("PEXELS_API_KEY not set, cannot fetch stock B-roll.")
            return None

        headers = {"Authorization": self.pexels_api_key}
        params = {
            "query": query,
            "per_page": 5,
            "orientation": "portrait",
            "size": "medium",
        }

        resp = requests.get("https://api.pexels.com/videos/search", headers=headers, params=params)
        if resp.status_code != 200:
            print(f"Pexels API error: {resp.status_code} {resp.text}")
            return None

        data = resp.json()
        videos = data.get("videos", [])
        if not videos:
            print(f"No Pexels videos found for query: {query}")
            return None

        # Pick a random video, then pick the shortest file
        video = random.choice(videos)
        files = video.get("video_files", [])
        if not files:
            return None

        # Prefer vertical-ish, smaller resolution
        files_sorted = sorted(files, key=lambda f: (abs((f.get("width", 0) / max(f.get("height", 1), 1)) - 9/16), f.get("width", 9999)))
        chosen = files_sorted[0]
        url = chosen.get("link")
        if not url:
            return None

        return self._download_file(url, ".mp4")

    def _resolve_ai_clip(self, description: str) -> str | None:
        """
        Placeholder for AI video generation (Runway/Pika/etc.).
        For now, just returns None so the caller can fall back to stock.
        """
        print(f"[AI CLIP STUB] Would generate AI clip for: {description}")
        return None

    def resolve_broll(self, description: str) -> str | None:
        """
        Resolve a B-roll clip using hybrid strategy:
        - 80% chance: Pexels stock
        - 20% chance: AI clip (stubbed)
        """
        use_ai = random.random() < 0.2

        if use_ai:
            path = self._resolve_ai_clip(description)
            if path:
                return path

        # Fallback or default: Pexels
        return self._resolve_pexels_broll(description)

    def resolve_music(self, mode: str, description: str) -> Dict[str, Any]:
        """
        Stub for music resolution. In practice, you'd map 'energetic', 'dark', etc.
        to local tracks or a small curated library.
        """
        # For now, just return a tag; VideoAssembler will pick a track.
        return {
            "type": "music",
            "mode": mode,
            "description": description,
        }

    def resolve_sfx(self, description: str) -> Dict[str, Any]:
        """
        Stub for SFX resolution. Map 'whoosh', 'impact', etc. to local files.
        """
        return {
            "type": "sfx",
            "description": description,
        }
