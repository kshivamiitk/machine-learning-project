"""Sample script for Lesson 02 demonstrating NumPy and Pandas helpers."""

import numpy as np
import pandas as pd

from lessons.lesson02_numpy_pandas import basic_statistics, engineer_features, normalise

np.random.seed(7)
prices = np.random.lognormal(mean=11, sigma=0.5, size=5)
print("Summary stats:", basic_statistics(prices))
print("Normalised prices:", normalise(prices))

housing = pd.DataFrame({"price": prices, "rooms": [2, 3, 2, 4, 3]})
housing["location"] = ["urban", "suburban", "urban", "rural", "urban"]
features = engineer_features(housing)
print(features)
