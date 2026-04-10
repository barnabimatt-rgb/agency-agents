import os
from notion_client import Client
from openai import OpenAI

class TopicAgent:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.notion = Client(auth=os.getenv("NOTION_API_KEY"))

        # Unified Notion DB
        self.db_id = os.getenv("NOTION_DATABASE_ID")

        # Your niche stack
        self.niches = [
            "Hybrid Fitness (HYROX, endurance, tactical strength)",
            "AI automation and workflow systems",
            "Digital entrepreneurship and passive income",
            "Notion systems and productivity frameworks",
            "Tactical mindset, discipline, and identity"
        ]

    def generate_topics(self, n=3):
        """Generate n high-performing short-form video ideas."""
        prompt = f"""
        You are an elite content strategist. Generate {n} viral short-form video ideas 
        that combine these niches:

        - Hybrid Fitness (HYROX, endurance, tactical strength)
        - AI automation and workflow systems
        - Digital entrepreneurship and passive income
        - Notion systems and productivity frameworks
        - Tactical mindset, discipline, identity

        Rules:
        - Each idea must be 5–12 words.
        - Each idea must be punchy, scroll-stopping, and specific.
        - No hashtags, no emojis.
        - No generic advice.
        - Every idea must be unique and high-signal.

        Return ONLY a numbered list of ideas.
        """

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        # New SDK format
        raw = response.choices[0].message.content

        ideas = [
            line.split(". ", 1)[1]
            for line in raw.split("\n")
            if ". " in line
        ]

        return ideas

    def get_existing_topics(self):
        """Fetch existing topics from Notion to avoid duplicates."""
        pages = self.notion.databases.query(database_id=self.db_id)
        existing = set()

        for page in pages["results"]:
            title_prop = page["properties"].get("Name", {})
            title_array = title_prop.get("title", [])
            if title_array:
                existing.add(title_array[0]["plain_text"].strip().lower())

        return existing

    def write_topic_to_notion(self, topic):
        """Insert a new topic as a task in Notion."""
        self.notion.pages.create(
            parent={"database_id": self.db_id},
            properties={
                "Name": {"title": [{"text": {"content": topic}}]},
                "Status": {"select": {"name": "Pending"}}
            }
        )

    def run(self, n=3):
        """Generate topics, filter duplicates, write new ones to Notion."""
        print("Generating new content topics...")

        ideas = self.generate_topics(n)
        existing = self.get_existing_topics()

        new_ideas = [idea for idea in ideas if idea.lower() not in existing]

        if not new_ideas:
            print("No new unique ideas generated.")
            return []

        for idea in new_ideas:
            print(f"Adding topic: {idea}")
            self.write_topic_to_notion(idea)

        return new_ideas
