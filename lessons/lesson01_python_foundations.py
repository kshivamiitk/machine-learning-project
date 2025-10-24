"""Lesson 01 – Python Foundations for Machine Learning.

This lesson reviews the core Python language features that data scientists
use daily. Run the module directly to see examples of control flow, functions,
list comprehensions, generator expressions, and simple unit-style tests.

Key takeaways
-------------
1. Python syntax refresher (variables, types, loops, conditionals).
2. Working with iterables, comprehensions, and generators to write concise code.
3. Building reusable functions and lightweight classes for data workflows.
4. Leveraging the built-in ``unittest`` module to validate behaviour.

Recommended reading
-------------------
- Official Python tutorial: https://docs.python.org/3/tutorial/
- Fluent Python by Luciano Ramalho (O'Reilly)
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterable, List


def clean_names(raw_names: Iterable[str]) -> List[str]:
    """Normalise a sequence of raw names.

    Parameters
    ----------
    raw_names:
        Any iterable of strings, e.g. a list from a CSV column.

    Returns
    -------
    list of str
        Title-cased names stripped of leading/trailing whitespace.
    """

    return [name.strip().title() for name in raw_names if name]


@dataclass
class DatasetSummary:
    """A lightweight structure that keeps track of dataset metadata."""

    n_rows: int
    n_columns: int
    target: str | None = None

    def describe(self) -> str:
        """Return a human-readable description of the dataset."""

        parts = [f"Rows: {self.n_rows}", f"Columns: {self.n_columns}"]
        if self.target:
            parts.append(f"Target: {self.target}")
        return " | ".join(parts)


def apply_pipeline(data: Iterable[int], *steps: Callable[[Iterable[int]], Iterable[int]]) -> List[int]:
    """Apply a sequence of functions to a dataset.

    This mimics a very small portion of scikit-learn's pipeline mechanism and
    illustrates the power of higher-order functions in Python.
    """

    for step in steps:
        data = step(data)
    return list(data)


def unique_sorted(values: Iterable[int]) -> Iterable[int]:
    """Yield unique values in sorted order using generator semantics."""

    return (value for value in sorted(set(values)))


def square(values: Iterable[int]) -> Iterable[int]:
    """Square a stream of integers lazily."""

    return (value**2 for value in values)


if __name__ == "__main__":
    people = [" alice", "Bob", "eve ", "alice"]
    print("Original names:", people)
    print("Cleaned names:", clean_names(people))

    summary = DatasetSummary(n_rows=1000, n_columns=42, target="price")
    print("Dataset summary:", summary.describe())

    numbers = [5, 1, 3, 3, 2]
    transformed = apply_pipeline(numbers, unique_sorted, square)
    print("Transformed pipeline output:", transformed)

    assert clean_names(["alice"]) == ["Alice"]
    assert summary.describe() == "Rows: 1000 | Columns: 42 | Target: price"
    assert transformed == [1, 4, 9, 25]
    print("All simple assertions passed.")
