import joblib
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression

MODEL_FILENAME = "iris_classifier.joblib"
CLASS_NAMES = load_iris().target_names.tolist()


def load_data():
    iris = load_iris()
    X, y = iris.data, iris.target
    return X, y


def train_model(X, y):
    model = LogisticRegression(max_iter=5000, random_state=42)
    model.fit(X, y)
    return model


def save_model(model, filename=MODEL_FILENAME):
    data_to_save = {"model": model, "class_names": CLASS_NAMES}
    joblib.dump(data_to_save, filename)


if __name__ == "__main__":
    X, y = load_data()
    trained_model = train_model(X, y)
    save_model(trained_model)
