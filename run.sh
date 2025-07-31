#!/bin/bash
set -e

TARGET=${1:-bert}
PROFILE_NAME=data/profile_$TARGET
PLOT_PATH=data/kernel_plot.png

echo "🧠 Profiling target: $TARGET"

docker compose run --rm kernalyse \
    bash -c "cd /workspace && nsys profile -t cuda -o $PROFILE_NAME --force-overwrite true \
    python3 -m interface.cli.main profile --target=$TARGET"

echo "📊 Visualization saved to: $PLOT_PATH"

# Open image on host
if command -v xdg-open &> /dev/null; then
    xdg-open $PLOT_PATH
elif command -v open &> /dev/null; then
    open $PLOT_PATH  # macOS
else
    echo "📎 Please open $PLOT_PATH manually — no opener found"
fi
