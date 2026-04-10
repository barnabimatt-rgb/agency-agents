import os
from openai import OpenAI


class RepurposingAgent:
    """
    Repurposes a script into:
    - Tweet thread
    - LinkedIn post
    - Pinterest text
    - Newsletter snippet
    - Blog outline
    """

    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def create_from_script(self, topic: str, script: str, urls: dict):
        prompt = f"""
        You are a repurposing strategist for a hybrid athlete, tactical, AI-automation creator.

        Topic: {topic}

        Script:
        {script}

        URLs:
        {urls}

        Create:
        - A 6–10 tweet thread
        - A LinkedIn post
        - A Pinterest description
        - A newsletter snippet (2–3 paragraphs)
        - A blog outline (5–7 sections)

        Return ONLY a JSON object with:
        - thread
        - linkedin
        - pinterest
        - newsletter
        - blog_outline
        """

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        raw = response.choices[0].message.content

        try:
            return eval(raw)
        except:
            print("[RepurposingAgent] Failed to parse JSON.")
            return {}
