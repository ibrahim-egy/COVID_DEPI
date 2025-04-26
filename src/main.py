from flask import Flask, render_template, request
from model import Model
import os


app = Flask(__name__)
app.secret = os.environ.get('SECRET')

my_model = Model()

@app.route('/')
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    if request.method == "POST":


        data = request.get_json()
        model = data['model']
        del data['model']

        label, prop = my_model.detect(model_name=model, data=data)

        return {"Model": model,"Data": data, "Prediction": str(label), "Probability (per class)": str(prop)}


if __name__ == "__main__":
    app.run(debug=True)


