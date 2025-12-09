# app/pages.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from .ml_client import get_recommendation

pages_bp = Blueprint("pages", __name__)

@pages_bp.route("/")
@login_required
def home():
    """Main landing page after login."""
    return render_template("home.html")


@pages_bp.route("/ingredients")
@login_required
def ingredients():
    """Ingredients input / management page."""
    return render_template("ingredients.html")


def _parse_csv(raw: str) -> list[str]:
    """
    Helper: turn 'eggs, chicken' into ['eggs', 'chicken'].
    Lowercases and trims whitespace.
    """
    if not raw:
        return []
    return [item.strip().lower() for item in raw.split(",") if item.strip()]


@pages_bp.route("/recipe", methods=["GET", "POST"])
@login_required
def recipe():
    """
    Recipe results page.

    - POST: user came from the ingredients page → call ML client
      with their ingredients and render a recipe.

    - GET: user opened /recipe directly → show "no recipe yet" state.
    """
    # POST: handle form submission from ingredients.html
    if request.method == "POST":
        raw_ingredients = request.form.get("ingredients", "")
        include = _parse_csv(raw_ingredients)

        if not include:
            flash("Please enter at least one ingredient.", "error")
            return redirect(url_for("pages.ingredients"))

        # Build payload for the ML client; you can extend this later with
        # cuisine, allergies, taste, etc.
        payload = {
            "include": include,
        }

        # Call your ML client (works in test.py, we reuse the same function)
        result = get_recommendation(payload) or {}

        # Support two possible shapes of result:
        # 1) A dict with "best_recipes" and "other_suggestions"
        # 2) A single recipe dict
        recipe_obj = None
        other_suggestions = []

        if isinstance(result, dict) and "best_recipes" in result:
            best_recipes = result.get("best_recipes") or []
            recipe_obj = best_recipes[0] if best_recipes else None
            other_suggestions = result.get("other_suggestions") or []
        else:
            # Assume it's already a single recipe dict
            recipe_obj = result or None

        return render_template(
            "recipe.html",
            include=include,
            recipe=recipe_obj,
            other_suggestions=other_suggestions,
        )

    # GET: no POST data → no recipe yet
    return render_template(
        "recipe.html",
        include=[],
        recipe=None,
        other_suggestions=[],
    )
