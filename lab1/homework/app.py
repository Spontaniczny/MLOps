from fastapi import FastAPI
from starlette.responses import JSONResponse

from src.api.models.model import PredictRequest, PredictResponse
from src.load_models import load_classifier, load_sentence_transformer


app = FastAPI()
sentence_transformer = load_sentence_transformer()
classifier = load_classifier()
classes = ["negative", "neutral", "positive"]


@app.post("/predict")
def predict(request: PredictRequest):
    res_dump = request.model_dump()
    value = res_dump.get("text", None)

    if type(value) is not str or value == "":
        return JSONResponse(
            content={"message": "Invalid or empty string"}, status_code=422
        )

    embedding = sentence_transformer.encode(res_dump["text"])
    prediction = classifier.predict(embedding.reshape(1, -1))
    return PredictResponse(prediction=classes[prediction[0]])
