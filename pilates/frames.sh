#!/usr/bin/env bash
# Turns the photoreal Higgsfield videos into scroll frames.
# Usage: ./frames.sh <portrait.mp4> <landscape.mp4>
# Keeps every 2nd frame (336 → 168) as WebP: frames/p/000.webp … and frames/l/000.webp …
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
mkdir -p "$here/frames/p" "$here/frames/l"
ffmpeg -y -loglevel error -i "$1" -vf "select='not(mod(n\,2))',crop=iw-36:ih-36:18:18,scale=576:-2:flags=lanczos" -vsync vfr -start_number 0 -c:v libwebp -quality 72 "$here/frames/p/%03d.webp"
ffmpeg -y -loglevel error -i "$2" -vf "select='not(mod(n\,2))',scale=1280:720:flags=lanczos" -vsync vfr -start_number 0 -c:v libwebp -quality 72 "$here/frames/l/%03d.webp"
echo "portrait: $(ls "$here/frames/p" | wc -l) frames, $(du -sh "$here/frames/p" | cut -f1)"
echo "landscape: $(ls "$here/frames/l" | wc -l) frames, $(du -sh "$here/frames/l" | cut -f1)"
