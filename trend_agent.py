import os
from openai import OpenAI


class TrendAgent:
    """
    Scans for trending topics in your niche.
    Feeds insights back into TopicAgent.
    """

    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def update_trends(self):
        prompt = """
        You are a trend analyst for a hybrid athlete, tactical, AI-automation creator.

        Identify:
        - 5 trending topics in Hybrid Fitness
        - 5 trending topics in AI Automation
        - 5 trending topics in Digital Entrepreneurship
        - 5 trending topics in Notion Systems
        - 5 trending topics in Tactical Mindset

        Return ONLY a JSON object with:
        - hybrid_fitness
        - ai_automation
        - digital_entrepreneurship
        - notion_systems
        - tactical_mindset
        """

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        raw = response.choices[0].message.content

        try:
            trends = eval(raw)
            print("[TrendAgent] Updated trends:", trends)
            return trends
        except:
            print("[TrendAgent] Failed to parse trend JSON.")
            return {}
