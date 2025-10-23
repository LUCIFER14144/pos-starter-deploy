# Official Python runtime as a parent image
FROM python:3.11-slim

# set workdir
WORKDIR /app

# install deps
COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# copy project files
COPY . /app

# collect static
ENV PYTHONUNBUFFERED=1
RUN python manage.py collectstatic --noinput || true

# run migrations on container start (optional: in render use release commands instead)
# CMD python manage.py migrate && gunicorn pos_backend.wsgi:application --bind 0.0.0.0:8000
CMD gunicorn pos_backend.wsgi:application --bind 0.0.0.0:8000 --workers 3
