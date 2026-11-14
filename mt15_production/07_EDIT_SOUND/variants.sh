#!/bin/bash
# After finish.sh: the same picture with each of the four music tracks, as phone copies for choosing one.
# Usage: 07_EDIT_SOUND/variants.sh WORK_DIR vNNN      (run from mt15_production/)
set -e
WK=${1:?work dir}; V=${2:?version}
loud() { ffmpeg -hide_banner -nostats -i "$1" -af ebur128 -f null - 2>&1 | grep "I:" | tail -1 | awk '{print $2}'; }
for T in A B C D; do
  OUT=09_DELIVERY/MT15_mobile_${V}_music${T}.mp4
  python3 07_EDIT_SOUND/audio.py "$WK/mix_$T.wav" - $T > /dev/null
  GAIN=$(python3 -c "print(round(-14.0 - ($(loud "$WK/mix_$T.wav")), 2))")
  ffmpeg -loglevel error -y -i 09_DELIVERY/MT15_mobile_${V}.mp4 -i "$WK/mix_$T.wav" -map 0:v -map 1:a -c:v copy \
    -af "volume=${GAIN}dB,alimiter=limit=0.84:attack=2:release=60:level=disabled" -ar 48000 -c:a aac -b:a 192k \
    -movflags +faststart "$OUT"
  echo "$T gain ${GAIN} dB -> $(loud "$OUT") LUFS"
done
