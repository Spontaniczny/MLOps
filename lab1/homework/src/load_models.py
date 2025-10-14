import joblib
import os
from pathlib import Path

from sentence_transformers import SentenceTransformer


SCRIPT_DIR = str(Path(os.path.dirname(os.path.abspath(__file__))).parent)

SENTENCE_TRANSFORMER_PATH = SCRIPT_DIR + "/models/sentence_transformer.model"
CLASSIFIER_PATH = SCRIPT_DIR + "/models/classifier.joblib"


def load_sentence_transformer(filename=SENTENCE_TRANSFORMER_PATH):
    if not os.path.isdir(SENTENCE_TRANSFORMER_PATH):
        raise FileNotFoundError(f"Model directory not found at: {filename}")
    return SentenceTransformer(filename)


def load_classifier(filename=CLASSIFIER_PATH):
    if not os.path.exists(filename):
        raise FileNotFoundError(f"Model file not found at: {filename}.")

    return joblib.load(filename)
