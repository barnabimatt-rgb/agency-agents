class AffiliateAgent:
    """
    Injects affiliate links into descriptions.
    Lightweight, text-only, zero compute load.
    """

    def __init__(self):
        # Add your affiliate links here
        self.links = {
            "notion": "https://affiliate.notion.com/your-link",
            "hyrox": "https://hyrox.com/gear",
            "ai_tools": "https://your-affiliate-link.com/ai",
            "fitness": "https://your-affiliate-link.com/fitness",
        }

    def inject_links(self, description: str, topic: str):
        """
        Adds relevant affiliate links based on topic keywords.
        """
        desc = description + "\n\nRecommended tools:\n"

        if "notion" in topic.lower():
            desc += f"- Notion: {self.links['notion']}\n"

        if "ai" in topic.lower() or "automation" in topic.lower():
            desc += f"- AI Tools: {self.links['ai_tools']}\n"

        if "fitness" in topic.lower() or "hyrox" in topic.lower():
            desc += f"- Fitness Gear: {self.links['fitness']}\n"

        return desc.strip()
