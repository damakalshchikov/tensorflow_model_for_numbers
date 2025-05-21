from flask import Flask
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024

    from .routes import main

    app.register_blueprint(main)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
