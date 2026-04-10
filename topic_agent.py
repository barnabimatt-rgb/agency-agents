import os
from typing import List
from notion_client import Client
from openai import OpenAI


class TopicAgent:
    """
    Generates new content topics based on your niche stack and writes them into Notion.
    Uses a single unified Notion database (NOTION_DATABASE_ID).
    """

    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.notion = Client(auth=os.getenv("NOTION_API_KEY"))
        self.db_id = os.getenv("NOTION_DATABASE_ID")

        # Your niche stack pillars
        self.pillars = {
            "hybrid_fitness": "Hybrid Fitness (HYROX, endurance, tactical strength)",
            "ai_automation": "AI automation and workflow systems",
            "digital_entrepreneurship": "Digital entrepreneurship and passive income",
            "notion_systems": "Notion systems and productivity frameworks",
            "tactical_mindset": "Tactical mindset, discipline, and identity",
        }

    def generate_topics(self, n: int = 3, pillar: str | None = None) -> List[str]:
        """
        Generate n high-performing short-form video ideas.
        If pillar is provided, bias ideas toward that pillar.
        """
        if pillar and pillar in self.pillars:
            pillar_desc = self.pillars[pillar]
        else:
            pillar_desc = "All pillars combined"

        prompt = f"""
        You are an elite content strategist for a hybrid athlete, tactical, AI-automation creator.

        Generate {n} viral short-form video ideas that fit this niche stack:

        - Hybrid Fitness (HYROX, endurance, tactical strength)
        - AI automation and workflow systems
        - Digital entrepreneurship and passive income
        - Notion systems and productivity frameworks
        - Tactical mindset, discipline, identity

        Current focus pillar: {pillar_desc}

        Rules:
        - Each idea must be 5–12 words.
        - Each idea must be punchy, scroll-stopping, and specific.
        - No hashtags, no emojis.
        - No generic advice.
        - Every idea must be unique and high-signal.
        - Ideas should feel like they come from someone who actually trains, builds systems, and lives this.

        Return ONLY a numbered list of ideas.
        """

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        raw = response.choices[0].message.content

        ideas: List[str] = [
            line.split(". ", 1)[1].strip()
            for line in raw.split("\n")
            if ". " in line
        ]

        return [idea for idea in ideas if idea]

    def _get_existing_titles(self) -> set[str]:
        """
        Fetch existing topics from Notion to avoid duplicates.
        Assumes a 'Name' title property.
        """
        existing: set[str] = set()

        has_more = True
        cursor = None

        while has_more:
            kwargs = {"database_id": self.db_id}
            if cursor:
                kwargs["start_cursor"] = cursor

            pages = self.notion.databases.query(**kwargs)

            for page in pages.get("results", []):
                title_prop = page["properties"].get("Name", {})
                title_array = title_prop.get("title", [])
                if title_array:
                    existing.add(title_array[0]["plain_text"].strip().lower())

            has_more = pages.get("has_more", False)
            cursor = pages.get("next_cursor")

        return existing

    def write_topics_to_notion(self, topics: List[str]) -> None:
        """
        Insert new topics as tasks in Notion with Status = Pending.
        """
        if not topics:
            return

        for topic in topics:
            self.notion.pages.create(
                parent={"database_id": self.db_id},
                properties={
                    "Name": {"title": [{"text": {"content": topic}}]},
                    "Status": {"select": {"name": "Pending"}},
                }
            )

    def run(self, n: int = 3, pillar: str | None = None) -> List[str]:
        """
        Convenience method: generate topics, filter duplicates, write new ones to Notion.
        """
        print("Generating new content topics...")

        ideas = self.generate_topics(n=n, pillar=pillar)
        existing = self._get_existing_titles()

        new_ideas = [idea for idea in ideas if idea.lower() not in existing]

        if not new_ideas:
            print("No new unique ideas generated.")
            return []

        self.write_topics_to_notion(new_ideas)

        for idea in new_ideas:
            print(f"Added topic: {idea}")

        return new_ideas
