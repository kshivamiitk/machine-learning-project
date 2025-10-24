"""Lesson 09 – Model Deployment and Monitoring.

In this module we focus on the operational side of machine learning:
packaging models, creating prediction services, and monitoring drift.
The code snippets illustrate lightweight patterns using FastAPI.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import joblib
import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel
from sklearn.datasets import load_diabetes
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

MODEL_PATH = Path("models/linear_regression_diabetes.joblib")


@dataclass
class ModelTrainer:
    """Train and persist a simple regression model."""

    model_path: Path = MODEL_PATH

    def train_and_save(self) -> None:
        data = load_diabetes()
        X_train, X_test, y_train, y_test = train_test_split(data.data, data.target, test_size=0.2, random_state=42)

        model = LinearRegression()
        model.fit(X_train, y_train)
        self.model_path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump({"model": model, "feature_names": data.feature_names}, self.model_path)


class PredictionRequest(BaseModel):
    """Schema for incoming prediction requests."""

    features: list[float]


class PredictionResponse(BaseModel):
    """Schema for model predictions."""

    prediction: float


class ModelService:
    """Lightweight service wrapper around a scikit-learn model."""

    def __init__(self, model_path: Path = MODEL_PATH) -> None:
        self.model_artifact = joblib.load(model_path)
        self.model: LinearRegression = self.model_artifact["model"]
        self.feature_names = self.model_artifact["feature_names"]

    def predict(self, features: list[float]) -> float:
        array = np.array(features).reshape(1, -1)
        return float(self.model.predict(array)[0])


app = FastAPI(title="ML Deployment Lesson")
service = None


@app.on_event("startup")
def load_model() -> None:
    global service
    if not MODEL_PATH.exists():
        ModelTrainer().train_and_save()
    service = ModelService()


@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest) -> PredictionResponse:
    if service is None:
        raise RuntimeError("Model service not initialised")
    prediction = service.predict(request.features)
    return PredictionResponse(prediction=prediction)


if __name__ == "__main__":
    # Demonstrate offline scoring for learners without FastAPI available.
    trainer = ModelTrainer()
    if not MODEL_PATH.exists():
        trainer.train_and_save()
    service = ModelService()
    sample = [0.03807591, 0.05068012, 0.06169621, 0.02187235, -0.0442235, -0.03482076, -0.04340085, -0.00259226, 0.01990842, -0.01764613]
    print("Sample prediction:", service.predict(sample))
