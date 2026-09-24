#!/bin/sh
# Runs as root at container start, before startapp.sh.
# The image is built with USER_ID/GROUP_ID baked in, but those can be overridden at
# run time — so re-own the paths the app writes to, or a changed USER_ID cannot save
# its config.
set -e

: "${USER_ID:=1000}"
: "${GROUP_ID:=$USER_ID}"

for d in /app /app/userdata /app/Log /mdcx-config; do
    if [ -d "$d" ]; then
        chown -R "$USER_ID:$GROUP_ID" "$d" 2>/dev/null || true
    fi
done

exit 0
