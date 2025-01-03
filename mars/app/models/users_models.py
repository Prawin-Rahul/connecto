from datetime import datetime

from pytz import timezone
from app import db , bcrypt
from flask import request

class UserProfile(db.Model):
    
    __tablename__ = 'user_profile'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(50),unique = True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone("Asia/Kolkata")), onupdate=lambda: datetime.now(timezone("Asia/Kolkata")), nullable=False)
    created_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone("Asia/Kolkata"))
    )
    bio = db.Column(db.String,unique=True)
    isVerified = db.Column(db.Boolean,default=False)
    image = db.Column(db.String, nullable=True)
    password = db.Column(db.String(100))
    # relationship
    posts = db.relationship(
        "UserPost", back_populates="user", cascade="all, delete-orphan"
    ) 
    
    def set_password(self, raw_password):
        self.password = bcrypt.generate_password_hash(raw_password).decode("utf-8")

    def check_password(self, raw_password):
        return bcrypt.check_password_hash(self.password, raw_password)

    # CRUD Ops
    @staticmethod
    def create_user(data):
        if not all(
            key in data
            for key in ["username", "email", "bio","name"]
        ):
            raise ValueError("Missing required fields")
        if UserProfile.query.filter_by(username=data["username"]).first():
            raise ValueError("Username already exists")
        if UserProfile.query.filter_by(email=data["email"]).first():
            raise ValueError("Email already exists")

        user = UserProfile(
            username = data["username"],
            email = data["email"],
            name = data["name"],
            bio = data["bio"]
        )
        # hash the password
        user.set_password(data["password"])
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def list_users():
        _users= []
        users = UserProfile.query.all()
        for user in users:
            _users.append({
            "username":user.username,
            "name":user.name,
            "email":user.email,
            "bio":user.bio,
            "user_id":user.id,
            "isVerified":user.isVerified
        })
        return _users
    
    @staticmethod
    def get_user(id):
        # send only to latest posts
        # In UI (Show all posts - then reDirect to all posts url)
        users = UserProfile.query.filter_by(id=id).first()
        _post = []
        if not users:
            return None, []
        if users:
            for post in users.posts:
                if len(_post)<3:
                    _post.append({
                        "post_id":post.post_id,
                        "title": post.title,
                        "content": post.content,
                        "user_id":post.user_id,
                        "created_at":post.created_at,
                        "image":post.image
                    })
            
        return users , _post

    @staticmethod
    def delete_user(id):
        try:
            user = UserProfile.query.filter_by(id=id).first()
            print(user)
            if user:
                db.session.delete(
                    user
                ) 
                db.session.commit()
                return user

            return False
        except Exception as e:
            db.session.rollback()
            raise e
        
    @staticmethod
    def update_user(updates,id):
        try:    
            user = UserProfile.query.filter_by(id=id).first()
            if not user:
                return None
            print(updates.items())
            for key, value in updates.items():
                setattr(user, key, value)
            db.session.commit()
            return user
        except Exception as e:
            db.session.rollback()
            raise e


