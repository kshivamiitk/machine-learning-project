"""Sample script for Lesson 03 to run the preprocessing pipeline."""

from lessons.lesson03_data_preprocessing import build_preprocessing_pipeline, load_raw_housing_data

raw = load_raw_housing_data()
preprocessor = build_preprocessing_pipeline(raw)
transformed = preprocessor.fit_transform(raw)
print("Transformed shape:", transformed.shape)
encoded_feature_names = preprocessor.named_transformers_["cat"].named_steps["encoder"].get_feature_names_out()
print("Categorical features:", list(encoded_feature_names))
