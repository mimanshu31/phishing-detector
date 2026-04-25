from flask import Flask, render_template, request
import joblib

app = Flask(__name__)

# ===== LOAD MODEL =====
model = joblib.load("model.pkl")


# ===== URL VALIDATION =====
def is_valid_url(url):
    return url.startswith("http://") or url.startswith("https://")


# ===== FEATURE EXTRACTION =====
def extract_features(url):
    url = url.strip()

    length = len(url)
    https = 1 if url.startswith("https") else 0
    at = 1 if "@" in url else 0
    dash = 1 if "-" in url else 0
    dots = url.count(".")

    return [length, https, at, dash, dots]


# ===== RISK CALCULATION =====
def calculate_risk(features):
    length, https, at, dash, dots = features
    risk = 0
    reasons = []

    if https == 0:
        risk += 20
        reasons.append("No HTTPS (Not Secure)")

    if at == 1:
        risk += 30
        reasons.append("Contains '@' symbol")

    if dash == 1:
        risk += 15
        reasons.append("Contains '-' (dash)")

    if dots > 3:
        risk += 15
        reasons.append("Too many dots in URL")

    if length > 50:
        risk += 20
        reasons.append("URL is too long")

    return risk, reasons


# ===== ROUTE =====
@app.route("/", methods=["GET", "POST"])
def home():
    result = ""
    risk = 0
    reasons = []

    if request.method == "POST":
        url = request.form.get("url")

        # VALIDATION
        if not is_valid_url(url):
            result = "Invalid URL"
            return render_template("index.html", result=result, risk=risk, reasons=reasons)

        # FEATURES
        features = extract_features(url)

        # PREDICTION
        prediction = model.predict([features])[0]

        # RESULT
        if prediction == 1:
            result = "Phishing Website"
        else:
            result = "Safe Website"

        # RISK CALCULATION
        risk, reasons = calculate_risk(features)

    return render_template("index.html", result=result, risk=risk, reasons=reasons)


# ===== RUN APP =====
if __name__ == "__main__":
    app.run(debug=True)