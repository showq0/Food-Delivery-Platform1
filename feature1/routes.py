from flask import Blueprint, render_template, request, session, jsonify, make_response
from .models import User
from app.extensions import db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity,create_refresh_token, set_access_cookies


# Create a blueprint instance
user_bp = Blueprint('user', __name__, template_folder='templates')



@user_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    data = request.form
    if User.query.filter_by(username=data["username"]).first():
        return jsonify({"msg": "User already exists"}), 400

    new_user = User(
        username=data["username"],
        role=data.get("role", "customer"),
        phone_number=data.get("phone_number"),
        address=data.get("address"),
        payment_info=data.get("payment_info"),
    )
    new_user.set_password(data["password"])

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg": "User registered successfully"}), 201


@user_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    data = request.form
    user = User.query.filter_by(username=data["username"]).first()

    if not user or not user.check_password(data["password"]):
        return jsonify({"msg": "Invalid username or password"}), 401

    access_token = create_access_token(identity=str(user.id))
    refresh_token = create_refresh_token(identity=user.id)
    resp = make_response(jsonify({"login": True}))
    set_access_cookies(resp, access_token)
    return resp


@user_bp.route("/profile", methods=["GET", "POST"])
@jwt_required()
def profile():
    current_user_id = int(get_jwt_identity())
    user = User.query.get(current_user_id)

    if request.method == "POST":
        user.phone_number = request.form.get("phone_number", user.phone_number)
        user.address = request.form.get("address", user.address)
        user.payment_info = request.form.get("payment_info", user.payment_info)
        db.session.commit()
        return "Profile updated successfully"

    return render_template("profile.html", user=user)
