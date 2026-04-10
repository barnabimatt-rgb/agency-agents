class CopywriterAgent:
    """
    Rewrites content to:
    - Remove legal issues
    - Improve clarity
    - Improve engagement
    - Stay platform-safe
    """

    def __init__(self):
        pass

    def rewrite_for_compliance(self, title: str, description: str, issues: list[str]):
        """
        Removes flagged terms and rewrites safely.
        """
        safe_title = title
        safe_description = description

        for issue in issues:
            if "Copyright" in issue:
                # Remove references to copyrighted works
                safe_title = safe_title.replace("song", "").replace("movie", "")
                safe_description = safe_description.replace("song", "").replace("movie", "")

            if "Medical Claim" in issue:
                safe_description = safe_description.replace("cure", "improve")
                safe_description = safe_description.replace("heal", "support recovery")

            if "Financial Claim" in issue:
                safe_description = safe_description.replace("guaranteed", "possible")
                safe_description = safe_description.replace("risk-free", "lower-risk")

            if "Defamation" in issue:
                safe_description = safe_description.replace("fraud", "controversial figure")
                safe_description = safe_description.replace("scam", "questionable")

            if "Platform Violation" in issue:
                safe_description = safe_description.replace("hate speech", "negative behavior")
                safe_description = safe_description.replace("violence", "conflict")

        return safe_title.strip(), safe_description.strip()
