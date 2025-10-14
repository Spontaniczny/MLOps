import pytest

from ..src.load_models import load_classifier, load_sentence_transformer


def test_loading_sentence_transformer():
    try:
        load_sentence_transformer()
    except Exception as e:
        pytest.fail(f"Failed to load model: {e}")


def test_loading_classifier():
    try:
        load_classifier()
    except Exception as e:
        pytest.fail(f"Failed to load model: {e}")
