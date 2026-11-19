#!/usr/bin/env bash
# Turns the upscaled photoreal Higgsfield videos into scroll frames.
# Usage: ./frames.sh <portrait-2k.mp4> <landscape-2k.mp4>
# Keeps every 2nd frame (336 → 169) as WebP: frames/p/000.webp … and frames/l/000.webp …
# Portrait source has a thin rounded border from the video model: cropped off.
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
mkdir -p "$here/frames/p" "$here/frames/l"
sharp="unsharp=5:5:0.45:5:5:0"
ffmpeg -y -loglevel error -i "$1" -vf "select='not(mod(n\,2))',crop=iw-80:ih-80:40:40,scale=1080:-2:flags=lanczos,$sharp" -vsync vfr -start_number 0 -c:v libwebp -quality 70 "$here/frames/p/%03d.webp"
ffmpeg -y -loglevel error -i "$2" -vf "select='not(mod(n\,2))',scale=1920:1080:flags=lanczos,$sharp" -vsync vfr -start_number 0 -c:v libwebp -quality 70 "$here/frames/l/%03d.webp"
echo "portrait: $(ls "$here/frames/p" | wc -l) frames, $(du -sh "$here/frames/p" | cut -f1)"
echo "landscape: $(ls "$here/frames/l" | wc -l) frames, $(du -sh "$here/frames/l" | cut -f1)"
