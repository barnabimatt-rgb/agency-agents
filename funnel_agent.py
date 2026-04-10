import os
from openai import OpenAI


class FunnelAgent:
    """
    Builds:
    - Landing page copy
    - Email sequences
    - Lead magnets
    - CTAs
    - Funnel structure
    """

    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def build_funnel(self, product, product_url):
        """
        Returns a dict of funnel assets.
        """
        prompt = f"""
        You are a funnel strategist for a hybrid athlete, tactical, AI-automation creator.

        Product:
        {product}

        Product URL:
        {product_url}

        Create:
        - A landing page headline
        - A landing page subheadline
        - A 3-step CTA section
        - A 5-email nurture sequence
        - A lead magnet idea
        - A short CTA to include in video descriptions

        Return ONLY a JSON object with:
        - headline
        - subheadline
        - steps (list)
        - emails (list)
        - lead_magnet
        - short_cta
        """

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        raw = response.choices[0].message.content

        try:
            funnel = eval(raw)
            return funnel
        except:
            print("[FunnelAgent] Failed to parse funnel JSON.")
            return {}
