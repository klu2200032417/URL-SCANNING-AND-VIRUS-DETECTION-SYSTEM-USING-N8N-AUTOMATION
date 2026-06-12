from flask import Flask, request, jsonify

from algorithms.blacklist import check_blacklist
from algorithms.lexical_analysis import lexical_detect
from algorithms.random_forest_detector import rf_predict
from algorithms.logistic_regression_detector import lr_predict

app = Flask(__name__)


@app.route("/predict", methods=["GET"])
def predict():

    url = request.args.get("url")

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    # Run all algorithms
    blacklist_result = check_blacklist(url)
    lexical_result = lexical_detect(url)
    rf_result = rf_predict(url)
    lr_result = lr_predict(url)

    results = {
        "blacklist": bool(blacklist_result),
        "lexical_analysis": bool(lexical_result),
        "random_forest": bool(rf_result),
        "logistic_regression": bool(lr_result)
    }

    # Count malicious detections
    malicious_count = sum(1 for v in results.values() if v)

    total_algorithms = 4
    malicious_score = (malicious_count / total_algorithms) * 100

    # Final verdict
    if malicious_score >= 50:
        verdict = "Malicious"
    else:
        verdict = "Benign"

    response = {
        "url": url,
        "results": results,
        "malicious_score": malicious_score,
        "final_verdict": verdict
    }

    return jsonify(response)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)