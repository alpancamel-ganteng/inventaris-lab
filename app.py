import os
import sqlite3
from functools import wraps
from pathlib import Path

from flask import Flask, g, jsonify, request, session
from werkzeug.security import check_password_hash, generate_password_hash


ROLES = ("admin", "staff", "viewer")


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.update(
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev-only-change-this-secret"),
        DATABASE=os.environ.get("DATABASE_PATH", "./data/inventory.db"),
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Strict",
        SESSION_COOKIE_SECURE=os.environ.get("COOKIE_SECURE", "0") == "1",
        PERMANENT_SESSION_LIFETIME=1800,
        JSON_SORT_KEYS=True,
        SEED_DEMO_USERS=os.environ.get("SEED_DEMO_USERS", "1") == "1",
    )
    if test_config:
        app.config.update(test_config)

    Path(app.config["DATABASE"]).parent.mkdir(parents=True, exist_ok=True)

    def get_db():
        if "db" not in g:
            g.db = sqlite3.connect(app.config["DATABASE"])
            g.db.row_factory = sqlite3.Row
            g.db.execute("PRAGMA foreign_keys = ON")
        return g.db

    @app.teardown_appcontext
    def close_db(_error=None):
        db = g.pop("db", None)
        if db is not None:
            db.close()

    def init_db():
        db = get_db()
        db.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL CHECK(role IN ('admin','staff','viewer'))
            );
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                quantity INTEGER NOT NULL CHECK(quantity >= 0),
                location TEXT NOT NULL
            );
        """)
        if app.config["SEED_DEMO_USERS"]:
            demo_users = [
                ("admin", "Admin-Demo-2026!", "admin"),
                ("staff", "Staff-Demo-2026!", "staff"),
                ("viewer", "Viewer-Demo-2026!", "viewer"),
            ]
            for username, password, role in demo_users:
                exists = db.execute(
                    "SELECT id FROM users WHERE username = ?", (username,)
                ).fetchone()
                if not exists:
                    db.execute(
                        "INSERT INTO users(username,password_hash,role) VALUES(?,?,?)",
                        (username, generate_password_hash(password, method="scrypt"), role),
                    )
        if db.execute("SELECT COUNT(*) FROM items").fetchone()[0] == 0:
            db.execute(
                "INSERT INTO items(name,quantity,location) VALUES(?,?,?)",
                ("Laptop Lab", 10, "Ruang Komputer"),
            )
        db.commit()

    with app.app_context():
        init_db()

    def current_user():
        user_id = session.get("user_id")
        if not user_id:
            return None
        return get_db().execute(
            "SELECT id, username, role FROM users WHERE id = ?", (user_id,)
        ).fetchone()

    def require_login(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            user = current_user()
            if user is None:
                return jsonify(error="authentication_required"), 401
            g.user = user
            return fn(*args, **kwargs)
        return wrapper

    def require_roles(*allowed_roles):
        def decorator(fn):
            @wraps(fn)
            @require_login
            def wrapper(*args, **kwargs):
                if g.user["role"] not in allowed_roles:
                    return jsonify(error="forbidden"), 403
                return fn(*args, **kwargs)
            return wrapper
        return decorator

    @app.get("/health")
    def health():
        return jsonify(status="ok")

    @app.post("/api/login")
    def login():
        data = request.get_json(silent=True) or {}
        username = data.get("username", "")
        password = data.get("password", "")
        if not isinstance(username, str) or not isinstance(password, str):
            return jsonify(error="invalid_credentials"), 401
        user = get_db().execute(
            "SELECT id, username, password_hash, role FROM users WHERE username = ?",
            (username,),
        ).fetchone()
        if user is None or not check_password_hash(user["password_hash"], password):
            return jsonify(error="invalid_credentials"), 401
        session.clear()
        session["user_id"] = user["id"]
        session.permanent = True
        return jsonify(message="login_success", username=user["username"], role=user["role"])

    @app.post("/api/logout")
    @require_login
    def logout():
        session.clear()
        return jsonify(message="logout_success")

    @app.get("/api/items")
    @require_roles("admin", "staff", "viewer")
    def list_items():
        rows = get_db().execute(
            "SELECT id, name, quantity, location FROM items ORDER BY id"
        ).fetchall()
        return jsonify(items=[dict(row) for row in rows])

    @app.post("/api/items")
    @require_roles("admin", "staff")
    def create_item():
        data = request.get_json(silent=True) or {}
        name = data.get("name")
        quantity = data.get("quantity")
        location = data.get("location")
        if not isinstance(name, str) or not name.strip():
            return jsonify(error="name_required"), 400
        if not isinstance(quantity, int) or quantity < 0:
            return jsonify(error="quantity_must_be_nonnegative_integer"), 400
        if not isinstance(location, str) or not location.strip():
            return jsonify(error="location_required"), 400
        db = get_db()
        cursor = db.execute(
            "INSERT INTO items(name,quantity,location) VALUES(?,?,?)",
            (name.strip(), quantity, location.strip()),
        )
        db.commit()
        return jsonify(id=cursor.lastrowid, message="item_created"), 201

    @app.patch("/api/items/<int:item_id>")
    @require_roles("admin", "staff")
    def update_item(item_id):
        data = request.get_json(silent=True) or {}
        allowed = {"name", "quantity", "location"}
        if not data or set(data) - allowed:
            return jsonify(error="invalid_fields"), 400
        db = get_db()
        item = db.execute("SELECT id FROM items WHERE id = ?", (item_id,)).fetchone()
        if item is None:
            return jsonify(error="not_found"), 404
        current = db.execute(
            "SELECT name,quantity,location FROM items WHERE id = ?", (item_id,)
        ).fetchone()
        values = {
            "name": data.get("name", current["name"]),
            "quantity": data.get("quantity", current["quantity"]),
            "location": data.get("location", current["location"]),
        }
        if not isinstance(values["name"], str) or not values["name"].strip():
            return jsonify(error="invalid_name"), 400
        if not isinstance(values["quantity"], int) or values["quantity"] < 0:
            return jsonify(error="invalid_quantity"), 400
        if not isinstance(values["location"], str) or not values["location"].strip():
            return jsonify(error="invalid_location"), 400
        db.execute(
            "UPDATE items SET name=?,quantity=?,location=? WHERE id=?",
            (values["name"].strip(), values["quantity"], values["location"].strip(), item_id),
        )
        db.commit()
        return jsonify(message="item_updated")

    @app.delete("/api/items/<int:item_id>")
    @require_roles("admin")
    def delete_item(item_id):
        db = get_db()
        cursor = db.execute("DELETE FROM items WHERE id = ?", (item_id,))
        db.commit()
        if cursor.rowcount == 0:
            return jsonify(error="not_found"), 404
        return jsonify(message="item_deleted")

    @app.get("/api/users")
    @require_roles("admin")
    def list_users():
        rows = get_db().execute(
            "SELECT id, username, role FROM users ORDER BY id"
        ).fetchall()
        return jsonify(users=[dict(row) for row in rows])

    @app.post("/api/users")
    @require_roles("admin")
    def create_user():
        data = request.get_json(silent=True) or {}
        username = data.get("username")
        password = data.get("password")
        role = data.get("role")
        if not isinstance(username, str) or len(username.strip()) < 3:
            return jsonify(error="username_minimum_3_characters"), 400
        if not isinstance(password, str) or len(password) < 12:
            return jsonify(error="password_minimum_12_characters"), 400
        if role not in ROLES:
            return jsonify(error="invalid_role"), 400
        try:
            get_db().execute(
                "INSERT INTO users(username,password_hash,role) VALUES(?,?,?)",
                (username.strip(), generate_password_hash(password, method="scrypt"), role),
            )
            get_db().commit()
        except sqlite3.IntegrityError:
            return jsonify(error="username_already_exists"), 409
        return jsonify(message="user_created"), 201

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
