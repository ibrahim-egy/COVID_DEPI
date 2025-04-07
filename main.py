from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def home():
    return render_template("index.html")


@app.route("/detect", methods=["POST"])
def detect():
    if request.method == "POST":

        data = request.body[""]
        return {"detections" : 'data'}



if __name__ == "__main__":
    app.run(debug=True)


