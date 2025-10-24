"""Sample script for Lesson 04 running regression and classification helpers."""

from lessons.lesson04_supervised_learning import train_classification_model, train_regression_model

print("Training regression model (may take a moment)...")
regression_results = train_regression_model()
print(regression_results)

print("Training classification model...")
classification_results = train_classification_model()
print(classification_results)
