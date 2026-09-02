#!/usr/bin/env bash
set -euo pipefail

python3 build.py

printf '\nBuilt guide pages:\n'
find dist/guides -name index.html -print | sort
printf '\nAsset references:\n'
find dist -path '*/demo-guide.svg' -o -path '*/local-guide-image.svg' | sort
