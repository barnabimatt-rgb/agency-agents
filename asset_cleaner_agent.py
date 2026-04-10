import os
import time
import shutil


class AssetCleanerAgent:
    """
    Cleans up temporary files to keep Railway storage low.
    This is essential for Hobby tier.
    """

    def __init__(self):
        self.temp_dir = os.getenv("TEMP_DIR", "/app/tmp")
        os.makedirs(self.temp_dir, exist_ok=True)

    def cleanup_temp_files(self, max_age_hours=6):
        """
        Deletes files older than max_age_hours.
        """
        now = time.time()
        cutoff = now - (max_age_hours * 3600)

        removed = 0

        for filename in os.listdir(self.temp_dir):
            path = os.path.join(self.temp_dir, filename)

            try:
                if os.path.isfile(path):
                    if os.path.getmtime(path) < cutoff:
                        os.remove(path)
                        removed += 1
                elif os.path.isdir(path):
                    # Remove old directories
                    if os.path.getmtime(path) < cutoff:
                        shutil.rmtree(path)
                        removed += 1
            except Exception as e:
                print(f"[AssetCleaner] Error removing {path}: {e}")

        print(f"[AssetCleaner] Removed {removed} old temp files.")
