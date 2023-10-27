def test_create_ratio(client):
    data = {}
    response = client.post("/insert_db",json=data)
    assert response.status_code == 200
    # assert response.json()