"""Sample script for Lesson 07 demonstrating clustering and PCA."""

from lessons.lesson07_unsupervised_learning import perform_clustering, reduce_dimensions

metrics = perform_clustering(k=3)
print("KMeans metrics:", metrics)

projected = reduce_dimensions()
print(projected.head())
