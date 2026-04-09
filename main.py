import os
import time
import logging
from datetime import datetime, timedelta

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

NOTION_API_KEY = os.getenv("NOTION_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
TIKTOK_API_KEY = os.getenv("TIKTOK_API_KEY")
INSTAGRAM_TOKEN = os.getenv("INSTAGRAM_TOKEN")
TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")

GUMROAD_API_KEY = os.getenv("GUMROAD_API_KEY")
ETSY_API_KEY = os.getenv("ETSY_API_KEY")
SHOPIFY_API_KEY = os.getenv("SHOPIFY_API_KEY")

def run_marketing_content_cycle():
    logger.info("[MARKETING] Running content cycle (placeholder).")

def run_product_cycle():
    logger.info("[PRODUCT] Running product cycle (placeholder).")

def run_funnel_cycle():
    logger.info("[FUNNEL] Running funnel optimization (placeholder).")

def run_analytics_cycle():
    logger.info("[ANALYTICS] Running analytics + insights (placeholder).")

def run_strategy_review():
    logger.info("[STRATEGY] Running strategy review (placeholder).")

def sync_to_notion():
    logger.info("[NOTION] Syncing updates to Notion (placeholder).")

class Scheduler:
    def __init__(self):
        self.jobs = []

    def add_job(self, name, func, interval_minutes):
        self.jobs.append({
            "name": name,
            "func": func,
            "interval": timedelta(minutes=interval_minutes),
            "next_run": datetime.utcnow()
        })

    def run_forever(self, sleep_seconds=30):
        logger.info("🚀 Orchestrator started. Running hybrid schedule...")
        while True:
            now = datetime.utcnow()
            for job in self.jobs:
                if now >= job["next_run"]:
                    logger.info(f"▶️ Running job: {job['name']}")
                    try:
                        job["func"]()
                    except Exception as e:
                        logger.exception(f"❌ Error in job {job['name']}: {e}")
                    job["next_run"] = now + job["interval"]
                    logger.info(f"⏭ Next run for {job['name']}: {job['next_run']}")
            time.sleep(sleep_seconds)

def register_jobs():
    scheduler = Scheduler()

    scheduler.add_job("content_cycle", run_marketing_content_cycle, 60 * 24)
    scheduler.add_job("product_cycle", run_product_cycle, 60 * 24 * 3)
    scheduler.add_job("funnel_cycle", run_funnel_cycle, 60 * 24 * 7)
    scheduler.add_job("analytics_cycle", run_analytics_cycle, 60 * 24)
    scheduler.add_job("notion_sync", sync_to_notion, 60 * 24)
    scheduler.add_job("strategy_review", run_strategy_review, 60 * 24 * 7)

    return scheduler

if __name__ == "__main__":
    scheduler = register_jobs()
    scheduler.run_forever()
