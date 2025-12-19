
FROM python:3.9-slim
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN addgroup --system appgroup && adduser --system appuser --ingroup appgroup
WORKDIR /app
COPY api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY api/ .
RUN chown -R appuser:appgroup /app
USER appuser
EXPOSE 5000
CMD ["python", "app.py"]
