# MediBot AI - Intelligent Health Monitoring System

🏥 **AI-powered medical assistant for real-time vital signs analysis and clinical decision support**

##  Features

- **Real-time Vital Signs Analysis**: Monitor heart rate, blood pressure, SpO2, and temperature
- **AI-Powered Clinical Decisions**: Uses Ollama LLM for intelligent medical recommendations
- **Multi-Agent Architecture**: Specialized agents for health monitoring, data ingestion, and doctor assistance
- **Interactive Dashboard**: React-based frontend with real-time data visualization
- **RESTful API**: FastAPI backend with comprehensive endpoints

##  Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React Frontend │────│  FastAPI Backend │────│   Ollama LLM    │
│   (Port 5173)   │    │   (Port 8000)   │    │  (Port 11434)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │              ┌─────────────────┐              │
         └──────────────│  Message Bus    │──────────────┘
                        │   Coordinator   │
                        └─────────────────┘
                                 │
                    ┌────────────┼────────────┐
                    │            │            │
            ┌───────────┐ ┌─────────────┐ ┌──────────────┐
            │Health Agent│ │Ingest Agent │ │Doctor Assistant│
            └───────────┘ └─────────────┘ └──────────────┘
```

## 🛠️ Setup Instructions

### Prerequisites
- Python 3.11+
- Node.js 18+
- Git

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/MediBotAI.git
cd MediBotAI
```

### 2. Backend Setup
```bash
cd MediBotAINew-main

# Install Python dependencies
pip install -r requirements.txt

# Install and setup Ollama
curl -fsSL https://ollama.com/install.sh | sh
ollama serve &
ollama pull phi3:mini

# Start backend server
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 3. Frontend Setup
```bash
cd ../frontend

# Install Node dependencies
npm install

# Start development server
npm run dev
```

### 4. Access Application
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## Environment Variables

Create `.env` file in backend directory:
```env
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=phi3:mini
API_PORT=8000
FRONTEND_URL=http://localhost:5173
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| POST | `/api/health/analyze` | Analyze vital signs |
| GET | `/ingest/latest` | Get latest mock vitals |
| POST | `/api/doctor-assistant/analyze` | Doctor assistant analysis |

### Sample Request
```bash
curl -X POST "http://localhost:8000/api/health/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "resp_rate": 28,
    "spo2": 90,
    "bp_sys": 180,
    "pulse": 130,
    "temp": 38.5,
    "consciousness": "Voice"
  }'
```

##  Testing

```bash
# Run backend tests
cd MediBotAINew-main
python -m pytest tests/

# Run frontend tests
cd frontend
npm test
```

##  Deployment

### GitHub Codespaces (Recommended for Demo)
1. Open repository in GitHub Codespaces
2. Follow setup instructions above
3. Make ports 8000 and 5173 public
4. Share the generated URLs

### Docker Deployment
```bash
docker-compose up --build
```

##  Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

##  License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

##  Team

- **Healthcare AI Specialists**
- **Full-Stack Developers** 
- **Medical Domain Experts**
