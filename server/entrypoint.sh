#!/bin/bash
exec python3 -u server.py &
exec uvicorn api:app --host 0.0.0.0 --port 8002
