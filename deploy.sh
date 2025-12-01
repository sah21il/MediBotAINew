#!/bin/bash

echo "🚀 Deploying MediBot AI..."

# Start services
docker-compose up -d

echo "⏳ Waiting for services to start..."
sleep 30

# Check if services are running
echo "📊 Service Status:"
docker-compose ps

echo "✅ MediBot AI deployed successfully!"
echo "🌐 Frontend: http://localhost:5173"
echo "🔧 Backend API: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo "🤖 Ollama: http://localhost:11434"