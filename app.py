from flask import Flask, render_template, request, jsonify
import tensorflow as tf
import numpy as np
from PIL import Image
import base64
from io import BytesIO
import os

app = Flask(__name__)

# Проверка наличия модели
MODEL_PATH = "char_classifier_tensorflow.keras"
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Модель {MODEL_PATH} не найдена!")

# Загрузка модели
model = tf.keras.models.load_model(MODEL_PATH)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Получение данных с canvas
        data = request.get_json()
        img_data = data["image"].split(",")[1]  # Удаление заголовка base64
        img_bytes = base64.b64decode(img_data)

        # Преобразование в изображение
        img = Image.open(BytesIO(img_bytes)).convert("L")  # Градации серого
        img = img.resize((28, 28))  # Размер 28x28

        # Преобразование в массив и нормализация
        img_array = tf.keras.preprocessing.image.img_to_array(img)
        img_array = img_array / 255.0  # Нормализация
        img_array = np.expand_dims(img_array, axis=0)  # Добавление batch-размерности

        # Предсказание
        predictions = model.predict(img_array)
        predicted_idx = int(np.argmax(predictions[0]))

        # Сопоставление индекса с символом
        symbols = {i: str(i) for i in range(10)}

        return jsonify({"digit": symbols[predicted_idx]})

    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == "__main__":
    app.run(debug=True)
