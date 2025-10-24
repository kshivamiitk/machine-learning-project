"""Lesson 04 – Supervised Learning Workflows.

This module demonstrates a complete supervised learning pipeline using
scikit-learn. It covers regression and classification examples, emphasising
model training, hyper-parameter tuning, and evaluation.
"""

from __future__ import annotations

import numpy as np
from sklearn.datasets import fetch_california_housing, load_wine
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import accuracy_score, mean_squared_error
from sklearn.model_selection import GridSearchCV, train_test_split


def train_regression_model() -> dict[str, float]:
    """Train a random forest regressor on the California housing dataset."""

    data = fetch_california_housing()
    X_train, X_test, y_train, y_test = train_test_split(data.data, data.target, test_size=0.2, random_state=42)

    model = RandomForestRegressor(random_state=42)
    param_grid = {"n_estimators": [50, 100], "max_depth": [None, 8, 16]}
    search = GridSearchCV(model, param_grid, cv=5, n_jobs=-1)
    search.fit(X_train, y_train)

    predictions = search.predict(X_test)
    rmse = float(np.sqrt(mean_squared_error(y_test, predictions)))
    return {"rmse": rmse, "best_params": search.best_params_}


def train_classification_model() -> dict[str, float]:
    """Train a random forest classifier on the wine dataset."""

    data = load_wine()
    X_train, X_test, y_train, y_test = train_test_split(data.data, data.target, test_size=0.2, random_state=42, stratify=data.target)

    model = RandomForestClassifier(random_state=42)
    param_grid = {"n_estimators": [100, 200], "max_depth": [None, 8, 16]}
    search = GridSearchCV(model, param_grid, cv=5, n_jobs=-1)
    search.fit(X_train, y_train)

    predictions = search.predict(X_test)
    accuracy = float(accuracy_score(y_test, predictions))
    return {"accuracy": accuracy, "best_params": search.best_params_}


if __name__ == "__main__":
    regression_results = train_regression_model()
    print("Regression results:", regression_results)

    classification_results = train_classification_model()
    print("Classification results:", classification_results)
