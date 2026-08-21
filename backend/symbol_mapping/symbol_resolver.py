"""
symbol_resolver.py

Resolves AndyScanner canonical market symbols into
provider-specific symbols.

The scanner's internal market identity must never be
changed merely because a provider uses a different symbol.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class SymbolResolution:
    canonical: str
    provider: str
    symbol: str | None
    supported: bool


class SymbolResolver:
    """
    Resolve canonical AndyScanner markets for providers.

    Canonical symbols are provider-independent.

    Examples:

        EURUSD -> EUR/USD
        GBPUSD -> GBP/USD
        USDJPY -> USD/JPY
        XAUUSD -> XAU/USD
        XAGUSD -> XAG/USD
    """

    # ==================================================
    # Explicit Provider Mappings
    # ==================================================

    _MAPPINGS = {

        # --------------------------------------------------
        # Twelve Data
        # --------------------------------------------------

        "TWELVEDATA": {

            # Forex
            "EURUSD": "EUR/USD",
            "GBPUSD": "GBP/USD",
            "USDJPY": "USD/JPY",

            # Precious metals
            "XAUUSD": "XAU/USD",
            "XAGUSD": "XAG/USD",
        },

        # --------------------------------------------------
        # Generic API
        #
        # Current API endpoint is Twelve Data's
        # /time_series endpoint, so it uses the same
        # provider symbol conventions.
        # --------------------------------------------------

        "API": {

            # Forex
            "EURUSD": "EUR/USD",
            "GBPUSD": "GBP/USD",
            "USDJPY": "USD/JPY",

            # Precious metals
            "XAUUSD": "XAU/USD",
            "XAGUSD": "XAG/USD",
        },

        # --------------------------------------------------
        # CSV
        #
        # CSV files use AndyScanner canonical symbols.
        # --------------------------------------------------

        "CSV": {

            "US30": "US30",

            "EURUSD": "EURUSD",
            "GBPUSD": "GBPUSD",
            "USDJPY": "USDJPY",

            "XAUUSD": "XAUUSD",
            "XAGUSD": "XAGUSD",
        },

        # --------------------------------------------------
        # MT5
        #
        # Broker-specific mappings will be added when
        # broker symbols are configured.
        # --------------------------------------------------

        "MT5": {},
    }

    # ==================================================
    # Resolve
    # ==================================================

    @classmethod
    def resolve(
        cls,
        market: str,
        provider: str,
    ) -> SymbolResolution:

        canonical = market.strip().upper()
        provider_name = provider.strip().upper()

        if not canonical:
            raise ValueError(
                "Market symbol cannot be empty."
            )

        if not provider_name:
            raise ValueError(
                "Provider name cannot be empty."
            )

        provider_mappings = cls._MAPPINGS.get(
            provider_name,
            {},
        )

        symbol = provider_mappings.get(
            canonical
        )

        return SymbolResolution(
            canonical=canonical,
            provider=provider_name,
            symbol=symbol,
            supported=symbol is not None,
        )

    # ==================================================
    # Supported
    # ==================================================

    @classmethod
    def is_supported(
        cls,
        market: str,
        provider: str,
    ) -> bool:

        return cls.resolve(
            market,
            provider,
        ).supported