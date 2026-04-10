import re


class LegalAgent:
    """
    Scans content for:
    - Copyright risk
    - Medical/financial claims
    - Defamation
    - Platform policy violations
    - Trademark misuse
    """

    def __init__(self):
        # Simple keyword lists (expandable)
        self.copyright_terms = [
            "lyrics", "song by", "as seen in", "from the movie",
            "copyright", "©", "™", "®"
        ]

        self.medical_claims = [
            "cure", "guarantee results", "heal your", "fix your disease",
            "treats cancer", "medical advice"
        ]

        self.financial_claims = [
            "get rich quick", "guaranteed income", "make $10k instantly",
            "risk-free money", "no risk"
        ]

        self.defamation_terms = [
            "this person is a fraud", "scam artist", "criminal behavior",
            "illegal activity by"
        ]

        self.platform_violations = [
            "hate speech", "violence", "explicit content", "graphic content"
        ]

    def _scan(self, text: str, terms: list[str], label: str):
        issues = []
        for t in terms:
            if t.lower() in text.lower():
                issues.append(f"{label}: '{t}' detected")
        return issues

    def check_content(self, script: str, title: str, description: str):
        """
        Returns a list of issues found.
        """
        combined = f"{script}\n{title}\n{description}"

        issues = []
        issues += self._scan(combined, self.copyright_terms, "Copyright")
        issues += self._scan(combined, self.medical_claims, "Medical Claim")
        issues += self._scan(combined, self.financial_claims, "Financial Claim")
        issues += self._scan(combined, self.defamation_terms, "Defamation")
        issues += self._scan(combined, self.platform_violations, "Platform Violation")

        return issues
