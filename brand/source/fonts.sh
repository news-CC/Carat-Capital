#!/bin/bash
# Fetches the OFL typefaces the marks are drawn from (Google Fonts), into ./fonts.
cd "$(dirname "$0")" && mkdir -p fonts
get() { if [ -n "$2" ]; then url="https://fonts.googleapis.com/css2?family=$1:wght@$2"; else url="https://fonts.googleapis.com/css2?family=$1"; fi; ttf=$(curl -sS -A "Mozilla/4.0" "$url" | grep -o 'https://fonts.gstatic.com[^)]*' | head -1); curl -sS -o "fonts/$3" "$ttf" && echo "fonts/$3"; }
get "Bodoni+Moda" 500 bodoni500.ttf
get "Bodoni+Moda:opsz,wght@28,500" "" bodoni500o28.ttf
get "Bodoni+Moda" 700 bodoni700.ttf
get "Castoro+Titling" 400 castorotitling.ttf
get "Gloock" 400 gloock.ttf
get "IBM+Plex+Mono" 500 plexmono500.ttf
