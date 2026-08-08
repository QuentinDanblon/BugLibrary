#!/bin/bash
# recon_pipeline.sh — Pipeline de reconnaissance incrémental
# Usage : ./recon_pipeline.sh <target-domain>
# Prérequis : subfinder, httpx, dnsx installés (voir tools/README.md)
#
# ⚠️ Vérifier les règles du programme (rate limiting, scan autorisé) avant exécution.
# Voir docs/11-Legal-Ethics-and-OPSEC/README.md

set -euo pipefail

TARGET="${1:?Usage: $0 <target-domain>}"
OUTDIR="recon_output/${TARGET}"
mkdir -p "${OUTDIR}"

TODAY=$(date +%Y-%m-%d)
CURRENT_SUBS="${OUTDIR}/subs_${TODAY}.txt"
PREVIOUS_SUBS="${OUTDIR}/subs_latest.txt"
NEW_SUBS="${OUTDIR}/new_subs_${TODAY}.txt"

echo "[*] Subdomain enumeration for ${TARGET}..."
subfinder -d "${TARGET}" -all -silent -o "${CURRENT_SUBS}"

if [ -f "${PREVIOUS_SUBS}" ]; then
    comm -13 <(sort "${PREVIOUS_SUBS}") <(sort "${CURRENT_SUBS}") > "${NEW_SUBS}" || true
    if [ -s "${NEW_SUBS}" ]; then
        echo "[+] New subdomains found:"
        cat "${NEW_SUBS}"
    else
        echo "[*] No new subdomains since last run."
    fi
else
    echo "[*] First run — no baseline to diff against."
    cp "${CURRENT_SUBS}" "${NEW_SUBS}"
fi

cp "${CURRENT_SUBS}" "${PREVIOUS_SUBS}"

echo "[*] Probing alive hosts..."
httpx -l "${CURRENT_SUBS}" -status-code -title -tech-detect -silent -o "${OUTDIR}/alive_${TODAY}.txt"

echo "[*] Done. Results in ${OUTDIR}/"
