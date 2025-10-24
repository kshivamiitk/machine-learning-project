"""Sample script for Lesson 01 showing how to reuse the helper functions."""

from lessons.lesson01_python_foundations import (
    DatasetSummary,
    apply_pipeline,
    clean_names,
    square,
    unique_sorted,
)

people = ["  ada", "Babbage", "  turing  ", "ada"]
print("Original names:", people)
print("Cleaned names:", clean_names(people))

summary = DatasetSummary(n_rows=500, n_columns=12, target="quality")
print("Dataset summary:", summary.describe())

values = [4, 1, 2, 2, 3]
print("Pipeline output:", apply_pipeline(values, unique_sorted, square))
