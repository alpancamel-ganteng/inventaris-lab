import pytest
from app import create_app


@pytest.fixture()
def app(tmp_path):
    database = tmp_path / "test.db"
    return create_app({
        "TESTING": True,
        "SECRET_KEY": "test-secret-key-not-for-production",
        "DATABASE": str(database),
        "SEED_DEMO_USERS": True,
        "SESSION_COOKIE_SECURE": False,
    })


@pytest.fixture()
def client(app):
    return app.test_client()


def login(client, username, password):
    return client.post("/api/login", json={"username": username, "password": password})


def test_health_is_public(client):
    assert client.get("/health").status_code == 200


def test_items_require_login(client):
    assert client.get("/api/items").status_code == 401


def test_admin_can_manage_items_and_users(client):
    assert login(client, "admin", "Admin-Demo-2026!").status_code == 200
    assert client.get("/api/items").status_code == 200
    created = client.post("/api/items", json={
        "name": "Monitor", "quantity": 4, "location": "Lab A"
    })
    assert created.status_code == 201
    item_id = created.get_json()["id"]
    assert client.patch(f"/api/items/{item_id}", json={"quantity": 5}).status_code == 200
    assert client.delete(f"/api/items/{item_id}").status_code == 200
    assert client.get("/api/users").status_code == 200


def test_staff_can_create_and_update_but_not_delete_or_manage_users(client):
    assert login(client, "staff", "Staff-Demo-2026!").status_code == 200
    created = client.post("/api/items", json={
        "name": "Keyboard", "quantity": 8, "location": "Lab B"
    })
    assert created.status_code == 201
    item_id = created.get_json()["id"]
    assert client.patch(f"/api/items/{item_id}", json={"quantity": 9}).status_code == 200
    assert client.delete(f"/api/items/{item_id}").status_code == 403
    assert client.get("/api/users").status_code == 403


def test_viewer_is_read_only(client):
    assert login(client, "viewer", "Viewer-Demo-2026!").status_code == 200
    assert client.get("/api/items").status_code == 200
    assert client.post("/api/items", json={
        "name": "Mouse", "quantity": 2, "location": "Lab C"
    }).status_code == 403
    assert client.patch("/api/items/1", json={"quantity": 3}).status_code == 403
    assert client.delete("/api/items/1").status_code == 403
    assert client.get("/api/users").status_code == 403


def test_wrong_password_is_rejected(client):
    response = login(client, "admin", "wrong-password")
    assert response.status_code == 401


def test_user_creation_requires_strong_password(client):
    login(client, "admin", "Admin-Demo-2026!")
    weak = client.post("/api/users", json={
        "username": "newuser", "password": "short", "role": "viewer"
    })
    assert weak.status_code == 400
    good = client.post("/api/users", json={
        "username": "newuser", "password": "A-Long-Demo-Pass-2026!", "role": "viewer"
    })
    assert good.status_code == 201
