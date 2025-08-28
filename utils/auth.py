from datetime import datetime, timedelta, timezone
import os
from typing import Any, Dict, Optional, Tuple
import uuid

import jwt
from flask import Request, g
from werkzeug.security import generate_password_hash, check_password_hash


def _get_jwt_secret() -> str:
    return os.environ.get("JWT_SECRET", "dev_secret_change_me")


def create_access_and_refresh_tokens(user_id: str, extra_claims: Optional[Dict[str, Any]] = None) -> Tuple[str, str]:
    now = datetime.now(tz=timezone.utc)
    payload_common: Dict[str, Any] = {
        "sub": str(user_id),
        "iat": int(now.timestamp()),
    }
    if extra_claims:
        payload_common.update(extra_claims)
    
    access_payload = {
        **payload_common,
        "type": "access",
        "exp": int((now + timedelta(minutes=15)).timestamp()),
    }
    refresh_payload = {
        **payload_common,
        "type": "refresh",
        "exp": int((now + timedelta(days=7)).timestamp()),
    }
    
    secret = _get_jwt_secret()
    access_token = jwt.encode(access_payload, secret, algorithm="HS256")
    refresh_token = jwt.encode(refresh_payload, secret, algorithm="HS256")
    return access_token, refresh_token


def decode_token(token: str) -> Optional[Dict[str, Any]]:
    try:
        return jwt.decode(token, _get_jwt_secret(), algorithms=["HS256"])  # type: ignore[no-any-return]
    except jwt.PyJWTError:
        return None


def extract_bearer_token(request: Request) -> Optional[str]:
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return None
    return auth_header.split(" ", 1)[1].strip()


def require_auth(fn):
    from functools import wraps
    from flask import jsonify, request

    @wraps(fn)
    def wrapper(*args, **kwargs):
        token = extract_bearer_token(request)
        if not token:
            return jsonify({"error": "Unauthorized"}), 401
        payload = decode_token(token)
        if not payload or payload.get("type") != "access":
            return jsonify({"error": "Unauthorized"}), 401
        g.current_user_id = str(payload.get("sub"))
        g.token_payload = payload
        return fn(*args, **kwargs)

    return wrapper


def hash_password(password: str) -> str:
    """Hash a password using werkzeug"""
    return generate_password_hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return check_password_hash(hashed_password, password)


def generate_verification_token() -> str:
    """Generate a random verification token"""
    return str(uuid.uuid4())


def generate_reset_token() -> str:
    """Generate a random password reset token"""
    return str(uuid.uuid4())


