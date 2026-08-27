FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN addgroup --system anything && adduser --system --ingroup anything anything
WORKDIR /app

COPY enterprise/api/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY enterprise/api /app/api
COPY enterprise/gui /app/gui

USER anything
EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8080/healthz')"

CMD ["uvicorn","api.app:app","--host","0.0.0.0","--port","8080","--proxy-headers"]
