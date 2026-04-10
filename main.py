import os
from notion_client_wrapper import NotionWrapper

# Core content agents
from agents.topic_agent import TopicAgent
from agents.content_pillar_rotator import ContentPillarRotator
from agents.duplicate_detector import DuplicateDetector
from agents.hybrid_agent import HybridAgent

# Compliance & quality
from agents.legal_agent import LegalAgent
from agents.copywriter_agent import CopywriterAgent
from agents.persona_agent import PersonaAgent

# Distribution
from agents.youtube_agent import YouTubeAgent
from agents.tiktok_agent import TikTokAgent
from agents.instagram_agent import InstagramAgent
from agents.facebook_reels_agent import FacebookReelsAgent
from agents.x_agent import XAgent
from agents.pinterest_agent import PinterestAgent
from agents.linkedin_agent import LinkedInAgent

# Monetization
from agents.product_agent import ProductAgent
from agents.product_uploader_agent import ProductUploaderAgent
from agents.funnel_agent import FunnelAgent

# System automation
from agents.status_updater import StatusUpdater
from agents.analytics_agent import AnalyticsAgent
from agents.scheduler_agent import SchedulerAgent
from agents.error_monitor_agent import ErrorMonitorAgent
from agents.asset_cleaner_agent import AssetCleanerAgent

# Repurposing / leverage
from agents.repurposing_agent import RepurposingAgent
from agents.seo_agent import SEOAgent
from agents.affiliate_agent import AffiliateAgent
from agents.upsell_agent import UpsellAgent
from agents.pricing_agent import PricingAgent
from agents.trend_agent import TrendAgent


notion = NotionWrapper()

topic_agent = TopicAgent()
pillar_rotator = ContentPillarRotator()
duplicate_detector = DuplicateDetector()
hybrid_agent = HybridAgent()

legal_agent = LegalAgent()
copywriter_agent = CopywriterAgent()
persona_agent = PersonaAgent()

youtube_agent = YouTubeAgent()
tiktok_agent = TikTokAgent()
instagram_agent = InstagramAgent()
facebook_agent = FacebookReelsAgent()
x_agent = XAgent()
pinterest_agent = PinterestAgent()
linkedin_agent = LinkedInAgent()

product_agent = ProductAgent()
product_uploader = ProductUploaderAgent()
funnel_agent = FunnelAgent()

status_updater = StatusUpdater()
analytics_agent = AnalyticsAgent()
scheduler_agent = SchedulerAgent()
error_monitor = ErrorMonitorAgent()
asset_cleaner = AssetCleanerAgent()

repurposing_agent = RepurposingAgent()
seo_agent = SEOAgent()
affiliate_agent = AffiliateAgent()
upsell_agent = UpsellAgent()
pricing_agent = PricingAgent()
trend_agent = TrendAgent()


