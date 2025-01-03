import json
from math import ceil

from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required , get_jwt_identity

from app.models.users_models import UserProfile

user_bp = Blueprint("user", __name__)

@user_bp.route("/<int:userid>", methods=["GET", "PUT", "DELETE"])
def user_operations(userid):
    if request.method == "PUT":
        return update_user(userid)
    elif request.method == "DELETE":
        return delete_user(userid)
    elif request.method == "GET":
        return get_user(userid)
    

@user_bp.route("/login", methods=["POST"])
def login():
	data = request.get_json()
	if not data or "username" not in data or "password" not in data:
		return jsonify({"error": "Username and password are required"}), 400

	user = UserProfile.query.filter_by(username=data["username"]).first()
	if not user or not user.check_password(data["password"]):
		return jsonify({"error": "Invalid username or password"}), 401

	access_token = create_access_token(identity=str(user.id))
    # Generate refresh token
    # refresh_token = create_refresh_token(identity={"username": user.username})
	return jsonify({"access_token": access_token}), 200
 
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
@jwt_required()
def list_users():
	page = request.args.get("page", 1, type=int)
	per_page = request.args.get("per_page", 5, type=int)

# ofset is not a property of lisst , But the model itself
	query = UserProfile.query
	total_users = query.count()
	users = (
		query.offset((page - 1) * per_page).limit(per_page).all()
	) 
	paginated_response = {
			"data": [
				{
					"username": user.username,
					"email": user.email,
					"created_at": user.created_at,
				}
				for user in users
			],
			"pagination": {
				"current_page": page,
				"per_page": per_page,
				"total_pages": ceil(total_users / per_page),
				"total_users": total_users,
			},
		}
	return jsonify(paginated_response), 200
	
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

# Add user_id in jwt as int itself
@user_bp.route("/<userid>",methods = ["DELETE"])
@jwt_required()
def delete_user(userid):
	current_user_id = get_jwt_identity() 
	if userid != int(current_user_id):
		return jsonify({"error": "Unauthorized to delete this user"}), 403
	user=UserProfile.delete_user(id=userid)
	if user:
		return jsonify({"User deleted sucessfully":user.username})
	return jsonify({"error":"NO user found"}),404
	
@user_bp.route("/<userid>",methods = ["PUT"])
@jwt_required	()
def update_user(userid):
	current_user_id = get_jwt_identity() 
	print(type(userid))
	print(type(current_user_id))
	if userid != int(current_user_id):
		return jsonify({"error": "Unauthorized to update this user"}), 403
	updates = request.get_json()
	user = UserProfile.update_user(id=userid, updates=updates)
	if user:
		return jsonify({"message": "User updated", "username": user.username})
	return jsonify({"error": "User not found"}), 404



# list verified users amoing you friends list