from __future__ import annotations
from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass(frozen=True)
class LineItem:
    sku: str
    qty: int
    unit_price: float


class PricingStrategy(ABC):
    # TODO: Define the common interface for all pricing strategies.
    # This should include a method that takes pricing parameters and returns a calculated value.
    @abstractmethod
    def apply(self, subtotal: float, items: list[LineItem]) -> float:
        pass



class NoDiscount(PricingStrategy):
    # TODO: Implement a strategy that returns the original value without changes
    def apply(self, subtotal: float, items: list[LineItem]) -> float:
        if not isinstance(subtotal, (int, float)) or subtotal < 0:
            raise ValueError("Subtotal must be a non-negative number")
        for item in items:
            if not isinstance(item, LineItem):
                raise ValueError("All items must be of type LineItem")
            if item.qty < 0 or item.unit_price < 0:
                raise ValueError("Item quantity and unit price must be non-negative")
        return round(float(subtotal), 2)  # No discount applied, return original subtotal



class PercentageDiscount(PricingStrategy):
    def __init__(self, percent: float) -> None:
        # TODO: Store the percentage value and validate it's in the correct range
        if not (0 <= percent <= 100):
            raise ValueError("Percentage must be between 0 and 100.")
        self.percent = percent

    # TODO: Implement the main calculation method that reduces the input by a percentage
    def apply(self, subtotal: float, items: list[LineItem]) -> float:
        subtotal = super().apply(subtotal, items)
        discount = subtotal * (self.percent / 100)
        return round(subtotal - discount, 2)


class BulkItemDiscount(PricingStrategy):
    """If any single item's quantity >= threshold, apply a per-item discount for that SKU."""
    def __init__(self, sku: str, threshold: int, per_item_off: float) -> None:
        # TODO: Store the parameters needed to identify items and calculate reductions
        self.sku = sku
        self.threshold = threshold
        self.per_item_off = per_item_off

    # TODO: Implement logic to iterate through items and apply reductions based on quantity thresholds
    def apply(self, subtotal: float, items: list[LineItem]) -> float:
        subtotal = super().apply(subtotal, items)
        for item in items:
            if item.sku == self.sku and item.qty >= self.threshold:
                subtotal -= self.per_item_off * item.qty
        return round(subtotal, 2)


class CompositeStrategy(PricingStrategy):
    """Compose multiple strategies; apply in order."""
    def __init__(self, strategies: list[PricingStrategy]) -> None:
        # TODO: Store the collection of strategies to be applied sequentially
        self.strategies = strategies

    # TODO: Implement method that applies each strategy in sequence, using the output of one as input to the next
    def apply(self, subtotal: float, items: list[LineItem]) -> float:
        for strategy in self.strategies:
            subtotal = strategy.calculate(subtotal, items)
        return subtotal

def compute_subtotal(items: list[LineItem]) -> float:
    return round(sum(it.unit_price * it.qty for it in items), 2)
