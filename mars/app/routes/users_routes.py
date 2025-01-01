import json
from math import ceil

from flask import Blueprint, jsonify, request

from app.models.users_models import UserProfile

user_bp = Blueprint("user", __name__)

@user_bp.route("/register", methods=["POST"])
def register_user():
	data = request.get_json()
	try:
		if data :
			user=UserProfile.create_user(data)
			return jsonify(
            {"message": "User registered", "username": user.username}
        ), 201
	except Exception as e:
		return jsonify({"error": str(e)}), 400

@user_bp.route("/",methods=["GET"])
def list_users():
	users = UserProfile.list_users()
	if users:
		return jsonify({"all users":users}),200
	
@user_bp.route("/<userid>",methods = ["GET"])	
def get_user(userid):
	user , _post = UserProfile.get_user(id=userid)
	if user:
		return jsonify({
			"id":user.id,
			"username":user.username,
            "name":user.name,
            "email":user.email,
            "bio":user.bio,
			"isVerified":user.isVerified,
			"created_at":user.created_at,
			"updated_at":user.updated_at,
			"posts":_post
		})
	return jsonify({"error": "User not found"}), 404	

@user_bp.route("/<username>",methods = ["DELETE"])
def delete_user(username):
	user=UserProfile.delete_user(username=username)
	if user:
		return jsonify({"User deleted sucessfully":user.username})
	return jsonify({"failed"})
	
@user_bp.route("/<userid>",methods = ["PUT"])	
def update_user(userid):
    updates = request.get_json()
    user = UserProfile.update_user(id=userid, updates=updates)
    if user:
        return jsonify({"message": "User updated", "username": user.username})
    return jsonify({"error": "User not found"}), 404



# list verified users amoing you friends list