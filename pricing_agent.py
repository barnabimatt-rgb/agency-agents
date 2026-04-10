class PricingAgent:
    """
    Suggests pricing based on:
    - Product type
    - Deliverables
    - Market norms
    """

    def __init__(self):
        pass

    def suggest_price(self, product):
        """
        Simple heuristic:
        - Notion templates: $9–$29
        - Guides/playbooks: $19–$49
        - Systems/automation: $29–$99
        """
        name = product.get("name", "").lower()
        deliverables = product.get("deliverables", [])

        if "notion" in name:
            return 19

        if "guide" in name or "playbook" in name:
            return 29

        if "system" in name or "automation" in name:
            return 49

        # Default
        return 25
