#!/bin/sh

exec gunicorn --workers=1 -k eventlet --bind 0.0.0.0:8000 gunicorn_app:app