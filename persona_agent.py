class PersonaAgent:
    """
    Ensures all content matches your voice:
    - Tactical
    - Disciplined
    - Hybrid athlete
    - Systems thinker
    - Calm, direct, no fluff
    """

    def __init__(self):
        self.tones = {
            "hybrid": "Direct, disciplined, tactical, grounded in real training.",
            "systems": "Clear, structured, efficient, automation-first mindset.",
            "entrepreneur": "Practical, no-hype, execution-focused.",
        }

    def align_and_optimize(self, title: str, description: str, topic: str):
        """
        Rewrites title + description to match your persona.
        """
        # Title: short, punchy, tactical
        title = title.strip()
        if len(title.split()) > 10:
            title = " ".join(title.split()[:10])

        # Description: calm, disciplined, no hype
        description = description.strip()

        # Remove hype words
        for word in ["insane", "crazy", "unbelievable", "viral", "secret"]:
            description = description.replace(word, "")

        # Add persona tone
        description += "\n\n" + "Tone: Tactical. Disciplined. System-driven."

        return title, description
