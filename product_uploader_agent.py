import os
import requests


class ProductUploaderAgent:
    """
    Publishes products to:
    - Gumroad
    - Lemon Squeezy
    - Stripe Checkout

    Returns a product URL.
    """

    def __init__(self):
        self.gumroad_key = os.getenv("GUMROAD_API_KEY")
        self.ls_key = os.getenv("LEMONSQUEEZY_API_KEY")
        self.stripe_key = os.getenv("STRIPE_SECRET_KEY")

    # ---------------------------------------------------------
    # Gumroad
    # ---------------------------------------------------------
    def _upload_gumroad(self, product, price):
        url = "https://api.gumroad.com/v2/products"
        headers = {"Authorization": f"Bearer {self.gumroad_key}"}

        data = {
            "name": product["name"],
            "description": product["description"],
            "price": int(price * 100),  # cents
            "published": True
        }

        resp = requests.post(url, headers=headers, data=data)
        if resp.status_code != 200:
            print("[ProductUploader] Gumroad error:", resp.text)
            return None

        product_id = resp.json().get("product", {}).get("id")
        if not product_id:
            return None

        return f"https://gumroad.com/l/{product_id}"

    # ---------------------------------------------------------
    # Lemon Squeezy
    # ---------------------------------------------------------
    def _upload_lemonsqueezy(self, product, price):
        url = "https://api.lemonsqueezy.com/v1/products"
        headers = {
            "Authorization": f"Bearer {self.ls_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "data": {
                "type": "products",
                "attributes": {
                    "name": product["name"],
                    "description": product["description"],
                    "price": price,
                    "status": "published"
                }
            }
        }

        resp = requests.post(url, headers=headers, json=payload)
        if resp.status_code not in [200, 201]:
            print("[ProductUploader] Lemon Squeezy error:", resp.text)
            return None

        pid = resp.json().get("data", {}).get("id")
        if not pid:
            return None

        return f"https://{os.getenv('LEMONSQUEEZY_STORE')}.lemonsqueezy.com/checkout/buy/{pid}"

    # ---------------------------------------------------------
    # Stripe Checkout
    # ---------------------------------------------------------
    def _upload_stripe(self, product, price):
        url = "https://api.stripe.com/v1/products"
        headers = {"Authorization": f"Bearer {self.stripe_key}"}

        # Create product
        resp = requests.post(url, headers=headers, data={"name": product["name"]})
        if resp.status_code != 200:
            print("[ProductUploader] Stripe product error:", resp.text)
            return None

        product_id = resp.json().get("id")

        # Create price
        price_resp = requests.post(
            "https://api.stripe.com/v1/prices",
            headers=headers,
            data={
                "unit_amount": int(price * 100),
                "currency": "usd",
                "product": product_id
            }
        )

        if price_resp.status_code != 200:
            print("[ProductUploader] Stripe price error:", price_resp.text)
            return None

        price_id = price_resp.json().get("id")

        # Create checkout link
        checkout_resp = requests.post(
            "https://api.stripe.com/v1/checkout/sessions",
            headers=headers,
            data={
                "mode": "payment",
                "line_items[0][price]": price_id,
                "line_items[0][quantity]": 1,
                "success_url": "https://yourdomain.com/success",
                "cancel_url": "https://yourdomain.com/cancel"
            }
        )

        if checkout_resp.status_code != 200:
            print("[ProductUploader] Stripe checkout error:", checkout_resp.text)
            return None

        return checkout_resp.json().get("url")

    # ---------------------------------------------------------
    # Main entrypoint
    # ---------------------------------------------------------
    def publish(self, product, price):
        """
        Publishes to all platforms and returns the first successful URL.
        """
        print("[ProductUploader] Publishing product...")

        # Try Gumroad
        if self.gumroad_key:
            url = self._upload_gumroad(product, price)
            if url:
                return url

        # Try Lemon Squeezy
        if self.ls_key:
            url = self._upload_lemonsqueezy(product, price)
            if url:
                return url

        # Try Stripe
        if self.stripe_key:
            url = self._upload_stripe(product, price)
            if url:
                return url

        print("[ProductUploader] All platforms failed.")
        return None
