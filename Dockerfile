# Stage 1: Builder - installs dependencies and clears cache
FROM python:3.9-slim-buster AS builder
WORKDIR /app
COPY requirements.txt .
RUN python -m pip install --no-cache-dir --prefix=/install -r requirements.txt \
    && rm -rf /root/.cache/pip

# Stage 2: Final image - optimized for production
FROM python:3.9-slim-buster
WORKDIR /app
COPY . .
RUN adduser --disabled-password --gecos "" appuser \
    && chown -R appuser:appuser /usr/local \
    && chown -R appuser:appuser /app
USER appuser
COPY --from=builder /install /usr/local
# Add environment variables for production
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
EXPOSE 5000
CMD ["waitress-serve", "--host=0.0.0.0", "--port=5000", "app_frontend:app"]
