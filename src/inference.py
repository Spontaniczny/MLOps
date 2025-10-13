import joblib
import os
from src.api.models.irys import PredictRequest

MODEL_FILENAME = "src/iris_classifier.joblib"


def load_model(filename=MODEL_FILENAME):
    if not os.path.exists(filename):
        raise FileNotFoundError(
            f"Model file not found at: {filename}. Please run training.py first."
        )

    loaded_data = joblib.load(filename)
    model = loaded_data["model"]
    class_names = loaded_data["class_names"]
    return model, class_names


def predict(model, class_names, features) -> str:
    feature_array = [[features[key] for key in PredictRequest.model_fields.keys()]]
    predicted_index = model.predict(feature_array)[0]
    predicted_class = class_names[predicted_index]
    return predicted_class
