"""Lesson 06 – Feature Engineering and Pipelines.

Learning outcomes
-----------------
- Build reusable feature engineering steps with scikit-learn pipelines.
- Combine numerical and text features.
- Understand feature union and custom transformers.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.compose import ColumnTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import FeatureUnion, Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


def create_text_length_feature(text_series: pd.Series) -> np.ndarray:
    """Return the length of each text entry as an engineered feature."""

    return text_series.fillna("").str.len().to_numpy().reshape(-1, 1)


class TextLengthTransformer(BaseEstimator, TransformerMixin):
    """Custom transformer that appends a text length feature."""

    def fit(self, X: pd.Series, y: Iterable | None = None):
        return self

    def transform(self, X: pd.Series) -> np.ndarray:
        return create_text_length_feature(pd.Series(X))


@dataclass
class FeaturePipelineBuilder:
    """Factory for constructing complex preprocessing pipelines."""

    numeric_features: list[str]
    categorical_features: list[str]
    text_feature: str

    def build(self) -> ColumnTransformer:
        numeric_transformer = Pipeline(
            steps=[("imputer", SimpleImputer(strategy="median")), ("scaler", StandardScaler())]
        )

        categorical_transformer = Pipeline(
            steps=[
                ("imputer", SimpleImputer(strategy="most_frequent")),
                ("encoder", OneHotEncoder(handle_unknown="ignore")),
            ]
        )

        text_transformer = FeatureUnion(
            transformer_list=[
                ("tfidf", TfidfVectorizer(max_features=100)),
                ("length", TextLengthTransformer()),
            ]
        )

        preprocessor = ColumnTransformer(
            transformers=[
                ("num", numeric_transformer, self.numeric_features),
                ("cat", categorical_transformer, self.categorical_features),
                ("text", text_transformer, self.text_feature),
            ]
        )

        return preprocessor


if __name__ == "__main__":
    data = pd.DataFrame(
        {
            "price": [199, 299, 159, 450],
            "category": ["electronics", "home", "electronics", "outdoors"],
            "description": [
                "Compact wireless headphones with noise cancellation",
                "Ergonomic office chair with lumbar support",
                "Portable Bluetooth speaker with long battery life",
                "Durable hiking backpack with hydration reservoir",
            ],
            "rating": [4.5, 4.0, 4.7, 4.2],
        }
    )

    builder = FeaturePipelineBuilder(
        numeric_features=["price", "rating"],
        categorical_features=["category"],
        text_feature="description",
    )

    pipeline = builder.build()
    transformed = pipeline.fit_transform(data, None)
    print("Transformed shape:", transformed.shape)
