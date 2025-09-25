from __future__ import annotations
from domain.pricing import PricingStrategy, NoDiscount, PercentageDiscount, BulkItemDiscount, CompositeStrategy


def choose_strategy(kind: str, **kwargs) -> PricingStrategy:
    # TODO: Implement strategy selection logic based on the 'kind' parameter
    # Should support: "none", "percent", "bulk", "composite"
    # Each strategy type needs different parameters from **kwargs
    # Return the appropriate strategy instance or raise an error for unknown types
    if kind == "none":
        return NoDiscount()
    elif kind == "percent":
        percent = kwargs.get("percent")
        if percent is None:
            raise ValueError("Missing 'percent' parameter")
        return PercentageDiscount(percent)
    elif kind == "bulk":
        sku = kwargs.get("sku")
        threshold = kwargs.get("threshold")
        per_item_off = kwargs.get("per_item_off")
        if None in (sku, threshold, per_item_off):
            raise ValueError("Missing one of the required parameters: 'sku', 'threshold', 'per_item_off'")
        return BulkItemDiscount(sku, threshold, per_item_off)
    elif kind == "composite":
        strategies = kwargs.get("strategies")
        if not strategies or not isinstance(strategies, list):
            raise ValueError("Missing or invalid 'strategies' parameter; must be a list of PricingStrategy instances")
        for strategy in strategies:
            if not isinstance(strategy, PricingStrategy):
                raise ValueError("All items in 'strategies' must be instances of PricingStrategy")
        return CompositeStrategy(strategies)
    else:
        raise ValueError(f"Unknown strategy kind: {kind}")
    pass
