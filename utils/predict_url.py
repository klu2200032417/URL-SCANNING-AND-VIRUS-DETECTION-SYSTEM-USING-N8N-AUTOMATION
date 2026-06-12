import joblib
import re

# Load the saved model and vectorizer
print("Loading trained model and vectorizer...")
model = joblib.load('../models/random_forest_model.pkl')
vectorizer = joblib.load('../models/vectorizer.pkl')

# Define the exact same feature extraction function used during training
def extract_lexical_features(url):
    features = []
    features.append(len(url))
    features.append(len(re.findall(r'[.-_@?=&]', url)))
    suspicious_keywords = ['login', 'secure', 'account', 'update', 'signin', 'banking']
    features.append(1 if any(keyword in url.lower() for keyword in suspicious_keywords) else 0)
    try:
        hostname = url.split('/')[2]
        features.append(1 if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', hostname) else 0)
    except IndexError:
        features.append(0)
    return ' '.join(map(str, features))

# Function to make a prediction on a single URL
def predict_url(url_to_check):
    features_for_prediction = url_to_check + ' ' + extract_lexical_features(url_to_check)
    vectorized_features = vectorizer.transform([features_for_prediction])
    prediction = model.predict(vectorized_features)
    return "Malicious" if prediction[0] == 1 else "Safe"

# Main part of the script
if __name__ == "__main__":
    input_url = input("Enter the URL you want to check: ")
    result = predict_url(input_url)
    print(f"The URL '{input_url}' is classified as: {result}")