# ml_client.py
# This is a placeholder module that simulates ML recommendations.
# Later you can replace calls here to real ML client HTTP requests.

def get_recommendation(payload):
    # payload contains include/exclude/cuisine/taste/diet
    # simple heuristic placeholder:
    includes = payload.get("include", [])
    cuisine = payload.get("cuisine") or "Generic"
    # build a fake recipe
    recipe = {
        "recipe_id": "ph-" + (",".join(includes)[:8] or "001"),
        "name": f"{cuisine} Placeholder Dish",
        "ingredients": [{"name": ing, "amount": "as needed"} for ing in includes] or [{"name":"egg","amount":"2"}],
        "tools": ["pot", "pan"],
        "steps": ["Prep ingredients", "Cook until done"],
        "substitutions": { }  # example: {"milk": ["oat milk", "soy milk"]}
    }
    return {
        "best_recipes": [recipe],
        "other_suggestions": []
    }

def replace_ingredient(recipe, from_name, to_name):
    # shallow replacement in recipe dict, return new recipe dict
    new = dict(recipe)
    new_ings = []
    for ing in new.get("ingredients", []):
        if ing.get("name") == from_name:
            new_ings.append({"name": to_name, "amount": ing.get("amount","as needed")})
        else:
            new_ings.append(ing)
    new["ingredients"] = new_ings
    return new
