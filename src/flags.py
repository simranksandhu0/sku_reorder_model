"""
flags.py
Applies category-specific thresholds to flag SKUs as:
  - REORDER NOW  : days of coverage < lead_time + buffer
  - SLOW MOVER   : velocity declined > threshold AND stock is high
  - WATCH        : days of coverage is tight but not yet critical
  - OK           : no action needed
"""

import yaml
import pandas as pd
import numpy as np
from pathlib import Path


def load_thresholds(path: str = "config/thresholds.yaml") -> dict:
    """Load category-level threshold config."""
    if not Path(path).exists():
        raise FileNotFoundError(f"{path} not found.")
    with open(path, "r") as f:
        config = yaml.safe_load(f)
    return config["categories"]


def compute_days_coverage(df: pd.DataFrame) -> pd.DataFrame:
    """
    Days of coverage = stock_on_hand / recent_velocity_daily.
    Where velocity is 0, set coverage to 999 (no demand = no urgency to reorder).
    """
    df = df.copy()
    df["days_coverage"] = np.where(
        df["recent_velocity_daily"] > 0,
        (df["stock_on_hand"] / df["recent_velocity_daily"]).round(1),
        999.0,
    )
    return df


def apply_flags(df: pd.DataFrame, thresholds: dict) -> pd.DataFrame:
    """
    Assign status flag and recommended action per SKU based on
    category-specific thresholds from config.
    """
    df = df.copy()
    flags = []
    actions = []

    for _, row in df.iterrows():
        cat = row["category"]
        config = thresholds.get(cat, {})

        lead  = config.get("lead_time_days", 14)
        buf   = config.get("buffer_days", 7)
        slow  = config.get("slow_mover_threshold", 0.30)
        cover = row["days_coverage"]
        vel_chg = row["velocity_change_pct"]

        critical_days = lead + buf

        if vel_chg <= -slow and cover > critical_days:
            flag   = "SLOW MOVER"
            action = "Do NOT reorder — velocity declining. Review stock."
        elif cover <= lead:
            flag   = "REORDER NOW"
            action = f"Reorder immediately — only {cover:.0f} days left (lead time: {lead}d)."
        elif cover <= critical_days:
            flag   = "WATCH"
            action = f"Monitor closely — {cover:.0f} days coverage, buffer is {buf}d."
        else:
            flag   = "OK"
            action = "No action needed."

        flags.append(flag)
        actions.append(action)

    df["status"] = flags
    df["recommended_action"] = actions
    return df
