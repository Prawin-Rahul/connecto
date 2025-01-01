from datetime import datetime

from pytz import timezone
from app import db

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
    # relationship
    posts = db.relationship(
        "UserPost", back_populates="user", cascade="all, delete-orphan"
    ) 
    
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
        users = UserProfile.query.filter_by(id=id).first()
        _post = []
        if users:
            for post in users.posts:
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
    def delete_user(username):
        try:
            user = UserProfile.query.filter_by(username=username).first()
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
            print(updates)
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



## how to keep created time static 
# only change Updated_time