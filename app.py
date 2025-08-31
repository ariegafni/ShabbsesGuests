from flask import Flask
from flask_cors import CORS
from auth.auth_api import auth_api
from hosts.host_api import host_api
from users.user_api import user_api
from locations.country_api import country_api
from accommodation_requests.accommodation_requests_api import accommodation_requests_api

def create_app():
    app = Flask(__name__)
    CORS(app, supports_credentials=True)

    # Register supported blueprints
    app.register_blueprint(auth_api, url_prefix="/api")
    app.register_blueprint(user_api, url_prefix="/api")
    app.register_blueprint(host_api, url_prefix="/api")
    app.register_blueprint(country_api, url_prefix="/api")
    app.register_blueprint(accommodation_requests_api, url_prefix="/api")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=3005)
