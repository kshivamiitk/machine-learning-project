"""Lesson 08 – Deep Learning Fundamentals.

This lesson introduces the core concepts of deep learning by implementing a
minimal feed-forward neural network using only NumPy. Building the forward and
backward passes manually reinforces the mathematical foundations of gradient
based learning.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Tuple

import numpy as np


@dataclass
class DenseLayer:
    """Single dense (fully-connected) neural network layer."""

    input_dim: int
    output_dim: int
    learning_rate: float

    def __post_init__(self) -> None:
        limit = math.sqrt(6 / (self.input_dim + self.output_dim))
        self.weights = np.random.uniform(-limit, limit, (self.input_dim, self.output_dim))
        self.bias = np.zeros((1, self.output_dim))

    def forward(self, inputs: np.ndarray) -> np.ndarray:
        self.inputs = inputs
        return inputs @ self.weights + self.bias

    def backward(self, grad_output: np.ndarray) -> np.ndarray:
        grad_weights = self.inputs.T @ grad_output / len(self.inputs)
        grad_bias = grad_output.mean(axis=0, keepdims=True)
        self.weights -= self.learning_rate * grad_weights
        self.bias -= self.learning_rate * grad_bias
        return grad_output @ self.weights.T


class ReLU:
    """Rectified Linear Unit activation function."""

    def forward(self, inputs: np.ndarray) -> np.ndarray:
        self.mask = inputs > 0
        return np.maximum(0, inputs)

    def backward(self, grad_output: np.ndarray) -> np.ndarray:
        return grad_output * self.mask


class MeanSquaredError:
    """Mean squared error loss function."""

    def forward(self, predictions: np.ndarray, targets: np.ndarray) -> float:
        self.predictions = predictions
        self.targets = targets
        return float(np.mean((predictions - targets) ** 2))

    def backward(self) -> np.ndarray:
        return 2 * (self.predictions - self.targets) / len(self.targets)


@dataclass
class SimpleNeuralNetwork:
    """A two-layer neural network for regression tasks."""

    input_dim: int
    hidden_dim: int
    output_dim: int
    learning_rate: float = 0.01

    def __post_init__(self) -> None:
        self.layer1 = DenseLayer(self.input_dim, self.hidden_dim, self.learning_rate)
        self.activation = ReLU()
        self.layer2 = DenseLayer(self.hidden_dim, self.output_dim, self.learning_rate)
        self.loss = MeanSquaredError()

    def forward(self, inputs: np.ndarray) -> np.ndarray:
        hidden = self.layer1.forward(inputs)
        activated = self.activation.forward(hidden)
        output = self.layer2.forward(activated)
        return output

    def train_step(self, inputs: np.ndarray, targets: np.ndarray) -> float:
        predictions = self.forward(inputs)
        loss_value = self.loss.forward(predictions, targets)

        grad_loss = self.loss.backward()
        grad_hidden = self.layer2.backward(grad_loss)
        _ = self.activation.backward(grad_hidden)
        self.layer1.backward(_)
        return loss_value


def generate_sine_wave_data(n_samples: int = 512) -> Tuple[np.ndarray, np.ndarray]:
    """Generate a simple regression dataset based on a noisy sine wave."""

    X = np.linspace(-2 * np.pi, 2 * np.pi, n_samples).reshape(-1, 1)
    y = np.sin(X) + 0.1 * np.random.randn(*X.shape)
    return X, y


if __name__ == "__main__":
    np.random.seed(42)
    X, y = generate_sine_wave_data()
    model = SimpleNeuralNetwork(input_dim=1, hidden_dim=32, output_dim=1, learning_rate=0.05)

    for epoch in range(500):
        loss = model.train_step(X, y)
        if epoch % 100 == 0:
            print(f"Epoch {epoch:03d} – Loss: {loss:.4f}")

    final_loss = model.train_step(X, y)
    print(f"Final loss: {final_loss:.4f}")
