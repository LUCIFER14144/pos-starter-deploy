# POS Starter Deploy

A Point of Sale starter application with Django DRF backend and React PWA frontend.

## 🚀 Deployment

### Frontend (Vercel)
This project is configured for easy deployment on Vercel:

1. **Fork or Clone** this repository
2. **Connect to Vercel**:
   - Go to [vercel.com](https://vercel.com)
   - Import your GitHub repository
   - Vercel will automatically detect it as a React app

3. **Environment Variables** (Optional):
   - Set `REACT_APP_API_URL` to your backend API URL
   - For testing, you can use the included mock API

### Backend (Render/Railway/Heroku)
The backend includes Docker configuration and can be deployed to:
- **Render**: Use the included `render.yaml`
- **Railway**: Connect your GitHub repo
- **Heroku**: Use the included `Procfile`

## 🏗️ Architecture

```
pos-starter-deploy/
├── frontend/          # React PWA
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── .env.example
├── backend/           # Django + DRF
│   ├── core/         # Main app
│   ├── pos_backend/  # Project settings
│   ├── Dockerfile
│   ├── requirements.txt
│   └── Procfile
├── vercel.json       # Vercel config
└── render.yaml       # Render config
```

## 🔧 Local Development

### Backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Frontend
```bash
cd frontend
npm install
npm start
```

## 🌐 Live Demo

- **Frontend**: [Deployed on Vercel](https://your-app.vercel.app)
- **Backend**: [API Documentation](https://your-backend.onrender.com/api/)

## 📝 Features

- ✅ POS Interface
- ✅ Product Management
- ✅ Sales Processing
- ✅ PWA Support
- ✅ Responsive Design
- ✅ Docker Ready
- ✅ Environment Config

## 🔒 Security Notes

- Change the `MANAGER_PIN` in production
- Update `SECRET_KEY` for Django
- Configure proper CORS settings
- Set up authentication for production use

---

Built with ❤️ using Django, React, and modern deployment practices.