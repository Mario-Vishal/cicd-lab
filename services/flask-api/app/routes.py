from flask import Blueprint, request, jsonify
from datetime import datetime
import random

bp = Blueprint("api", __name__)

@bp.get("/health")
def health():
    return jsonify(status="ok"), 200

@bp.get("/greet")
def greet():
    name = request.args.get("name", "World")
    return jsonify(message=f"Hello, {name}!"), 200

@bp.post("/echo")
def echo():
    if not request.is_json:
        return jsonify(error="Expected JSON body"), 400
    data = request.get_json()
    data["_echo_timestamp"] = datetime.utcnow().isoformat() + "Z"
    return jsonify(data), 200

@bp.get("/fail")
def fail():
    # Simulate unpredictable failure
    if random.random() < 0.5:
        raise RuntimeError("Simulated random failure")
    return jsonify(status="sometimes passes"), 200

# Global error handler example (will catch RuntimeError from /fail)
@bp.app_errorhandler(Exception)
def handle_exception(e):
    return jsonify(error=str(e), type=e.__class__.__name__), 500
