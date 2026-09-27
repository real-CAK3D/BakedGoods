#!/usr/bin/env bash
# After CHRONIC's baking day: reprint Baked Goods and The Green Thumb (Bedded Roots), ring the bell if new recipes came out of the oven.
set -u
D="$HOME/.hermes/garden/baked-goods"; PY="$HOME/.hermes/hermes-agent/venv/bin/python"
BEFORE=$(cat "$D/.recipe-count" 2>/dev/null || echo 0)
cd "$D" && "$PY" build_baked.py
(cd "$HOME/.hermes/garden/green-thumb" && /usr/bin/python3 build_green_thumb.py)
NOW=$(ls "$D"/recipes/*.json 2>/dev/null | wc -l); echo "$NOW" > "$D/.recipe-count"
[ "$NOW" -gt "$BEFORE" ] && "$PY" "$HOME/.hermes/garden/newsstand/notify.py" "🧁 Fresh out of the oven" "$((NOW-BEFORE)) new recipe(s) in Baked Goods." "/baked-goods/"
exit 0
