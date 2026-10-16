#!/bin/sh
set -eu

: "${PROMETHEUS_MULTIPROC_DIR:=/tmp/prometheus_multiproc}"
export PROMETHEUS_MULTIPROC_DIR

mkdir -p "$PROMETHEUS_MULTIPROC_DIR"
find "$PROMETHEUS_MULTIPROC_DIR" -maxdepth 1 -type f -delete

exec gunicorn app:app \
  -b 0.0.0.0:80 \
  --log-file - \
  --access-logfile - \
  --workers 4 \
  --keep-alive 0
