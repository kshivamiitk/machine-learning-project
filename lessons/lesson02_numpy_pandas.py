"""Lesson 02 – Numerical Computing with NumPy and Pandas.

Objectives
----------
- Become comfortable with vectorised operations in NumPy.
- Understand tabular data manipulations with Pandas DataFrames.
- Learn idiomatic patterns for filtering, aggregating, and reshaping data.

Running the module executes short demonstrations that showcase the material.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def basic_statistics(array: np.ndarray) -> dict[str, float]:
    """Return descriptive statistics for an array."""

    return {
        "mean": float(np.mean(array)),
        "std": float(np.std(array, ddof=1)),
        "min": float(np.min(array)),
        "max": float(np.max(array)),
    }


def normalise(array: np.ndarray) -> np.ndarray:
    """Scale an array to zero mean and unit variance."""

    mean = np.mean(array)
    std = np.std(array)
    if std == 0:
        raise ValueError("Cannot normalise an array with zero variance")
    return (array - mean) / std


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """Create additional columns using vectorised Pandas operations."""

    engineered = df.copy()
    engineered["price_per_room"] = engineered["price"] / engineered["rooms"]
    engineered["is_expensive"] = engineered["price"] > engineered["price"].median()
    engineered["log_price"] = np.log1p(engineered["price"])
    return engineered


if __name__ == "__main__":
    np.random.seed(42)
    prices = np.random.lognormal(mean=11, sigma=0.4, size=10)
    stats = basic_statistics(prices)
    print("NumPy statistics:", stats)
    print("Normalised prices:", normalise(prices))

    housing = pd.DataFrame(
        {
            "price": prices,
            "rooms": np.random.randint(1, 5, size=10),
            "location": ["urban", "suburban", "urban", "rural", "urban", "rural", "suburban", "urban", "rural", "urban"],
        }
    )
    engineered = engineer_features(housing)
    print("Engineered features:\n", engineered)
    summary = engineered.groupby("location")["price"].agg(["mean", "median", "count"])
    print("Aggregated summary:\n", summary)
