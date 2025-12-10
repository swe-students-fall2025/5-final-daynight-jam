def test_recipe_recommend_success(client, monkeypatch):
    def mock_post(url, json, timeout):
        class MockResp:
            def json(self):
                return {"recipe": "Mock Recipe"}
        return MockResp()

    monkeypatch.setattr("web.app.recipes.requests.post", mock_post)

    response = client.get("/recipes/recommend?ingredients=tomato&cookware=pan&allergies=&flavor=sweet")
    assert response.status_code == 200

    data = response.get_json()
    assert "input" in data
    assert "recommendation" in data
    assert data["recommendation"]["recipe"] == "Mock Recipe"


def test_recipe_recommend_failure(client, monkeypatch):
    def mock_post_fail(url, json, timeout):
        raise Exception("ML DOWN")

    monkeypatch.setattr("web.app.recipes.requests.post", mock_post_fail)

    response = client.get("/recipes/recommend")
    assert response.status_code == 503
    assert "error" in response.get_json()
