import pytest
from flask import session

def test_home_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "🍳 What can I cook right now?" in response.data.decode("utf-8")
    assert "Smart Ingredient Match" in response.data.decode("utf-8")


def test_ingredients_page(client):
    response = client.get("/ingredients")
    assert response.status_code == 200
    assert "🥬 My Ingredients" in response.data.decode("utf-8")
    assert "Add Ingredient" in response.data.decode("utf-8")
    assert "No ingredients added yet" in response.data.decode("utf-8")


def test_recipe_page_authenticated(client, mock_ml_client):
    response = client.post("/recipe", data={"ingredients": "chicken, eggs"})
    assert response.status_code == 200
    assert "Mock Recipe" in response.data.decode("utf-8")
    assert "ingredient1" in response.data.decode("utf-8")
    assert "ingredient2" in response.data.decode("utf-8")
    assert "sub1" in response.data.decode("utf-8")


def test_recipe_page_no_data(client):
    response = client.get("/recipe")
    assert response.status_code == 200
    assert "No recipe suggestions yet" in response.data.decode("utf-8")
    assert "No ingredients submitted yet" in response.data.decode("utf-8")

def test_shopping_list_empty(client):
    response = client.get("/shopping-list")
    assert response.status_code == 200
    assert b"Shopping List" in response.data


def test_add_to_shopping_list(client):
    payload = {"item": "tomato", "quantity": "2"}
    response = client.post("/shopping-list/add", json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert data["count"] == 1
    with client.session_transaction() as sess:
        assert sess["shopping_list"][0]["name"] == "tomato"


def test_remove_from_shopping_list(client):
    # Pre-populate
    with client.session_transaction() as sess:
        sess["shopping_list"] = [{"name": "tomato", "checked": False, "quantity": ""}]
    response = client.post("/shopping-list/remove", json={"item": "tomato"})
    assert response.status_code == 200
    data = response.get_json()
    assert data["count"] == 0


def test_toggle_shopping_item(client):
    with client.session_transaction() as sess:
        sess["shopping_list"] = [{"name": "tomato", "checked": False, "quantity": ""}]
    response = client.post("/shopping-list/toggle", json={"item": "tomato"})
    assert response.status_code == 200
    with client.session_transaction() as sess:
        assert sess["shopping_list"][0]["checked"] is True


def test_clear_shopping_list(client):
    with client.session_transaction() as sess:
        sess["shopping_list"] = [{"name": "tomato", "checked": True}]
    response = client.post("/shopping-list/clear")
    assert response.status_code == 200
    with client.session_transaction() as sess:
        assert sess["shopping_list"] == []


def test_clear_checked_items(client):
    with client.session_transaction() as sess:
        sess["shopping_list"] = [
            {"name": "tomato", "checked": True},
            {"name": "lettuce", "checked": False}
        ]
    response = client.post("/shopping-list/clear-checked")
    assert response.status_code == 200
    data = response.get_json()
    assert data["count"] == 1
    with client.session_transaction() as sess:
        assert sess["shopping_list"][0]["name"] == "lettuce"


from web.app.pages import _parse_csv

def test_parse_csv_basic():
    result = _parse_csv("eggs, chicken ,  milk")
    assert result == ["eggs", "chicken", "milk"]

def test_parse_csv_empty():
    result = _parse_csv("")
    assert result == []

def test_parse_csv_with_commas_and_spaces():
    result = _parse_csv(" , apple , , banana ,, ")
    assert result == ["apple", "banana"]

