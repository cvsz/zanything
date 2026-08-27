FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN addgroup --system zanything && adduser --system --ingroup zanything zanything
WORKDIR /app

COPY pyproject.toml /app/
COPY src/ /app/src/
RUN pip install --no-cache-dir /app

USER zanything
EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8080/healthz')"

CMD ["uvicorn", "zanything.app:app", "--host", "0.0.0.0", "--port", "8080", "--proxy-headers"]
