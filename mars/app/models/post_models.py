from datetime import datetime

from pytz import timezone

from app import db


class UserPost(db.Model):
    __tablename__ = "user_posts"

    post_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone("Asia/Kolkata"))
    )
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone("Asia/Kolkata")), onupdate=lambda: datetime.now(timezone("Asia/Kolkata")), nullable=False)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.String(250), nullable=False)
    user_id = db.Column(
        db.Integer, db.ForeignKey("user_profile.id"), nullable=False
    )
    image = db.Column(db.String, nullable=True)
    impression = db.Column(db.Integer,default=0)
    # Relationship definition
    user = db.relationship("UserProfile", back_populates="posts")

    @staticmethod
    def create_post(data):
        new_post = UserPost(
            title=data["title"],
            content=data["content"],
            user_id=data["user_id"], #  Anyone can replicate as User (Add Auth)
        )
        db.session.add(new_post)
        db.session.commit()
        return new_post

    @staticmethod
    def delete_post(post_id):
        """
        Delete a user post.
        Args:
            post_id (str): The post_id to delete.
            username (str): The owner of the post  # WE Dont need username, because postid id unique
        """
        try:
            user_post = UserPost.query.filter_by(post_id=post_id).first()
            if user_post:
                # for posts in user_post:
                if user_post.post_id == post_id:
                    db.session.delete(
                        user_post
                    )  # If a post loses its association with a user (becomes an "orphan")
                    db.session.commit()
                    return True
            return False
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    # post must return info of user .
    def get_post(post_id):
        post = UserPost.query.filter_by(post_id=post_id).first()
        if post:
            return post
        return False

    @staticmethod
    def get_all_posts(username):
        # get all post of a user , In pagination of 5
        all_posts = UserPost.query.all()
        _user_posts = []
        for post in all_posts:
            _user_posts.append(
                {
                    "username": post.post_id,
                    "email": post.title,
                    "first_name": post.text_content,
                    "last_name": post.created_at,
                }
            )
        return _user_posts

    @staticmethod
    def edit_post(data,post_id):
        """
        Update a user post.
        Args:
            post_id (str): The post_id to update.
            updates (dict): Key-value pairs of fields to update.
        """
        try:
            # print(data["post_id"])
            post = UserPost.query.filter_by(post_id=post_id).first()
            print(post)
            if not post:
                return None
            # print(data["updates"])
            for key, value in data.items():
                setattr(post, key, value)
            db.session.commit()
            return post
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def find_by_title():
        pass
