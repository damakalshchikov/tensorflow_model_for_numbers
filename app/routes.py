from flask import Blueprint, request, jsonify, render_template
import numpy as np
from PIL import Image
from io import BytesIO
import base64
from .utils import preprocess_image
from .model_loader import model

main = Blueprint("main", __name__)


@main.route("/")
def index():
    return render_template("index.html")


@main.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        img_data = data["image"].split(",")[1]
        img_bytes = base64.b64decode(img_data)
        img = Image.open(BytesIO(img_bytes)).convert("L")

        processed_img = preprocess_image(img)

        predictions = model.predict(processed_img)
        predicted_idx = int(np.argmax(predictions[0]))

        symbols = {i: str(i) for i in range(10)}
        return jsonify({"digit": symbols[predicted_idx]})

    except Exception as e:
        return jsonify({"error": str(e)})
