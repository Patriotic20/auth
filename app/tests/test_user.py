import uuid

def test_create_user_flow(client):
    # Создаем уникальный суффикс
    unique_id = str(uuid.uuid4())[:8]
    username = f"user_{unique_id}"
    role_name = f"role_{unique_id}"

    # 1. Создаем роль
    role_payload = {"name": role_name}
    client.post("/role/", json=role_payload)

    # 2. Создаем пользователя
    user_payload = {
        "username": username,
        "password": "password123",
        "roles": [{"name": role_name}]
    }
    
    response = client.post("/user/", json=user_payload)
    
    assert response.status_code == 201
    assert response.json()["username"] == username
    
    
    user_payload = {
        "username": username,
        "password": "password123",
    }
    
    response = client.post("/user/login", json=user_payload)
    
    assert response.status_code == 200
