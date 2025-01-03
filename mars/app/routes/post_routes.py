from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required , get_jwt_identity ,verify_jwt_in_request
import json
from math import ceil

from app.models.post_models import UserPost

post_bp = Blueprint("posts", __name__)
@post_bp.before_request
def require_jwt():
    try:
        verify_jwt_in_request()
    except:
        return jsonify({"error":"Token Expired"})

@post_bp.route("/<int:post_id>", methods=["GET", "PUT", "DELETE"])
def user_operations(post_id):
    if request.method == "PUT":
        return edit_post(post_id)
    elif request.method == "DELETE":
        return delete_post(post_id)
    elif request.method == "GET":
        return get_post(post_id)
    
@post_bp.route("/", methods=["GET", "POST"])  
def user_operation():
    if request.method == "POST":
        return create_post()
    elif request.method == "GET":
        return list_posts()  


def create_post():
    data = request.get_json()
    try:
        user_id = get_jwt_identity()
        new_post = UserPost.create_post(data,user_id)
        return jsonify({"message": "Post created", "userid": new_post.user_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

def delete_post(post_id):
    user_id = get_jwt_identity()
    response =  UserPost.delete_post(post_id=post_id,user_id=user_id)
    if response:
        return jsonify({"message": "Post deleted"})
    return jsonify({"error": "Post not found"}), 404

def edit_post(post_id):
    data = request.get_json()
    user_id = get_jwt_identity()
    posts = UserPost.edit_post(data=data,post_id=post_id,user_id=user_id)
    if posts:
        return jsonify({"message": "Post edited"})
    return jsonify({"error": "Post not found"}), 404

def get_post(post_id):
    post = UserPost.get_post(post_id)
    return post

def list_posts():
    response =  UserPost.list_posts()
    return response

# how to error handle if not post (Bxoz We aget metadat == true)


##### search post based on text .




