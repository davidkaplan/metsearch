#!/bin/sh

rm -rf build/ dist/ ../__pycache__/
rm MET\ Search.spec
pyinstaller --name "MET Search" --windowed metsearch.py

test -f "dist/MET Search.dmg" && rm "dist/MET Search.dmg"
create-dmg \
  --volname "MET Search" \
  --hide-extension "MET Search.app" \
  "dist/MET Search.dmg" \
  "dist/MET Search.app/"