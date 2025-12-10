import sys
import os
import importlib
import pytest
from unittest.mock import patch

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import mongodb_subsystem as mongo_pkg 

if hasattr(mongo_pkg, "init_mongo"):
    mongo_pkg.init_mongo = lambda *a, **k: None


import mongodb_subsystem.db as db_mod
db_mod.USE_MONGO = False  

if not hasattr(db_mod, "_memory"):
    # fallback safety: create structure expected by tests
    db_mod._memory = {"users": {}, "recipes": {}}
    db_mod._memory["users"] = {}
    db_mod._memory["recipes"] = {}

from web.app import create_app


@pytest.fixture()
def app():
    """Create a fresh Flask app for each test."""
    # Ensure in-memory DB is clear before constructing app
    db_mod._memory["users"].clear()
    db_mod._memory["recipes"].clear()
    db_mod.USE_MONGO = False

    app = create_app()
    app.config.update({
        "TESTING": True,
        "SECRET_KEY": "test-secret-key",
    })
    yield app


@pytest.fixture()
def client(app):
    """Flask test client."""
    with app.test_client() as client:
        yield client


@pytest.fixture(autouse=True)
def reset_in_memory_db():
    """Automatically clear in-memory DB before each test."""
    db_mod._memory["users"].clear()
    db_mod._memory["recipes"].clear()
    db_mod.USE_MONGO = False
    yield
    # also clear after
    db_mod._memory["users"].clear()
    db_mod._memory["recipes"].clear()


@pytest.fixture()
def mock_ml_client():
    # patch the factory that returns the ML client used by web.ml_subsystem
    target = "web.ml_subsystem._get_default_client"
    with patch(target) as mock_get_client:
        mock_client = mock_get_client.return_value
        # make sure methods used by tests exist
        mock_client.get_recommendation.return_value = {
            "recipe_id": "1",
            "name": "Mock Recipe",
            "ingredients": ["ingredient1", "ingredient2"],
            "tools": ["pan", "oven"],
            "steps": ["step1", "step2"],
            "substitutions": ["sub1"]
        }
        mock_client.replace_ingredient.return_value = {
            "recipe_id": "1",
            "name": "Mock Recipe Updated",
            "ingredients": ["ingredient1", "ingredient2", "ingredient3"],
            "tools": ["pan", "oven"],
            "steps": ["step1", "step2", "step3"],
            "substitutions": ["sub1", "sub2"]
        }
        yield mock_get_client
