# 🚀 MediBot AI Deployment Guide

## Quick Deploy Options

### 1. GitHub Codespaces (Recommended)
```bash
# Open in GitHub Codespaces
# Ports will auto-forward: 8000 (API), 5173 (Frontend), 11434 (Ollama)
docker-compose up -d
```

### 2. Local Docker Deployment
```bash
# Clone and deploy
git clone <your-repo-url>
cd MediBotAI
chmod +x deploy.sh
./deploy.sh
```

### 3. Manual Setup
```bash
# Backend
cd MediBotAINew-main
pip install -r requirements.txt
ollama serve &
ollama pull phi3:mini
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Frontend (new terminal)
cd frontend
npm install
npm run dev
```

## 🌐 Access URLs
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Ollama**: http://localhost:11434

## 🔧 Environment Variables
Create `.env` in backend directory:
```env
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=phi3:mini
API_PORT=8000
FRONTEND_URL=http://localhost:5173
```

## 📱 Features Ready for Demo
- ✅ Real-time Health Monitoring with Alarms
- ✅ AI-Powered Doctor Assistant Chat
- ✅ Smart Reminders with Medical Recommendations
- ✅ PDF Report Analysis
- ✅ Dark Theme Medical Dashboard
- ✅ Multi-Agent Architecture

## 🎯 Demo Flow
1. **Dashboard** → Overview of all agents
2. **Health Monitor** → Real-time vitals with alarms
3. **Doctor Assistant** → AI medical chat
4. **Reminders** → Smart medication/appointment reminders
5. **Reports** → Upload and analyze medical PDFs

## 🔒 Production Notes
- Enable HTTPS for production
- Configure proper CORS settings
- Set up persistent data storage
- Implement user authentication
- Add monitoring and logging