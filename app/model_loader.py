import tensorflow as tf
import os

MODEL_PATH = "models/char_classifier_tensorflow.keras"

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Модель {MODEL_PATH} не найдена!")

model = tf.keras.models.load_model(MODEL_PATH)
