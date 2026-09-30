FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY impact_melt_volume_estimator.py .

EXPOSE 7860

CMD ["python", "app.py"]
