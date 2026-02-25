import os
import socket
import logging
from datetime import datetime, timezone
from functools import wraps

from flask import Flask, request, jsonify, g
from werkzeug.security import generate_password_hash, check_password_hash
import jwt

# ── Logging ──────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s"
)
logger = logging.getLogger(__name__)

# ── App Factory ───────────────────────────────────────────────────────────────
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    register_routes(app)
    return app

# ── Config ────────────────────────────────────────────────────────────────────
class Config:
    SECRET_KEY        = os.environ.get("SECRET_KEY")          # REQUIRED in prod
    JWT_ALGORITHM     = "HS256"
    JWT_EXP_SECONDS   = int(os.environ.get("JWT_EXP_SECONDS", 3600))
    ENV               = os.environ.get("FLASK_ENV", "production")
    DEBUG             = ENV == "development"

# ── Fake user store (replace with DB later) ───────────────────────────────────
# Password is stored hashed — never store plaintext passwords
USERS = {
    "admin": generate_password_hash(os.environ.get("ADMIN_PASSWORD", "change-me-in-env"))
}

# ── Auth decorator ────────────────────────────────────────────────────────────
def require_json(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not request.is_json:
            return jsonify({"error": "Content-Type must be application/json"}), 415
        return f(*args, **kwargs)
    return decorated

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return jsonify({"error": "Missing or invalid Authorization header"}), 401
        token = auth_header.split(" ", 1)[1]
        try:
            payload = jwt.decode(token, Config.SECRET_KEY, algorithms=[Config.JWT_ALGORITHM])
            g.current_user = payload["sub"]
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401
        return f(*args, **kwargs)
    return decorated

# ── Routes ────────────────────────────────────────────────────────────────────
def register_routes(app):

    @app.route("/")
    def home():
        return jsonify({
            "message": "Docker Multi-Container App",
            "version": os.environ.get("APP_VERSION", "1.0.0"),
            "env": Config.ENV
        })

    @app.route("/health")
    def health():
        """Liveness probe — used by Docker / Kubernetes."""
        return jsonify({
            "status":    "ok",
            "hostname":  socket.gethostname(),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "database":  "not_connected"   # swap for real DB ping later
        }), 200

    @app.route("/ready")
    def ready():
        """Readiness probe — only returns 200 when truly ready to serve traffic."""
        # TODO: add real DB check here
        db_ok = True   # replace with: ping_database()
        if db_ok:
            return jsonify({"status": "ready"}), 200
        return jsonify({"status": "not_ready", "reason": "database unreachable"}), 503

    @app.route("/login", methods=["POST"])
    @require_json
    def login():
        data     = request.get_json()
        username = data.get("username", "").strip()
        password = data.get("password", "")

        if not username or not password:
            return jsonify({"error": "username and password are required"}), 400

        hashed = USERS.get(username)
        if not hashed or not check_password_hash(hashed, password):
            logger.warning("Failed login attempt for user: %s | IP: %s", username, request.remote_addr)
            return jsonify({"error": "Invalid credentials"}), 401   # same message for both cases (no user enumeration)

        import time
        token = jwt.encode(
            {
                "sub": username,
                "iat": int(time.time()),
                "exp": int(time.time()) + Config.JWT_EXP_SECONDS
            },
            Config.SECRET_KEY,
            algorithm=Config.JWT_ALGORITHM
        )

        logger.info("Successful login for user: %s | IP: %s", username, request.remote_addr)
        return jsonify({"token": token, "expires_in": Config.JWT_EXP_SECONDS}), 200

    @app.route("/protected")
    @require_auth
    def protected():
        """Example of a JWT-protected endpoint."""
        return jsonify({"message": f"Hello, {g.current_user}. You are authenticated."}), 200

    # ── Error handlers ────────────────────────────────────────────────────────
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "Resource not found"}), 404

    @app.errorhandler(405)
    def method_not_allowed(e):
        return jsonify({"error": "Method not allowed"}), 405

    @app.errorhandler(500)
    def internal_error(e):
        logger.exception("Unhandled exception: %s", e)
        return jsonify({"error": "Internal server error"}), 500


# ── Entrypoint (dev only — use gunicorn in production) ────────────────────────
app = create_app()

if __name__ == "__main__":
    if not Config.SECRET_KEY:
        raise RuntimeError("SECRET_KEY environment variable is not set!")
    app.run(host="0.0.0.0", port=5000, debug=Config.DEBUG)
