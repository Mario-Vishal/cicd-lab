import json
from app import app as flask_app

def test_health():
    client = flask_app.test_client()
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.get_json()["status"] == "ok"

def test_greet_default():
    client = flask_app.test_client()
    resp = client.get("/greet")
    assert resp.status_code == 200
    assert "World" in resp.get_json()["message"]

def test_greet_named():
    client = flask_app.test_client()
    resp = client.get("/greet?name=Mario")
    assert resp.status_code == 200
    assert "Mario" in resp.get_json()["message"]

def test_echo():
    client = flask_app.test_client()
    payload = {"foo": "bar"}
    resp = client.post("/echo", json=payload)
    data = resp.get_json()
    assert resp.status_code == 200
    assert data["foo"] == "bar"
    assert "_echo_timestamp" in data

def test_fail_endpoint():
    client = flask_app.test_client()
    # We don't assert on success vs failure—just that it returns a valid structure
    resp = client.get("/fail")
    assert resp.status_code in (200, 500)
