import re


class DuplicateDetector:
    """
    Prevents repeated topics, titles, or product ideas.
    Uses simple normalization + fuzzy matching.
    """

    def normalize(self, text: str) -> str:
        text = text.lower().strip()
        text = re.sub(r"[^a-z0-9 ]+", "", text)
        return text

    def is_duplicate(self, a: str, b: str) -> bool:
        """
        Simple fuzzy match:
        - Normalize
        - Compare overlap
        """
        na = self.normalize(a)
        nb = self.normalize(b)

        if na == nb:
            return True

        # Word overlap
        wa = set(na.split())
        wb = set(nb.split())

        overlap = len(wa & wb)
        if overlap >= max(2, min(len(wa), len(wb)) // 2):
            return True

        return False

    def filter_topics(self, topics: list[str]) -> list[str]:
        """
        Removes duplicates within the new batch.
        """
        unique = []
        for t in topics:
            if not any(self.is_duplicate(t, u) for u in unique):
                unique.append(t)
        return unique
