import os
from openai import OpenAI


class SEOAgent:
    """
    Optimizes:
    - Titles
    - Descriptions
    - Tags
    For YouTube, Pinterest, and Google.
    """

    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def optimize(self, title: str, description: str, topic: str):
        prompt = f"""
        You are an SEO strategist for a hybrid athlete, tactical, AI-automation creator.

        Optimize the following:

        Title: {title}
        Description: {description}
        Topic: {topic}

        Return:
        - Improved title (SEO-optimized)
        - Improved description (SEO-optimized)
        - 10–15 tags (comma-separated)

        Return ONLY a JSON object with:
        - title
        - description
        - tags
        """

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        raw = response.choices[0].message.content

        try:
            data = eval(raw)
            tags = [t.strip() for t in data["tags"].split(",")]
            return data["title"], data["description"], tags
        except:
            print("[SEOAgent] Failed to parse JSON.")
            return title, description, []
