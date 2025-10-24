"""Sample script for Lesson 08 training the simple neural network."""

import numpy as np

from lessons.lesson08_deep_learning import SimpleNeuralNetwork, generate_sine_wave_data

np.random.seed(0)
X, y = generate_sine_wave_data(128)
model = SimpleNeuralNetwork(input_dim=1, hidden_dim=16, output_dim=1, learning_rate=0.05)

for epoch in range(200):
    loss = model.train_step(X, y)
    if epoch % 50 == 0:
        print(f"Epoch {epoch:03d} – Loss: {loss:.4f}")
