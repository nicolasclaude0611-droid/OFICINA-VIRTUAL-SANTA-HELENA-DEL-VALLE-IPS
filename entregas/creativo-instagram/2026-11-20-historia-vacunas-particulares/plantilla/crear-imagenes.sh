#!/bin/bash
# Uso: bash crear-imagenes.sh A   (o B1, B2, B3). Necesita las fuentes Eras instaladas y Node con Playwright.
# Crea en ../<variación>/ las 3 pantallas de la historia en PNG (1080 × 1920).
set -e
V=${1:-A}; H="$(cd "$(dirname "$0")" && pwd)"; OUT="$H/../$V"; mkdir -p "$OUT"
for P in 1 2 3; do node "$H/capturar.js" "$V" $P "$OUT/pantalla-$P.png"; done
echo "Listo: $OUT"
