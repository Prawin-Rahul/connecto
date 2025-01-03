# Learning Documentation

---

## Project Overview

This project is built using Flask and SQLAlchemy, leveraging REST architecture, JWT for authentication, and Bcrypt for password hashing.

---

## Key Learnings & Concepts

### 1. Application Factory Method

Flask's application factory pattern allows creating an app instance that is independent of the configuration. This enhances flexibility and reusability.

```python
from app import create_app , db

app = create_app()

if __name__ == "__main__":

    with app.app_context():
        db.create_all()
        app.run(debug=True)
```

### 2. Flask Configuration

Configurations help manage app settings like secret keys, database URIs, etc at one place

```python
def create_app():
    app = Flask(__name__)
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
    app.config["JWT_SECRET_KEY"] = (
        "*****"
    )
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app,db)

    from app.routes.users_routes import user_bp
    app.register_blueprint(user_bp, url_prefix="/api/users")

    return app
```

### 3. Blueprints

Blueprints organize routes and views, enhancing modularity.

```python
user_bp = Blueprint('user', **name**)
@user_bp.route('/register', methods=['POST'])
def register_user():
	pass
```

### 4. Password Hashing

Bcrypt is used for secure password storage.

```python
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

# Hashing password

def set_password(self, raw_password):
        self.password = bcrypt.generate_password_hash(raw_password).decode("utf-8")

def check_password(self, raw_password):
        return bcrypt.check_password_hash(self.password, raw_password)
```

### 5. Database Relationships

SQLAlchemy ORM facilitates relationships, making models cleaner.

```python
class UserProfile(db.Model):
id = db.Column(db.Integer, primary_key=True)
username = db.Column(db.String(50), unique=True, nullable=False)
posts = db.relationship('Post', back_populates='user', cascade="all, delete-orphan")
```

### 6. Database Integration (SQLAlchemy ORM)

Example of creating a user model with CRUD operations.

```python
class UserProfile(db.Model): # Fields, relationships, and methods go here...
```

### 7. REST Architecture

Endpoints are designed following REST principles.

```python

@user_bp.route('/users/', methods=['GET'])
def list_users():
pass # Logic to list users
```

### 8. JWT Authentication

JWT is used for authentication, storing user identity.

```python
@user_bp.route("/<userid>",methods = ["DELETE"])
@jwt_required()
def delete_user(userid):
	pass # Logic to handle login
```

### 9. Authorization

Authorization is enforced using @jwt_required().

```python
@user_bp.route('/user/<user_id>', methods=['PUT'])
@jwt_required()
def delete_post(post_id):
    user_id = get_jwt_identity()
	pass # Logic to update user details
```

### There are more to resolve in this

- m:m relationship
- N+1 problem
- General token to exteant acess token life
- data validation
- etc ..

---
