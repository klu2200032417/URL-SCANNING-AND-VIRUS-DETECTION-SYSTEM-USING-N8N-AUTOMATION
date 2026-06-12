import joblib
import os
from utils.feature_extraction import extract_lexical_features

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

lr_model = joblib.load(os.path.join(BASE_DIR, "models", "logistic_regression_model.pkl"))
vectorizer = joblib.load(os.path.join(BASE_DIR, "models", "vectorizer.pkl"))


def lr_predict(url):
    features = extract_lexical_features(url)
    feature_string = url + " " + " ".join(map(str, features))

    vector = vectorizer.transform([feature_string])
    result = lr_model.predict(vector)[0]

    return result == 1