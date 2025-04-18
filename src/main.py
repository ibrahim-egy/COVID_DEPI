from flask import Flask, render_template, request
import os
app = Flask(__name__)
app.secret = os.environ.get('SECRET')

@app.route('/')
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    if request.method == "POST":


        data = request.form.to_dict()
        print(data)
        return data



if __name__ == "__main__":
    app.run(debug=True)