def process_cycle():
    """
    One full automation cycle:
    - Generate topics
    - Build videos
    - Run legal + copy
    - Upload everywhere
    - Log + update status
    - Trigger products/funnels/repurposing
    """

    try:
        # 1) Rotate content pillars and generate topics
        active_pillar = pillar_rotator.choose_pillar()
        raw_topics = topic_agent.generate_topics(n=3, pillar=active_pillar)
        unique_topics = duplicate_detector.filter_topics(raw_topics)

        topic_agent.write_topics_to_notion(unique_topics)

        # 2) Fetch scheduled / pending tasks (SchedulerAgent can filter by time)
        tasks = scheduler_agent.get_tasks_to_run(notion)

        if not tasks:
            print("No tasks scheduled for this window.")
            return

        for task in tasks:
            page_id = task["id"]
            props = task["properties"]

            title_prop = props.get("Name", {})
            title_array = title_prop.get("title", [])
            if not title_array:
                print(f"Skipping page {page_id}: no Name.")
                continue

            topic = title_array[0].get("plain_text", "").strip()
            if not topic:
                print(f"Skipping page {page_id}: empty Name.")
                continue

            print(f"Processing topic: {topic}")

            # Mark as In Progress
            status_updater.set_status(page_id, "In Progress")

            # 3) Generate video (HybridAgent internally uses ScriptParser, MediaResolver, VideoAssembler)
            try:
                video_path, script, raw_title, raw_description = hybrid_agent.run(topic)
            except Exception as e:
                print(f"Error generating video for '{topic}': {e}")
                error_monitor.log_error("video_generation", topic, str(e))
                status_updater.set_status(page_id, "Failed")
                continue

            # 4) Legal + copywriting + persona alignment
            #    First pass: legal check on raw script/title/description
            legal_issues = legal_agent.check_content(
                script=script,
                title=raw_title,
                description=raw_description,
            )

            if legal_issues:
                print(f"Legal issues detected for '{topic}', rewriting...")
                safe_title, safe_description = copywriter_agent.rewrite_for_compliance(
                    title=raw_title,
                    description=raw_description,
                    issues=legal_issues,
                )
            else:
                safe_title, safe_description = raw_title, raw_description

            # Persona alignment + optimization
            final_title, final_description = persona_agent.align_and_optimize(
                title=safe_title,
                description=safe_description,
                topic=topic,
            )

            # 5) SEO + affiliate enrichment
            seo_title, seo_description, tags = seo_agent.optimize(
                title=final_title,
                description=final_description,
                topic=topic,
            )

            enriched_description = affiliate_agent.inject_links(
                description=seo_description,
                topic=topic,
            )

            # 6) Upload to all platforms
            urls = {}

            try:
                yt_url = youtube_agent.upload(video_path, seo_title, enriched_description, tags)
                urls["youtube"] = yt_url
            except Exception as e:
                error_monitor.log_error("youtube_upload", topic, str(e))

            try:
                tt_url = tiktok_agent.upload(video_path, seo_title, enriched_description)
                urls["tiktok"] = tt_url
            except Exception as e:
                error_monitor.log_error("tiktok_upload", topic, str(e))

            try:
                ig_url = instagram_agent.upload(video_path, seo_title, enriched_description)
                urls["instagram"] = ig_url
            except Exception as e:
                error_monitor.log_error("instagram_upload", topic, str(e))

            try:
                fb_url = facebook_agent.upload(video_path, seo_title, enriched_description)
                urls["facebook"] = fb_url
            except Exception as e:
                error_monitor.log_error("facebook_upload", topic, str(e))

            try:
                x_url = x_agent.upload(video_path, seo_title)
                urls["x"] = x_url
            except Exception as e:
                error_monitor.log_error("x_upload", topic, str(e))

            try:
                pin_url = pinterest_agent.upload(video_path, seo_title, enriched_description)
                urls["pinterest"] = pin_url
            except Exception as e:
                error_monitor.log_error("pinterest_upload", topic, str(e))

            try:
                li_url = linkedin_agent.upload(video_path, seo_title, enriched_description)
                urls["linkedin"] = li_url
            except Exception as e:
                error_monitor.log_error("linkedin_upload", topic, str(e))

            # 7) Log URLs + mark as Done
            notion.write_video_urls(page_id, urls)
            status_updater.set_status(page_id, "Done")

            # 8) Repurpose content (threads, posts, newsletter snippets)
            repurposed_assets = repurposing_agent.create_from_script(
                topic=topic,
                script=script,
                urls=urls,
            )
            notion.write_repurposed_assets(page_id, repurposed_assets)

            # 9) Product + funnel (can be periodic, but here we keep it simple)
            product_idea = product_agent.maybe_generate_product(topic, script)
            if product_idea:
                price = pricing_agent.suggest_price(product_idea)
                product_url = product_uploader.publish(product_idea, price)
                funnel_assets = funnel_agent.build_funnel(product_idea, product_url)
                notion.write_product_and_funnel(page_id, product_url, funnel_assets)

        # 10) Analytics + trends + cleanup
        analytics_agent.sync_all()
        trend_agent.update_trends()
        asset_cleaner.cleanup_temp_files()

    except Exception as e:
        # Top-level catch so the container doesn't die silently
        print(f"Fatal error in process_cycle: {e}")
        error_monitor.log_error("fatal", "process_cycle", str(e))


if __name__ == "__main__":
    process_cycle()
