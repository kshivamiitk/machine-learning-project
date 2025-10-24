"""Sample script for Lesson 06 building the feature engineering pipeline."""

import pandas as pd

from lessons.lesson06_feature_engineering import FeaturePipelineBuilder

data = pd.DataFrame(
    {
        "price": [99, 120, 80],
        "rating": [4.8, 4.2, 4.5],
        "category": ["books", "electronics", "books"],
        "description": [
            "Inspirational data science handbook",
            "Noise-cancelling headphones",
            "Python best practices guide",
        ],
    }
)

builder = FeaturePipelineBuilder(
    numeric_features=["price", "rating"],
    categorical_features=["category"],
    text_feature="description",
)

pipeline = builder.build()
features = pipeline.fit_transform(data)
print("Feature matrix shape:", features.shape)
