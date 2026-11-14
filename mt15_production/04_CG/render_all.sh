#!/bin/bash
# Renders every CG shot of the film as PNG sequences.  Usage: ./render_all.sh /path/to/frames_dir
set -e
OUT=${1:?frames dir}
cd "$(dirname "$0")"
for SHOT in BG12 S08 S09 S10 S01 S11 S02 S03 S04 S05 S06 S07; do
  python3 film.py --shot $SHOT --out "$OUT/$SHOT" > "$OUT/$SHOT.log" 2>&1 || { echo "FAILED $SHOT"; tail -5 "$OUT/$SHOT.log"; exit 1; }
  echo "DONE $SHOT $(ls "$OUT/$SHOT" | wc -l) frames $(date +%H:%M:%S)"
done
echo ALL_SHOTS_DONE
