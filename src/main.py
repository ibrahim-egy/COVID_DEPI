from flask import Flask, render_template, request
import os
import requests

# 1. Set your Hugging Face API URL
API_URL = "https://jojoTH-covid.hf.space/predict"

# 2. Flask app setup
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET')


@app.route('/')
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    if request.method == "POST":
        data = request.get_json()

        # Build the payload correctly
        payload = {
            "model_name": data['model'],     # fix the model key
            "input_data": {k: v for k, v in data.items() if k != 'model'}  # rest goes into input_data
        }

        print("Payload sent to Hugging Face:", payload)  # Debugging

        try:
            response = requests.post(API_URL, json=payload)
            response.raise_for_status()

            return {"Model": data['model'], "Prediction": response.json()["prediction"], "Probability (per class)": response.json()["probabilities"]}


        except requests.exceptions.RequestException as e:
            print("Error contacting the Hugging Face API:", e)
            return {"error": "Failed to connect to prediction server."}, 500




if __name__ == "__main__":
    app.run(debug=True)