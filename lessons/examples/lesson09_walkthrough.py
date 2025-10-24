"""Sample script for Lesson 09 performing an offline prediction."""

from lessons.lesson09_model_deployment import ModelService, ModelTrainer, MODEL_PATH

trainer = ModelTrainer()
if not MODEL_PATH.exists():
    trainer.train_and_save()

service = ModelService()
sample = [0.03807591, 0.05068012, 0.06169621, 0.02187235, -0.0442235, -0.03482076, -0.04340085, -0.00259226, 0.01990842, -0.01764613]
print("Sample prediction:", service.predict(sample))
