"""
generate_data.py
Generates synthetic SKU-level inventory and sales data.
Saves to data/inventory.csv
"""

import numpy as np
import pandas as pd
from pathlib import Path

SEED = 42
N_SKUS = 120
WEEKS = 16  # 16 weeks of weekly sales history

CATEGORIES = ["Apparel", "Accessories", "Footwear"]


def generate_inventory_data(seed: int = SEED) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    records = []

    for sku_num in range(1, N_SKUS + 1):
        sku_id   = f"SKU{str(sku_num).zfill(4)}"
        category = rng.choice(CATEGORIES)

        # Base weekly demand units (varies by SKU)
        base_demand = rng.integers(5, 50)

        # Stock on hand
        stock_on_hand = rng.integers(0, 200)

        # Generate weekly sales for this SKU
        weekly_sales = []
        for w in range(WEEKS):
            noise = rng.normal(0, base_demand * 0.2)
            # Some SKUs have declining demand (slow movers)
            trend = -0.5 if sku_num % 5 == 0 else 0.0
            units = max(0, int(base_demand + trend * w + noise))
            weekly_sales.append(units)

        records.append({
            "sku_id":        sku_id,
            "category":      category,
            "stock_on_hand": int(stock_on_hand),
            **{f"week_{w+1}_sales": weekly_sales[w] for w in range(WEEKS)},
        })

    df = pd.DataFrame(records)
    return df


if __name__ == "__main__":
    Path("data").mkdir(exist_ok=True)
    df = generate_inventory_data()
    df.to_csv("data/inventory.csv", index=False)
    print(f"Saved {len(df):,} SKU records to data/inventory.csv")
    print(df[["sku_id", "category", "stock_on_hand"]].head(10))
