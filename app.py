from flask import Flask
from flask_cors import CORS
from routes.user_api import user_api
from routes.host_api import host_api
from routes.auth_api import auth_api


def create_app():
    app = Flask(__name__)
    CORS(app, supports_credentials=True)

    # Register supported blueprints
    app.register_blueprint(auth_api, url_prefix="/api")
    app.register_blueprint(user_api, url_prefix="/api")
    app.register_blueprint(host_api, url_prefix="/api")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=3005)
