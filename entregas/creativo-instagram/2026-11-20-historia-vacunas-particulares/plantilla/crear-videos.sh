#!/bin/bash
# Uso: bash crear-videos.sh A   (o B1, B2, B3). Necesita las fuentes Eras instaladas, Node con Playwright y ffmpeg.
# Crea en ../<variación>/ las 3 pantallas en PNG (sin Helenita) y en MP4 de 7 s (con Helenita animada).
set -e
V=${1:-A}; H="$(cd "$(dirname "$0")" && pwd)"; OUT="$H/../$V"; mkdir -p "$OUT"
node "$H/capturar.js" "$V" 1 "$OUT/frente.png" frente
for P in 1 2 3; do
  node "$H/capturar.js" "$V" $P "$OUT/pantalla-$P.png"
  ffmpeg -v error -y -loop 1 -framerate 30 -t 7 -i "$OUT/pantalla-$P.png" \
    -stream_loop -1 -c:v libvpx-vp9 -i "$H/img/invitar.webm" -loop 1 -framerate 30 -t 7 -i "$OUT/frente.png" \
    -filter_complex "[1:v]scale=900:900,fps=30[hel];[0:v][hel]overlay=x=-190:y=900:shortest=1[a];[a][2:v]overlay=0:0,fade=t=in:st=0:d=0.4,format=yuv420p[v]" \
    -map "[v]" -t 7 -r 30 -c:v libx264 -crf 20 -preset medium -movflags +faststart "$OUT/pantalla-$P.mp4"
done
rm "$OUT/frente.png"
echo "Listo: $OUT"
