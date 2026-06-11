"""
discount_engine.py
------------------
Implements a flexible discount system using the Strategy design pattern.

Each discount type is encapsulated in its own class, making it easy to add,
remove, or modify discount rules without touching the core engine logic.

Classes:
    Product             – A simple product with a name and price.
    DiscountStrategy    – Abstract base class defining the discount interface.
    PercentageDiscount  – Applies a percentage-based discount.
    FixedAmountDiscount – Subtracts a fixed amount from the price.
    PremiumUserDiscount – Grants a 20% discount to premium-tier users.
    DiscountEngine      – Evaluates all strategies and returns the best price.
"""

from abc import ABC, abstractmethod


# ---------------------------------------------------------------------------
# Domain model
# ---------------------------------------------------------------------------

class Product:
    """
    Represents a purchasable product.

    Attributes:
        name  (str):   Human-readable product name.
        price (float): Base price before any discounts are applied.
    """

    def __init__(self, name: str, price: float) -> None:
        if price < 0:
            raise ValueError(f"Product price cannot be negative, got {price}")
        self.name = name
        self.price = price

    def __str__(self) -> str:
        return f"{self.name} - ${self.price:.2f}"


# ---------------------------------------------------------------------------
# Strategy interface
# ---------------------------------------------------------------------------

class DiscountStrategy(ABC):
    """
    Abstract base class for all discount strategies.

    Every concrete strategy must implement two methods:
      - is_applicable: decides whether this discount can be applied.
      - apply_discount: computes the discounted price (never modifies the product).
    """

    @abstractmethod
    def is_applicable(self, product: Product, user_tier: str) -> bool:
        """
        Return True if this strategy should be considered for the given
        product and user tier, False otherwise.
        """

    @abstractmethod
    def apply_discount(self, product: Product) -> float:
        """
        Return the new price after applying this discount.
        Must return a non-negative value.
        """


# ---------------------------------------------------------------------------
# Concrete strategies
# ---------------------------------------------------------------------------

class PercentageDiscount(DiscountStrategy):
    """
    Reduces the product price by a fixed percentage (e.g. 10 → 10% off).

    Args:
        percent (int): Discount percentage. Must be between 1 and 100 inclusive.

    Raises:
        ValueError: If percent is outside the valid range.
    """

    def __init__(self, percent: int) -> None:
        if not (0 < percent <= 100):
            raise ValueError(f"Percent must be between 1 and 100, got {percent}")
        self.percent = percent

    def is_applicable(self, product: Product, user_tier: str) -> bool:
        # Validity is already enforced at construction time, so this discount
        # is always applicable once instantiated.
        return True

    def apply_discount(self, product: Product) -> float:
        """Apply the percentage reduction and return the resulting price."""
        return product.price * (1 - self.percent / 100)


class FixedAmountDiscount(DiscountStrategy):
    """
    Subtracts a fixed monetary amount from the product price (e.g. $5 off).

    Args:
        amount (float): Dollar amount to subtract. Must be positive.

    Raises:
        ValueError: If amount is not positive.
    """

    def __init__(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError(f"Discount amount must be positive, got {amount}")
        self.amount = amount

    def is_applicable(self, product: Product, user_tier: str) -> bool:
        # Only apply when the discount is strictly less than the product price,
        # ensuring the resulting price is always positive.
        return self.amount < product.price

    def apply_discount(self, product: Product) -> float:
        """Subtract the fixed amount and return the resulting price."""
        return product.price - self.amount


class PremiumUserDiscount(DiscountStrategy):
    """
    Grants a 20% discount exclusively to users with the 'premium' tier.

    No constructor arguments are needed; the tier check is done at runtime.
    """

    # Discount applied to premium users (20% off → keep 80% of price).
    DISCOUNT_FACTOR = 0.80

    def is_applicable(self, product: Product, user_tier: str) -> bool:
        # Guard against non-string values for user_tier before calling .lower().
        return isinstance(user_tier, str) and user_tier.lower() == "premium"

    def apply_discount(self, product: Product) -> float:
        """Return the price after applying the 20% premium-user discount."""
        return product.price * self.DISCOUNT_FACTOR


# ---------------------------------------------------------------------------
# Discount engine
# ---------------------------------------------------------------------------

class DiscountEngine:
    """
    Evaluates a collection of discount strategies against a product and
    returns the lowest achievable price.

    The engine follows a best-price approach:
      1. Start with the original price as the baseline.
      2. Collect every discounted price from applicable strategies.
      3. Return the minimum — the best deal for the user.

    Args:
        strategies (list[DiscountStrategy]): Ordered list of strategies to evaluate.
                                             Order does not affect the result.
    """

    def __init__(self, strategies: list[DiscountStrategy]) -> None:
        self.strategies = strategies

    def calculate_best_price(self, product: Product, user_tier: str) -> float:
        """
        Return the lowest price available for the given product and user tier.

        If no strategy is applicable the original product price is returned.

        Args:
            product   (Product): The product being purchased.
            user_tier (str):     The customer's membership tier (e.g. 'premium').

        Returns:
            float: The lowest price found across all applicable strategies.
        """
        # Initialise with the full price so it acts as a natural fallback.
        candidate_prices = [product.price]

        for strategy in self.strategies:
            if strategy.is_applicable(product, user_tier):
                discounted_price = strategy.apply_discount(product)
                candidate_prices.append(discounted_price)

        return min(candidate_prices)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # --- Set up the product ---
    product = Product("Wireless Mouse", 50.0)
    user_tier = "Premium"

    # --- Register discount strategies ---
    # The engine will automatically pick the best one.
    strategies = [
        PercentageDiscount(10),   # 10% off → $45.00
        FixedAmountDiscount(5),   # $5 off  → $45.00
        PremiumUserDiscount(),    # 20% off → $40.00  ← best for premium users
    ]

    # --- Calculate and display the best available price ---
    engine = DiscountEngine(strategies)
    best_price = engine.calculate_best_price(product, user_tier)

    print(f"Best price for {product.name} for {user_tier} user: ${best_price:.2f}")
