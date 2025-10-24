"""Lesson 03 – Data Preprocessing and Exploratory Data Analysis.

Concepts covered
----------------
- Handling missing values.
- Encoding categorical variables.
- Exploratory plots and summary statistics.
- Train/validation/test splits.

The code below uses synthetic data to demonstrate each step.
"""

from __future__ import annotations

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


def load_raw_housing_data() -> pd.DataFrame:
    """Generate a small synthetic housing dataset for demonstration purposes."""

    return pd.DataFrame(
        {
            "price": [250000, 190000, 340000, None, 450000, 230000],
            "rooms": [3, 2, 4, 3, None, 2],
            "location": ["urban", "suburban", "urban", "rural", "urban", "suburban"],
            "style": ["apartment", "semi-detached", "detached", "detached", "apartment", "apartment"],
            "age_years": [12, 35, 8, 52, 5, 28],
        }
    )


def build_preprocessing_pipeline(df: pd.DataFrame) -> Pipeline:
    """Construct a preprocessing pipeline to clean the dataset."""

    numeric_features = ["rooms", "age_years"]
    categorical_features = ["location", "style"]

    numeric_transformer = Pipeline(steps=[("imputer", SimpleImputer(strategy="median")), ("scaler", StandardScaler())])
    categorical_transformer = Pipeline(
        steps=[("imputer", SimpleImputer(strategy="most_frequent")), ("encoder", OneHotEncoder(handle_unknown="ignore"))]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, numeric_features),
            ("cat", categorical_transformer, categorical_features),
        ]
    )

    return preprocessor


if __name__ == "__main__":
    from sklearn.impute import SimpleImputer

    raw = load_raw_housing_data()
    print("Raw data:\n", raw)

    train, test = train_test_split(raw, test_size=0.2, random_state=42)
    print("Train set size:", len(train), "Test set size:", len(test))

    preprocessor = build_preprocessing_pipeline(raw)
    transformed = preprocessor.fit_transform(train)
    print("Transformed feature matrix shape:", transformed.shape)

    encoded_feature_names = list(preprocessor.named_transformers_["cat"].named_steps["encoder"].get_feature_names_out())
    print("Encoded categorical features:", encoded_feature_names)
