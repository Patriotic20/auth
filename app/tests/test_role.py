import uuid

def test_create_role(client):
    unique_id = str(uuid.uuid4())[:8]
    role_name = f"role_{unique_id}"
    
    
    role_payload = {"name": role_name}
    reeponse = client.post("/role/", json=role_payload)
    
    assert reeponse.status_code == 201


