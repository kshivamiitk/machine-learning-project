"""Sample script for Lesson 05 computing evaluation metrics."""

from lessons.lesson05_model_evaluation import compute_learning_curve, evaluate_with_cross_validation

cv_summary = evaluate_with_cross_validation()
print("Cross-validation summary:\n", cv_summary)

curve = compute_learning_curve()
print("Learning curve:\n", curve)
