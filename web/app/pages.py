from flask import Blueprint, render_template
from flask_login import login_required

pages_bp = Blueprint("pages", __name__)

@pages_bp.route("/")
@login_required
def home():
    """Home page with project overview"""
    return render_template("home.html")

@pages_bp.route("/ingredients")
@login_required
def ingredients():
    """Page to manage user's available ingredients"""
    return render_template("ingredients.html")

@pages_bp.route("/recipe")
@login_required
def recipe():
    """Recipe listing and detail page"""
    return render_template("recipe.html")