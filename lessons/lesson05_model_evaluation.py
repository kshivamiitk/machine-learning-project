"""Lesson 05 – Model Evaluation and Validation Strategies.

Topics
------
- Bias-variance trade-off.
- Cross-validation techniques.
- Regression and classification metrics.
- Learning curves for diagnosing under/overfitting.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.datasets import load_diabetes
from sklearn.linear_model import Ridge
from sklearn.model_selection import KFold, cross_validate, learning_curve


def evaluate_with_cross_validation() -> pd.DataFrame:
    """Return cross-validation metrics for a Ridge regression model."""

    data = load_diabetes()
    model = Ridge(alpha=1.0)
    scoring = {"rmse": "neg_root_mean_squared_error", "mae": "neg_mean_absolute_error"}
    cv_results = cross_validate(model, data.data, data.target, cv=KFold(n_splits=5, shuffle=True, random_state=42), scoring=scoring)

    results = pd.DataFrame(cv_results)
    results["rmse"] = -results["test_rmse"]
    results["mae"] = -results["test_mae"]
    return results[["rmse", "mae", "fit_time", "score_time"]]


def compute_learning_curve() -> pd.DataFrame:
    """Compute a learning curve for the Ridge regression model."""

    data = load_diabetes()
    train_sizes, train_scores, validation_scores = learning_curve(
        Ridge(alpha=1.0),
        data.data,
        data.target,
        cv=5,
        scoring="neg_root_mean_squared_error",
        train_sizes=np.linspace(0.1, 1.0, 5),
        shuffle=True,
        random_state=42,
    )

    curve = pd.DataFrame(
        {
            "train_size": train_sizes,
            "train_rmse": -np.mean(train_scores, axis=1),
            "validation_rmse": -np.mean(validation_scores, axis=1),
        }
    )
    return curve


if __name__ == "__main__":
    cv_summary = evaluate_with_cross_validation()
    print("Cross-validation summary:\n", cv_summary)

    learning_curve_df = compute_learning_curve()
    print("Learning curve:\n", learning_curve_df)
