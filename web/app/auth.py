from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from .db import create_user, find_user

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        data = request.form
        username = data.get("username")
        password = data.get("password")
        if not username or not password:
            return render_template("register.html", error="Require username and password")
        pw_hash = generate_password_hash(password)
        ok = create_user(username, pw_hash)
        if not ok:
            return render_template("register.html", error="User exists")
        # auto-login
        session["user"] = username
        return redirect(url_for("main.index"))
    return render_template("register.html")  

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data = request.form
        username = data.get("username")
        password = data.get("password")
        if not username or not password:
            return render_template("login.html", error="Require username and passwor")
        user = find_user(username)
        if not user:
            return render_template("login.html", error="User does not exist")
        pw_hash = user.get("password")
        if not check_password_hash(pw_hash, password):
            return render_template("login.html", error="Wrong password")
        session["user"] = username
        return redirect(url_for("main.index"))
    return render_template("login.html")

@auth_bp.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("auth.login"))

# small API for tests
@auth_bp.route("/api/me")
def me():
    user = session.get("user")
    return jsonify({"user": user})
