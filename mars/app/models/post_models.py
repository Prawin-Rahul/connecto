from datetime import datetime
from pytz import timezone
from typing import Optional, Dict, Any
from app import db
from flask import Blueprint, jsonify, request
from math import ceil

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

    # Use Decorater to Handle Authorization and prevent repetitive checks.
    @staticmethod
    def create_post(data: Dict[str, Any], user_id: int) -> 'UserPost':
        """
        Create a user post.

        Args:
            data (dict): Key-value pairs of fields to update.
            user_id (int): The ID of the owner of the post.

        Returns:
            UserPost: The newly created post.
        """
        new_post = UserPost(
            title=data["title"],
            content=data["content"],
            user_id=user_id,
        )
        db.session.add(new_post)
        db.session.commit()
        return new_post
    
    @staticmethod
    def delete_post(post_id: int, user_id: int) -> bool:
        """
        Delete a user post.

        Args:
            post_id (int): The ID of the post to delete.
            user_id (int): The ID of the owner of the post.

        Returns:
            bool: True if the post was successfully deleted, False otherwise.
        """
        try:
            user_post = UserPost.query.filter_by(post_id=post_id).first()
            if user_post:
                if user_post.user_id == int(user_id):
                    db.session.delete(user_post)
                    db.session.commit()
                    return True
            return False
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def edit_post(data: Dict[str, Any], post_id: int, user_id: int) -> Optional['UserPost']:
        """
        Update a user post.

        Args:
            data (dict): Key-value pairs of fields to update.
            post_id (int): The ID of the post to update.
            user_id (int): The ID of the owner of the post.

        Returns:
            Optional[UserPost]: The updated post if successful, otherwise None.
        """
        try:
            post = UserPost.query.filter_by(post_id=post_id).first()
            if post and post.user_id == int(user_id):
                for key, value in data.items():
                    setattr(post, key, value)
                db.session.commit()
                return True
            return False
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_post(post_id: int) -> Optional['UserPost']:
        # If impressions need to auto-increment on views, 
        # consider adding logic in the get_post method.
        # post.impression += 1 , Before commiting
        try:
            post = UserPost.query.filter_by(post_id=post_id).first()
            if post:
                return jsonify(
                    {
                        "post_id": post.post_id,
                        "title": post.title,
                        "content": post.content,
                        "user_id": post.user_id,
                        "created_at": post.created_at,
                        "image": post.image,
                        "impressions": post.impression,
                        "updated_at": post.updated_at,
                        "user": {
                            "username": post.user.username, # N+1 Query Problem , Do Eager loading
                            "image": post.user.image,
                            "isVerified": post.user.isVerified,
                        },
                    }
                )
            return jsonify({"error": "Post not found"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500
   
    @staticmethod
    def list_posts():
        # Invalid (e.g., negative or zero) page or per_page, needs to be handled gracefully.
        page = max(1, request.args.get("page", 1, type=int))
        per_page = max(1, request.args.get("per_page", 5, type=int))

        query = UserPost.query
        total_posts = query.count()
        posts = (
            query.offset((page - 1) * per_page).limit(per_page).all()
        ) 
        if not posts:
            return jsonify({"data": [], "message": "No posts found"}), 200
            # Give pagination details are always returned, even when the data array is empty.
        paginated_response = {
                    "data": [
                        {
                            "post_id":post.post_id,
                            "title": post.title,
                            "content": post.content,
                            "user_id":post.user_id,
                            "created_at":post.created_at,
                            "image":post.image,
                            "impressions":post.impression,
                            "updated_at":post.updated_at,
                        }
                        for post in posts
                    ],
                    "pagination": {
                        "current_page": page,
                        "per_page": per_page,
                        "total_pages": ceil(total_posts / per_page),
                        "total_users": total_posts,
                    },
                }
        print(paginated_response)
        return jsonify(paginated_response), 200

# Need to Add data Validation , to Aviod premature call to DB