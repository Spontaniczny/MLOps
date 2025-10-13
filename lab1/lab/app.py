from fastapi import FastAPI
from src.inference import load_model, predict as model_predict
from src.api.models.irys import PredictRequest, PredictResponse


app = FastAPI()
model, class_names = load_model()


@app.get("/")
def welcome_root():
    return {"message": "Welcome to the ML API"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/predict")
def predict(request: PredictRequest) -> PredictResponse:
    prediction = model_predict(model, class_names, request.model_dump())
    return PredictResponse(prediction=prediction)
