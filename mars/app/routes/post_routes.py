from flask import Blueprint, jsonify, request

from app.models.post_models import UserPost

post_bp = Blueprint("posts", __name__)


# Resource Identification via URL  - is a good practice
@post_bp.route("/<int:post_id>", methods=["GET", "PUT", "DELETE"])
def user_operations(post_id):
    if request.method == "PUT":
        return edit_post(post_id)
    elif request.method == "DELETE":
        return delete_post(post_id)
    elif request.method == "GET":
        return get_post(post_id)


@post_bp.route("/", methods=["POST"])
def create_post():
    data = request.get_json()
    try:
        new_post = UserPost.create_post(data)
        print(new_post.post_id)
        return jsonify({"message": "Post created", "username": new_post.user_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

def delete_post(post_id):
    if UserPost.delete_post(post_id):
        return jsonify({"message": "Post deleted"})
    return jsonify({"error": "Post not found"}), 404

def edit_post(post_id):
    data = request.get_json()
    posts = UserPost.edit_post(data=data,post_id=post_id)
    if posts:
        print(posts.title)
        return jsonify({"message": "Post edited"})
    return jsonify({"error": "Post not found"}), 404


def get_post(post_id):
    data = UserPost.get_post(post_id)
    if data is not False:
        post = data
        print(post)
        return jsonify(
            {
                "post_id":post.post_id,
                "title": post.title,
                "content": post.content,
                "user_id":post.user_id,
                "created_at":post.created_at,
                "image":post.image,
                "impressions":post.impression,
                "updated_at":post.updated_at,
                # from the post perspective , this user details is enough
                "user":{
                    "username":post.user.username,
                    "image":post.user.image,
                    "isVerified":post.user.isVerified
                }
            }
        )
    return jsonify({"error": "Post not found"}), 404

# List posts 

##### search post based on text .