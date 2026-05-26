# SKU Reorder Intelligence Model

> A Python/Excel inventory model that flags slow-moving SKUs 2–3 weeks before buying cycles — giving founders cash-flow visibility before purchase decisions are made.

---

## Overview

Retail founders often make purchasing decisions reactively — replenishing what's already run out, or holding excess stock on slow movers. This model flips that: it monitors 100+ SKUs continuously and surfaces early warnings before problems compound into cash-flow pressure.

Built as the sole analyst at a growing Vancouver retail brand, this was designed to be usable by non-technical founders — not just another dashboard that collects dust.

---

## Problem Statement

- Purchasing decisions were reactive, driven by stock-outs rather than demand patterns
- Slow-moving inventory was being reordered out of habit, tying up cash
- Founders had no early-warning system — problems surfaced at the buying meeting, not before

---

## Solution

A Python-driven, Excel-output model that:
1. **Tracks sales velocity** per SKU over rolling time windows
2. **Flags slow-movers** when velocity drops below category-specific thresholds
3. **Projects stock coverage** in days, triggered 2–3 weeks before the next buying cycle
4. **Outputs a clean Excel report** founders can review without opening Python

---

## How It Works

### Velocity Calculation
```python
# Rolling 4-week sales velocity per SKU
df['velocity_4w'] = df.groupby('sku_id')['units_sold'].transform(
    lambda x: x.rolling(window=4, min_periods=1).mean()
)

# Coverage in days (current stock / daily velocity)
df['days_coverage'] = df['stock_on_hand'] / (df['velocity_4w'] / 7)
```

### Flag Logic
SKUs are flagged when:
- Days of coverage < reorder lead time + buffer (configurable per category)
- Velocity has declined > 30% versus prior 4-week period
- Stock is high but velocity is low (slow-mover alert — don't reorder)

### Output
A structured Excel report with:
- Traffic-light status (🔴 Reorder Now / 🟡 Watch / 🟢 OK)
- Current stock on hand
- Projected days of coverage
- 4-week velocity trend
- Recommended action

---

## Impact

- Identified cash-flow risk from reactive purchasing patterns before it compounded
- Gave founders a structured inventory review 2–3 weeks before each buying cycle
- Reduced unplanned purchases by flagging slow movers before they were reordered

---

## Stack

- **Python** — data processing and flag logic (Pandas)
- **Excel** — output format (openpyxl for formatting)
- **Configurable thresholds** — lead time and buffer days set per category in a config file

---

## File Structure

```
sku_reorder_model/
├── src/                  # Core model logic (velocity, flags, report generation)
├── generate_data.py      # Generates synthetic inventory and sales data
└── README.md
```

---

## How to Run

```
# Clone the repo
git clone https://github.com/simranksandhu0/sku_reorder_model.git
cd sku_reorder_model

# Generate synthetic inventory data
python generate_data.py

# Run the reorder model
python src/report.py
```

---

## Configuration

Lead time and buffer thresholds are set per category directly in `src/report.py`. Adjust the `lead_time_days`, `buffer_days`, and `slow_mover_threshold` values to match your category buying cycles.

---

## Key Takeaways

- Usability was as important as the model logic — a technically correct model founders don't open solves nothing
- Category-specific thresholds outperformed a single global threshold significantly in flag accuracy
- The slow-mover alert (don't reorder this) was as valuable as the reorder alert — it prevented cash being tied up in dead stock
