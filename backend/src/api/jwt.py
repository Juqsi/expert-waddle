import os
import json
import base64
import hashlib
import hmac

# Lies dir einen „Secret“ aus der Env, Standard ist hier nur für Demo
SECRET_KEY = os.getenv("JWT_SECRET", "insecure-demo-secret")

def _b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")

def _b64url_decode(data: str) -> bytes:
    padding = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)

def create_jwt_md5(payload: dict) -> str:
    """
    Erstellt ein JWT mit Header.alg='MD5', Signatur via HMAC-MD5.
    """
    header = {"typ": "JWT", "alg": "MD5"}
    # 1) Header und Payload serialisieren & base64url‑encodieren
    h = _b64url_encode(json.dumps(header, separators=(",", ":")).encode())
    p = _b64url_encode(json.dumps(payload, separators=(",", ":")).encode())
    signing_input = f"{h}.{p}".encode()
    # 2) HMAC‑MD5 Signature
    sig = hmac.new(SECRET_KEY.encode(), signing_input, hashlib.md5).digest()
    s = _b64url_encode(sig)
    # 3) Token zusammensetzen
    return f"{h}.{p}.{s}"

def verify_jwt_md5(token: str) -> dict:
    """
    Verifiziert das MD5‑JWT. Gibt die Payload zurück oder wirft eine Exception.
    """
    try:
        h, p, s = token.split(".")
    except ValueError:
        raise HTTPException(status_code=400, detail="Token-Format ungültig")

    signing_input = f"{h}.{p}".encode()
    # erneute MD5‑HMAC
    expected_sig = _b64url_encode(
        hmac.new(SECRET_KEY.encode(), signing_input, hashlib.md5).digest()
    )
    if not hmac.compare_digest(s, expected_sig):
        raise HTTPException(status_code=401, detail="Token ungültig oder verfälscht")

    # Payload decodieren
    payload_json = _b64url_decode(p)
    return json.loads(payload_json)
