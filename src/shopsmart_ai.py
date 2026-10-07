from __future__ import annotations

from dataclasses import dataclass


def normalize_query(raw: str) -> str:
    """Normalize user search text for consistent matching."""
    if raw is None:
        raise ValueError("raw query cannot be None")
    return " ".join(str(raw).strip().split()).lower()


@dataclass
class ProductMatcher:
    query: str

    def __post_init__(self) -> None:
        self.query = normalize_query(self.query)

    def score(self, product_name: str) -> int:
        normalized_product = normalize_query(product_name)
        if not normalized_product:
            return 0
        product_tokens = normalized_product.split()
        query_tokens = self.query.split()
        return sum(1 for token in query_tokens if token in product_tokens)

    def matches(self, product_name: str, min_score: int = 1) -> bool:
        return self.score(product_name) >= min_score


def build_product_summary(product_name: str, query: str) -> str:
    matcher = ProductMatcher(query)
    score = matcher.score(product_name)
    return f"{product_name} matches query '{query}' with score {score}"
