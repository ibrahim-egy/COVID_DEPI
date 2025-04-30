from flask import Flask, render_template, request
import os
import requests

API_URL = "https://jojoTH-covid.hf.space/predict"

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET')


@app.route('/')
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    if request.method == "POST":
        data = request.get_json()

        payload = {
            "model_name": data['model'],
            "input_data": {k: v for k, v in data.items() if k != 'model'}
        }

        try:
            response = requests.post(API_URL, json=payload)
            response.raise_for_status()

            return {"Model": data['model'], "Prediction": response.json()["prediction"], "Probability": response.json()["probabilities"]}


        except requests.exceptions.RequestException as e:
            print("Error contacting the Hugging Face API:", e)
            return {"error": "Failed to connect to prediction server."}, 500




if __name__ == "__main__":
    app.run(debug=True)