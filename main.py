import os
import time
import logging
from datetime import datetime, timedelta

# -----------------------------
# Logging Setup
# -----------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

# -----------------------------
# Environment Variables
# -----------------------------
NOTION_API_KEY = os.getenv("NOTION_API_KEY")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
TIKTOK_API_KEY = os.getenv("TIKTOK_API_KEY")
INSTAGRAM_TOKEN = os.getenv("INSTAGRAM_TOKEN")
TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")

GUMROAD_API_KEY = os.getenv("GUMROAD_API_KEY")
ETSY_API_KEY = os.getenv("ETSY_API_KEY")
SHOPIFY_API_KEY = os.getenv("SHOPIFY_API_KEY")

# -----------------------------
# Import Real Agents
# -----------------------------
from marketing.content_agent import generate_content
from product.product_agent import generate_product
from marketing.funnel_agent import optimize_funnel
from analytics.analytics_agent import pull_analytics
from strategy.strategy_agent import generate_strategy_review
from notion.sync_agent import sync_notion

# -----------------------------
# Agent Wrappers
# -----------------------------
def run_marketing_content_cycle():
    logger.info("[MARKETING] Running content cycle...")
    try:
        generate_content()
        logger.info("[MARKETING] Content cycle complete.")
    except Exception as e:
        logger.exception(f"[MARKETING] Error: {e}")

def run_product_cycle():
    logger.info("[PRODUCT] Running product cycle...")
    try:
        generate_product()
        logger.info("[PRODUCT] Product cycle complete.")
    except Exception as e:
        logger.exception(f"[PRODUCT] Error: {e}")

def run_funnel_cycle():
    logger.info("[FUNNEL] Running funnel optimization...")
    try:
        optimize_funnel()
        logger.info("[FUNNEL] Funnel optimization complete.")
    except Exception as e:
        logger.exception(f"[FUNNEL] Error: {e}")

def run_analytics_cycle():
    logger.info("[ANALYTICS] Pulling analytics...")
    try:
        pull_analytics()
        logger.info("[ANALYTICS] Analytics cycle complete.")
    except Exception as e:
        logger.exception(f"[ANALYTICS] Error: {e}")

def run_strategy_review():
    logger.info("[STRATEGY] Running strategy review...")
    try:
        generate_strategy_review()
        logger.info("[STRATEGY] Strategy review complete.")
    except Exception as e:
        logger.exception(f"[STRATEGY] Error: {e}")

def sync_to_notion():
    logger.info("[NOTION] Syncing to Notion...")
    try:
        sync_notion()
        logger.info("[NOTION] Sync complete.")
    except Exception as e:
        logger.exception(f"[NOTION] Error: {e}")

# -----------------------------
# Scheduler
# -----------------------------
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

# -----------------------------
# Register Jobs
# -----------------------------
def register_jobs():
    scheduler = Scheduler()

    # Daily
    scheduler.add_job("content_cycle", run_marketing_content_cycle, 60 * 24)
    scheduler.add_job("analytics_cycle", run_analytics_cycle, 60 * 24)
    scheduler.add_job("notion_sync", sync_to_notion, 60 * 24)

    # Every 3 days
    scheduler.add_job("product_cycle", run_product_cycle, 60 * 24 * 3)

    # Weekly
    scheduler.add_job("funnel_cycle", run_funnel_cycle, 60 * 24 * 7)
    scheduler.add_job("strategy_review", run_strategy_review, 60 * 24 * 7)

    return scheduler

# -----------------------------
# Main Entry
# -----------------------------
if __name__ == "__main__":
    scheduler = register_jobs()
    scheduler.run_forever()
