FROM python:3.11-slim

# Arbeitsverzeichnis im Container
WORKDIR /app

# Requirements zuerst installieren (besseres Caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Rest des Codes kopieren
COPY . .

# Statische Dateien sammeln
RUN python manage.py collectstatic --noinput

# Port freigeben
EXPOSE 8000

# App starten
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
