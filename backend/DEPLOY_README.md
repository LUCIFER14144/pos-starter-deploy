Render deployment notes

- This project includes a Dockerfile for the backend (backend/Dockerfile).
- render.yaml is provided to create a web service (docker) for the backend and a static site for the frontend build.

Suggested Render steps:
1. Push repo to GitHub.
2. In Render, select "New -> From Existing Repo" and choose the repo.
3. Render will read render.yaml and create services. Set the following environment variables in Render for the web service:
   SECRET_KEY: (generate a secure key)
   DEBUG: False
   ALLOWED_HOSTS: your-backend-render-domain (or * temporarily)
   DATABASE_URL: (if using Postgres or leave blank to use SQLite inside container)
   MANAGER_PIN: (choose secure PIN)
   CORS_ALLOWED_ORIGINS: https://your-frontend.vercel.app

If you prefer, use Render's managed Postgres and set DATABASE_URL accordingly.
