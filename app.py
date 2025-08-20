from flask import Flask
from flask_cors import CORS
from routes.user_api import user_api
from routes.guest_api import guest_api
from routes.host_api import host_api
from routes.availability_api import availability_api
from routes.hosting_request_api import hosting_request_api
from routes.message_api import message_api
from routes.thank_you_note_api import thank_you_note_api
from routes.report_api import report_api
from routes.auth_api import auth_api


def create_app():
    app = Flask(__name__)
    CORS(app, supports_credentials=True)

    # Register blueprints
    app.register_blueprint(auth_api, url_prefix="/api")
    app.register_blueprint(user_api, url_prefix="/api")
    app.register_blueprint(guest_api, url_prefix="/api")
    app.register_blueprint(host_api, url_prefix="/api")
    app.register_blueprint(availability_api, url_prefix="/api")
    app.register_blueprint(hosting_request_api, url_prefix="/api")
    app.register_blueprint(message_api, url_prefix="/api")
    app.register_blueprint(thank_you_note_api, url_prefix="/api")
    app.register_blueprint(report_api, url_prefix="/api")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=3002)
