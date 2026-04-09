import logging

from agents import (
    generate_content,
    generate_product,
    optimize_funnel,
    generate_strategy_review,
    pull_analytics,
)
from notion_writer import log_entry

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)


def run_all_cycles():
    logger.info("🚀 Starting passive income cycle...")

    # Content
    content = generate_content()
    log_entry(
        title="Content Cycle",
        item_type="Content",
        status="Done",
        notes=content,
    )

    # Product
    product = generate_product()
    log_entry(
        title="Product Cycle",
        item_type="Product",
        status="Done",
        notes=product,
    )

    # Funnel
    funnel = optimize_funnel()
    log_entry(
        title="Funnel Optimization",
        item_type="Funnel",
        status="Done",
        notes=funnel,
    )

    # Strategy
    strategy = generate_strategy_review()
    log_entry(
        title="Strategy Review",
        item_type="Strategy",
        status="Done",
        notes=strategy,
    )

    # Analytics
    analytics = pull_analytics()
    log_entry(
        title="Analytics Snapshot",
        item_type="Analytics",
        status="Done",
        notes=analytics,
    )

    logger.info("✅ Passive income cycle complete.")


if __name__ == "__main__":
    run_all_cycles()
