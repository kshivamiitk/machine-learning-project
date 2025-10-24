"""Lesson 07 – Unsupervised Learning Techniques.

We explore clustering and dimensionality reduction using scikit-learn. The
lesson highlights practical tips for choosing the number of clusters and for
interpreting principal components.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.datasets import load_iris
from sklearn.metrics import silhouette_score


def perform_clustering(k: int = 3) -> dict[str, float]:
    """Cluster the Iris dataset and compute the silhouette score."""

    data = load_iris()
    model = KMeans(n_clusters=k, random_state=42, n_init="auto")
    labels = model.fit_predict(data.data)
    score = float(silhouette_score(data.data, labels))
    return {"inertia": float(model.inertia_), "silhouette": score}


def reduce_dimensions(n_components: int = 2) -> pd.DataFrame:
    """Return the Iris dataset projected onto principal components."""

    data = load_iris()
    pca = PCA(n_components=n_components, random_state=42)
    components = pca.fit_transform(data.data)

    projected = pd.DataFrame(components, columns=[f"PC{i+1}" for i in range(n_components)])
    projected["target"] = data.target
    return projected


if __name__ == "__main__":
    clustering_metrics = perform_clustering()
    print("Clustering metrics:", clustering_metrics)

    projected_df = reduce_dimensions()
    print("Projected data head:\n", projected_df.head())
