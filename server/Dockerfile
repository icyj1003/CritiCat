FROM python:3.10-slim

WORKDIR /app
COPY server.py /app/
COPY api.py /app/
COPY requirements.txt /app/
COPY entrypoint.sh /app/
RUN chmod +x /app/entrypoint.sh

EXPOSE 8001
EXPOSE 8002

RUN python3 -m pip install -r /app/requirements.txt

ENTRYPOINT ["sh", "/app/entrypoint.sh"]