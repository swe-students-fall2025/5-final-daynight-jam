from flask import Flask
from .db import init_db_client

def create_app():
    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.config["SECRET_KEY"] = "dev-secret-key"  # TODO: switch to .env

    # init DB client (attempt Mongo, otherwise in-memory fallback)
    init_db_client(app)

    # register blueprints
    from .auth import auth_bp
    from .api import api_bp
    from .main import main_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(main_bp)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8000, debug=True)
