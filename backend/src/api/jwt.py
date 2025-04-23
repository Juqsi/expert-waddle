import os
import json
import base64
import hashlib
import hmac
from fastapi import HTTPException

# Lies dir einen „Secret“ aus der Env, Standard ist hier nur für Demo
SECRET_KEY = os.getenv("JWT_SECRET", "insecure-demo-secret")

def _b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")

def _b64url_decode(data: str) -> bytes:
    padding = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)

def create_jwt_sha256(payload: dict) -> str:
    """
    Erstellt ein JWT mit Header.alg='HS256', Signatur via HMAC-SHA256.
    """
    header = {"typ": "JWT", "alg": "HS256"}
    print("[JWT_SECRET]" + SECRET_KEY)
    # 1) Header und Payload serialisieren & Base64URL-encodieren
    h = _b64url_encode(json.dumps(header, separators=(",", ":")).encode())
    p = _b64url_encode(json.dumps(payload, separators=(",", ":")).encode())
    signing_input = f"{h}.{p}".encode()
    # 2) HMAC-SHA256 Signature
    sig = hmac.new(SECRET_KEY.encode(), signing_input, hashlib.sha256).digest()
    s = _b64url_encode(sig)
    # 3) Token zusammensetzen
    return f"{h}.{p}.{s}"

def verify_jwt_sha256(token: str) -> dict:
    """
    Verifiziert das HS256-JWT. Gibt die Payload zurück oder wirft eine Exception.
    """
    try:
        h, p, s = token.split(".")
    except ValueError:
        raise HTTPException(status_code=400, detail="Token-Format ungültig")

    signing_input = f"{h}.{p}".encode()
    # erneute SHA256-HMAC
    expected_sig = _b64url_encode(
        hmac.new(SECRET_KEY.encode(), signing_input, hashlib.sha256).digest()
    )
    if not hmac.compare_digest(s, expected_sig):
        raise HTTPException(status_code=401, detail="Token ungültig oder verfälscht")

    # Payload decodieren
    payload_json = _b64url_decode(p)
    return json.loads(payload_json)
