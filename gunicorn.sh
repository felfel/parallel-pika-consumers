#!/bin/sh

exec gunicorn --workers=2 -k eventlet --bind 0.0.0.0:8000 gunicorn_app:app