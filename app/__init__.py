from flask import Flask
from flask_sqlalchemy import SQLAlchemy
 

# Create database object
db = SQLAlchemy()

def create_app():

    app = Flask(__name__)

    app.config["SECRET_KEY"] = "trek123"

    # SQLite Database
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///trek.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize database
    db.init_app(app)
     

    # Import Blueprints
    from app.routes.home import home_bp
    from app.routes.auth import auth_bp
    from app.routes.admin import admin_bp
    from app.routes.staff import staff_bp
    from app.routes.trek import trek_bp

    # Register Blueprints
    app.register_blueprint(home_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(staff_bp)
    app.register_blueprint(trek_bp)

    return app