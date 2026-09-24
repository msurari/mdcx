#!/bin/sh
# jlesage/baseimage-gui runs this as the app user (USER_ID) with DISPLAY already set,
# after the cont-init.d scripts have run.
set -e

cd /app

echo "[startapp] MDCx (English fork) — running from source"
echo "[startapp] revision : $(cat /app/.revision 2>/dev/null || echo unknown)"
echo "[startapp] language : ${MDCX_LANG:-en (default)}"
echo "[startapp] python   : $(/opt/venv/bin/python -V 2>&1)"
if [ -f /app/MDCx.config ]; then
    echo "[startapp] config   : $(cat /app/MDCx.config)  (marker file)"
else
    echo "[startapp] config   : NO MARKER at /app/MDCx.config — the app will use its v1 default"
fi
echo "[startapp] scan dir : (see the 刮削目录 setting inside the app)"

exec /opt/venv/bin/python /app/main.py
