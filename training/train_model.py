import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression

from utils.feature_extraction import extract_lexical_features


# Load dataset
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
dataset_path = os.path.join(BASE_DIR, "dataset", "malicious_phish.csv")

data = pd.read_csv(dataset_path)

# Convert labels without modifying dataset
data['label'] = data['type'].apply(lambda x: 0 if x == 'benign' else 1)

urls = data['url']
labels = data['label']

processed_urls = []

# Combine URL + lexical features
for url in urls:
    features = extract_lexical_features(url)
    feature_string = url + " " + " ".join(map(str, features))
    processed_urls.append(feature_string)


# Convert text to vectors
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(processed_urls)
y = labels


# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)


# Train Random Forest
rf_model = RandomForestClassifier(n_estimators=100)
rf_model.fit(X_train, y_train)


# Train Logistic Regression
lr_model = LogisticRegression(max_iter=1000)
lr_model.fit(X_train, y_train)


# Save models
models_path = os.path.join(BASE_DIR, "models")

joblib.dump(rf_model, os.path.join(models_path, "random_forest_model.pkl"))
joblib.dump(lr_model, os.path.join(models_path, "logistic_regression_model.pkl"))
joblib.dump(vectorizer, os.path.join(models_path, "vectorizer.pkl"))


print("Training complete.")
print("Models saved in models folder.")