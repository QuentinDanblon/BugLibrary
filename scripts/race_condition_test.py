#!/usr/bin/env python3
"""
race_condition_test.py — Squelette de test de race condition (HTTP).

Usage : python3 race_condition_test.py <url> --requests 20 [--method POST] [--data '{"code":"PROMO10"}']

Envoie N requêtes identiques en parallèle pour tenter de déclencher une race
condition (TOCTOU) sur un endpoint applicant un état "vérifier puis agir"
(coupon, retrait, inscription à quota limité).

Pour la technique la plus fiable (HTTP/2 single-packet attack), voir Turbo
Intruder (extension Burp) documentée dans docs/03-Web-Application-Hunting/05-Business-Logic.md
— ce script est un fallback simple en pur Python (threads), moins précis que
Turbo Intruder mais utile pour une vérification rapide sans Burp.

⚠️ Respecter le scope et les règles de rate limiting du programme ciblé.
Voir docs/11-Legal-Ethics-and-OPSEC/README.md.
"""
import argparse
import concurrent.futures
import json
import sys

import requests


def fire_request(url: str, method: str, headers: dict, data: str | None):
    try:
        resp = requests.request(method, url, headers=headers, data=data, timeout=10)
        return resp.status_code, resp.text[:200]
    except requests.RequestException as exc:
        return None, str(exc)


def main():
    parser = argparse.ArgumentParser(description="Race condition test harness (Python fallback).")
    parser.add_argument("url")
    parser.add_argument("--requests", type=int, default=20, help="Nombre de requêtes parallèles")
    parser.add_argument("--method", default="POST")
    parser.add_argument("--data", default=None, help="Corps de la requête (JSON string)")
    parser.add_argument("--header", action="append", default=[], help="Header custom 'Name: Value', répétable")
    args = parser.parse_args()

    headers = {}
    for h in args.header:
        if ":" not in h:
            print(f"[!] Header ignoré (format invalide) : {h}", file=sys.stderr)
            continue
        name, value = h.split(":", 1)
        headers[name.strip()] = value.strip()

    if args.data and "Content-Type" not in headers:
        headers["Content-Type"] = "application/json"

    print(f"[*] Envoi de {args.requests} requêtes {args.method} en parallèle vers {args.url}")

    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.requests) as executor:
        futures = [
            executor.submit(fire_request, args.url, args.method, headers, args.data)
            for _ in range(args.requests)
        ]
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())

    success_count = sum(1 for status, _ in results if status and 200 <= status < 300)
    print(f"[+] Réponses 2xx obtenues : {success_count} / {args.requests}")
    print("[*] Si success_count > 1 sur une opération censée être appliquée une seule fois,")
    print("    la race condition est probablement confirmée — analyser les réponses en détail.")

    for i, (status, body) in enumerate(results):
        print(f"  [{i}] status={status} body_preview={body!r}")


if __name__ == "__main__":
    main()
