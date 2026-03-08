import pandas as pd

from services.cache import cache


@cache.memoize(timeout=300)
def get_tca_summary_data() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "desk": ["PT", "PT", "PT", "DMA", "DMA", "DMA", "High Touch", "High Touch", "High Touch"],
            "region": ["UK", "EU", "US", "UK", "EU", "US", "UK", "EU", "US"],
            "orders": [1240, 980, 1430, 860, 790, 1100, 420, 390, 510],
            "notional_m": [82, 71, 96, 43, 39, 56, 30, 27, 33],
            "fill_rate": [81.2, 79.4, 83.0, 76.1, 74.8, 77.9, 88.5, 87.1, 89.2],
            "slippage_bps": [4.2, 5.1, 3.9, 6.4, 6.9, 5.8, 2.8, 3.1, 2.6],
        }
    )


@cache.memoize(timeout=300)
def get_tca_execution_data() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "algo": ["VWAP", "TWAP", "Arrival", "Close", "Participation", "VWAP", "TWAP"],
            "region": ["UK", "EU", "US", "UK", "EU", "US", "UK"],
            "orders": [1800, 950, 1400, 720, 610, 1200, 870],
            "fill_rate": [84.2, 79.8, 81.3, 91.1, 76.4, 82.9, 80.5],
            "slippage_bps": [3.8, 5.6, 4.4, 2.7, 6.2, 4.1, 5.0],
            "participation_rate": [14.1, 11.5, 12.7, 18.8, 9.4, 15.0, 12.1],
        }
    )