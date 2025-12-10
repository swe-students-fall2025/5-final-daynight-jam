def test_api_recommend(client, mock_ml_client):
    response = client.post("/api/recommend", json={})
    data = response.get_json()
    assert response.status_code == 200
    assert "recipe" in data
    assert data["recipe"]["name"] == "Mock Recipe"
