import random


class ContentPillarRotator:
    """
    Ensures TopicAgent rotates through your 5 content pillars evenly.
    """

    def __init__(self):
        self.pillars = [
            "hybrid_fitness",
            "ai_automation",
            "digital_entrepreneurship",
            "notion_systems",
            "tactical_mindset",
        ]

        self.last_used = None

    def choose_pillar(self) -> str:
        """
        Picks a pillar different from the last one used.
        """
        choices = [p for p in self.pillars if p != self.last_used]
        pillar = random.choice(choices)
        self.last_used = pillar
        print(f"[PillarRotator] Selected pillar: {pillar}")
        return pillar
