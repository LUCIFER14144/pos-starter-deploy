POS Starter (Django + DRF backend) and Frontend (React PWA minimal)

Folders:
 - backend/  -> Django project
 - frontend/ -> React PWA (minimal)

Quick start (backend):
 1. cd backend
 2. python -m venv .venv
 3. source .venv/bin/activate  # or .\\.venv\\Scripts\\activate on Windows
 4. pip install -r requirements.txt
 5. python manage.py migrate
 6. python manage.py createsuperuser
 7. python manage.py runserver

Quick start (frontend):
 1. cd frontend
 2. npm install
 3. npm start

Notes:
 - Backend runs on port 8000 by default. Frontend expects API at http://localhost:8000/api
 - Manager PIN is set to '1234' in backend/settings.py (DEV ONLY) — change it in production.
 - This starter is minimal: add auth, permissions, production settings before deploying.
