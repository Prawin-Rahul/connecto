from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)  
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
    db.init_app(app)

    from app.routes.users_routes import user_bp
    from app.routes.post_routes import post_bp
    app.register_blueprint(user_bp, url_prefix="/api/users")
    app.register_blueprint(post_bp,url_prefix="/api/posts")

    return app 