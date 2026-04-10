import os
from openai import OpenAI


class ProductAgent:
    """
    Generates digital products based on:
    - Topic
    - Script content
    - Your niche pillars

    Product types:
    - Notion templates
    - Tactical fitness programs
    - AI automation systems
    - Productivity frameworks
    - Playbooks / guides
    """

    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def maybe_generate_product(self, topic: str, script: str):
        """
        20% chance to generate a product for a given topic.
        You can adjust this logic later.
        """
        import random
        if random.random() > 0.20:
            return None

        prompt = f"""
        You are a product strategist for a hybrid athlete, tactical, AI-automation creator.

        Topic: "{topic}"

        Script:
        {script}

        Create a digital product concept that:
        - Fits the topic
        - Fits the script
        - Fits the niche pillars (Hybrid Fitness, AI Automation, Digital Entrepreneurship, Notion Systems, Tactical Mindset)
        - Is simple to produce (PDF, Notion template, guide, playbook)
        - Has a clear transformation
        - Has a clear target audience
        - Has a clear deliverable

        Return ONLY a JSON object with:
        - name
        - description
        - deliverables (list)
        - target_audience
        - transformation
        """

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        raw = response.choices[0].message.content

        try:
            product = eval(raw)  # safe because model returns pure JSON-like dict
            return product
        except:
            print("[ProductAgent] Failed to parse product JSON.")
            return None
