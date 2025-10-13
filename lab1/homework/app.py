import joblib
from fastapi import FastAPI

from src.api.api import PredictRequest, PredictResponse
from sentence_transformers import SentenceTransformer

app = FastAPI()
sentence_transformer = SentenceTransformer("models/sentence_transformer.model")
classifier = joblib.load("models/classifier.joblib")
classes = ["negative", "neutral", "positive"]


@app.post("/predict")
def predict(request: PredictRequest) -> PredictResponse:
    embedding = sentence_transformer.encode(request.model_dump()["text"])
    prediction = classifier.predict(embedding.reshape(1, -1))
    return PredictResponse(prediction=classes[prediction[0]])
