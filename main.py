from flask import Flask, request, render_template
import pickle
import numpy as np
import time

app = Flask(__name__)

with open("california_house_price_mode.pkl", "rb") as f:
    model = pickle.load(f)

# @app.route("/predict", methods=["POST"])
# def predict():
#     data = request.get_json()
#     features = np.array([data["features"]])
#     prediction = model.predict(features)
#     return jsonify({"Price": prediction[0]})

@app.route("/", methods=["GET", "POST"])
def home():
    prediction = None
    error = None

    if request.method == "POST":
        try:
            features = [
                float(request.form["medinc"]),
                float(request.form["houseage"]),
                float(request.form["averooms"]),
                float(request.form["avebedrms"]),
                float(request.form["population"]),
                float(request.form["aveoccup"]),
                float(request.form["latitude"]),
                float(request.form["longitude"]),
            ]

            if any(x < 0 for x in features[:6]):
                error = "Features (except latitude/longitude) cannot be negative!"
            else:
                features_array = np.array([features])
                time.sleep(1)  # Simulate processing delay (remove in production)
                prediction = model.predict(features_array)[0]
                prediction = f"${prediction * 100000: .2f}"

        except ValueError:
            error = "Please enter valid numbers!"

        except KeyError as e:
            error = f"Missing field: {str(e)}"

    return render_template("index.html", prediction=prediction, error=error)

if __name__ == '__main__':
    app.run(debug=True)

# {"features": [8.3252, 41.0, 6.9841, 1.0238, 322.0, 2.5556, 37.88, -122.23]}