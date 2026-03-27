from typing import Iterable


def build_badge_counts(items: Iterable) -> dict:
    return {"total": len(list(items))}
