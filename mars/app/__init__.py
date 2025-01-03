from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)  
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
    app.config["JWT_SECRET_KEY"] = (
        "prawin1411"
    )  # store it in .env
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app,db)

    from app.routes.users_routes import user_bp
    from app.routes.post_routes import post_bp
    app.register_blueprint(user_bp, url_prefix="/api/users")
    app.register_blueprint(post_bp,url_prefix="/api/posts")

    return app 