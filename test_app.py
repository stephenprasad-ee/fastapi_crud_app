# test_app.py
import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

# -----------------------
# Health Check Test
# -----------------------
def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["status"] == "Healthy"
    assert "timestamp" in json_data

# -----------------------
# CRUD Tests
# -----------------------
def test_create_item():
    response = client.post("/items/", json={
        "name": "Test Item",
        "description": "A test item",
        "price": 10.5,
        "quantity": 5
    })
    assert response.status_code == 200
    data = response.json()
    assert data["id"] > 0
    assert data["name"] == "Test Item"

def test_list_items():
    # Ensure at least one item exists
    client.post("/items/", json={
        "name": "Item 2",
        "description": "Another item",
        "price": 20.0,
        "quantity": 2
    })
    response = client.get("/items/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1

def test_get_item():
    # Create an item
    create_resp = client.post("/items/", json={
        "name": "Get Test",
        "description": "Get test item",
        "price": 15.0,
        "quantity": 3
    })
    item_id = create_resp.json()["id"]

    # Retrieve the item
    response = client.get(f"/items/{item_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == item_id
    assert data["name"] == "Get Test"

def test_update_item():
    # Create an item
    create_resp = client.post("/items/", json={
        "name": "Update Test",
        "description": "Before update",
        "price": 12.0,
        "quantity": 1
    })
    item_id = create_resp.json()["id"]

    # Update the item
    response = client.put(f"/items/{item_id}", json={
        "name": "Updated Item",
        "description": "After update",
        "price": 14.0,
        "quantity": 2
    })
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Item"
    assert data["description"] == "After update"

def test_delete_item():
    # Create an item
    create_resp = client.post("/items/", json={
        "name": "Delete Test",
        "description": "To be deleted",
        "price": 5.0,
        "quantity": 1
    })
    item_id = create_resp.json()["id"]

    # Delete the item
    response = client.delete(f"/items/{item_id}")
    assert response.status_code == 200
    data = response.json()
    assert "deleted successfully" in data["message"]

    # Ensure item no longer exists
    response = client.get(f"/items/{item_id}")
    assert response.status_code == 404

# Use the following command to execute tests:
# pytest test_app.py --disable-warnings -v