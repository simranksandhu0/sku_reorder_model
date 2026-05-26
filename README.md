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
sku-reorder-model/
├── data/
│   └── sample_inventory.csv        # Anonymised sample data
├── src/
│   ├── velocity.py                 # Sales velocity calculations
│   ├── flags.py                    # Reorder flag logic
│   └── report.py                   # Excel output generation
├── config/
│   └── thresholds.yaml             # Lead time and buffer settings per category
├── outputs/
│   └── sample_reorder_report.xlsx  # Example output
├── notebooks/
│   └── model_walkthrough.ipynb     # End-to-end walkthrough
├── requirements.txt
└── README.md
```

---

## How to Run

```bash
git clone https://github.com/your-username/sku-reorder-model.git
cd sku-reorder-model

pip install -r requirements.txt
# requirements.txt should include: pandas, openpyxl, pyyaml, jupyter

# Run the full pipeline
python src/report.py --input data/sample_inventory.csv --output outputs/reorder_report.xlsx
```

---

## Configuration

Edit `config/thresholds.yaml` to set category-specific lead times and buffer days:

```yaml
categories:
  apparel:
    lead_time_days: 14
    buffer_days: 7
    slow_mover_threshold: 0.3   # Flag if velocity drops 30% vs prior period
  accessories:
    lead_time_days: 10
    buffer_days: 5
    slow_mover_threshold: 0.25
```

---

## Key Takeaways

- Usability was as important as the model logic — a technically correct model founders don't open solves nothing
- Category-specific thresholds outperformed a single global threshold significantly in flag accuracy
- The slow-mover alert (don't reorder this) was as valuable as the reorder alert — it prevented cash being tied up in dead stock
