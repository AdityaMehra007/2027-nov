FROM python:3.13-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY services/intelligence/ ./
RUN useradd --create-home --uid 10001 atlas
USER atlas
EXPOSE 8090
CMD ["python", "app.py"]
