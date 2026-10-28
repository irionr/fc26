#!/bin/sh
# Avvia il sito sulla LAN (porta 8000). Accessibile da altri dispositivi su http://<IP-di-questo-pc>:8000
cd "$(dirname "$0")"
.venv/bin/python manage.py migrate --noinput
IP=$(ipconfig getifaddr en0 2>/dev/null || hostname -I 2>/dev/null | cut -d' ' -f1)
echo "Apri da LAN: http://${IP:-<IP>}:8000"
exec .venv/bin/python manage.py runserver 0.0.0.0:8090
