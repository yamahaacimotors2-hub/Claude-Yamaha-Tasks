#!/bin/bash
# After render_all.sh: comp, soundtrack, encode, review copies, stills and technical QC.
# Usage: ./finish.sh FRAMES_DIR WORK_DIR [version]
set -e
FR=${1:?frames dir}; WK=${2:?work dir}; V=${3:-v001}
cd "$(dirname "$0")"
mkdir -p "$WK/final" 09_DELIVERY 08_REVIEW/stills 03_ANIMATIC
python3 06_COMP/post.py "$FR" "$WK/final"
python3 07_EDIT_SOUND/audio.py "$WK/mix.wav" 07_EDIT_SOUND/Sound_Cue_Sheet.csv
M=09_DELIVERY/MT15_master_${V}.mp4
ffmpeg -loglevel error -y -framerate 24 -i "$WK/final/%04d.png" -i "$WK/mix.wav" \
  -af "loudnorm=I=-14:TP=-1.5:LRA=11" -ar 48000 \
  -c:v libx264 -preset slow -crf 17 -maxrate 20M -bufsize 40M -pix_fmt yuv420p \
  -colorspace bt709 -color_primaries bt709 -color_trc bt709 \
  -c:a aac -b:a 256k -frames:v 384 -movflags +faststart "$M"
# mobile review / publish copy (SOP step 96): 1080x1920 H.264/AAC, 24 fps, Rec.709 SDR
ffmpeg -loglevel error -y -i "$M" -c:v libx264 -preset slow -crf 22 -maxrate 8M -bufsize 16M -pix_fmt yuv420p \
  -colorspace bt709 -color_primaries bt709 -color_trc bt709 -c:a aac -b:a 192k -movflags +faststart \
  09_DELIVERY/MT15_mobile_${V}.mp4
# review copy: shot ID and frame number burned in (SOP step 20)
DT=""; i=0
for row in "S01 0 30" "S02 30 50" "S03 50 62" "S04 62 96" "S05 96 126" "S06 126 150" "S07 150 164" \
           "S08 164 236" "S09 236 272" "S10 272 302" "S11 302 342" "S12 342 384"; do
  set -- $row
  DT="${DT}drawtext=text='$1':x=40:y=h-150:fontsize=54:fontcolor=white:box=1:boxcolor=black@0.55:boxborderw=12:enable='between(n,$2,$(($3-1)))',"
done
ffmpeg -loglevel error -y -i "$M" -vf "${DT}drawtext=text='%{frame_num}':start_number=0:x=w-tw-40:y=h-150:fontsize=44:fontcolor=white:box=1:boxcolor=black@0.55:boxborderw=12,scale=540:960" \
  -c:v libx264 -crf 22 -pix_fmt yuv420p -c:a aac -b:a 128k 08_REVIEW/MT15_review_burnin_${V}.mp4
# one still per shot (middle frame) for review and as Higgsfield start frames
for row in "S01 15" "S02 44" "S03 53" "S04 82" "S05 116" "S06 138" "S07 160" "S08 205" "S09 254" "S10 290" "S11 322" "S12 375"; do
  set -- $row; cp "$WK/final/$(printf %04d $2).png" "08_REVIEW/stills/$1.png"
done
ffmpeg -loglevel error -y -pattern_type glob -i "08_REVIEW/stills/S*.png" -vf "scale=270:480,tile=6x2" -frames:v 1 08_REVIEW/contact_sheet_${V}.jpg
ffmpeg -loglevel error -y -i "08_REVIEW/stills/S%02d.png" -vf "scale=540:960" -q:v 4 "$WK/still_%02d.jpg"
for f in 08_REVIEW/stills/S*.png; do ffmpeg -loglevel error -y -i "$f" -vf scale=720:1280 -q:v 3 "${f%.png}.jpg" && rm "$f"; done
# technical QC (SOP step 97)
{ echo "# ffprobe"; ffprobe -v error -select_streams v:0 -count_frames \
    -show_entries stream=codec_name,width,height,r_frame_rate,nb_read_frames,pix_fmt:format=duration,size -of default=nw=1 "$M";
  ffprobe -v error -select_streams a:0 -show_entries stream=codec_name,sample_rate,channels -of default=nw=1 "$M";
  echo "# decode errors (empty = none)"; ffmpeg -v error -i "$M" -f null - 2>&1;
  echo "# loudness"; ffmpeg -hide_banner -nostats -i "$M" -af ebur128=peak=true -f null - 2>&1 | grep -E "I:|Peak:" | tail -2; } > 08_REVIEW/technical_qc_${V}.txt
cat 08_REVIEW/technical_qc_${V}.txt
echo FINISH_DONE
