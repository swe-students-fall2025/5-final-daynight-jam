from flask import Blueprint, render_template, request, session, redirect, url_for
from .db import insert_recipe

main_bp = Blueprint("main", __name__)

def login_required(f):
    """Simple session-based login check"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated_function

@main_bp.route("/")
@login_required
def index():
    """Home page"""
    return render_template("home.html")

@main_bp.route("/home")
@login_required
def home():
    """Home page with project overview"""
    return render_template("home.html")

@main_bp.route("/ingredients")
@login_required
def ingredients():
    """Page to manage user's available ingredients"""
    return render_template("ingredients.html")

@main_bp.route("/recipe")
@login_required
def recipe():
    """Recipe listing and detail page"""
    return render_template("recipe.html")

@main_bp.route("/result")
@login_required
def result_page():
    """Result page - expects query string with recipe_id"""
    recipe_id = request.args.get("recipe_id")
    recipe = None
    if recipe_id:
        from .db import find_recipe_by_id
        recipe = find_recipe_by_id(recipe_id)
    return render_template("result.html", recipe=recipe)