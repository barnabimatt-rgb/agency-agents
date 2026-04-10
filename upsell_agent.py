class UpsellAgent:
    """
    Creates upsells and cross-sells for products.
    """

    def __init__(self):
        pass

    def create_upsells(self, product, product_url):
        """
        Returns a list of upsell ideas.
        """
        name = product.get("name", "This Product")

        return [
            f"Upgrade to the premium version of {name}",
            f"Bundle {name} with our Tactical Training Guide",
            f"Add 1-on-1 coaching for deeper implementation",
        ]
