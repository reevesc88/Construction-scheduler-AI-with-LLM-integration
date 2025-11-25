# 🏗️ Construction AI Planner - Full Stack Repository

A production-ready AI-powered construction project planning system with integrated GPT capabilities, multi-agent orchestration, and advanced scheduling analysis.

## 🎯 Overview

This repository provides:
- **Backend API** (FastAPI): Ingests construction documents, generates execution plans with costs and risks
- **Frontend Dashboard** (Streamlit): Visual interface for plan viewing and analysis
- **GPT Integration Ready**: OpenAPI spec for connecting to OpenAI Custom GPTs
- **Multi-Agent System**: Supervisor, Scheduler, Risk Analyzer, and Cost Estimator agents
- **Advanced Features**: CPM scheduling, GraphRAG retrieval, dynamic cost estimation, risk quantification

## 🚀 Quick Start

### Option 1: Docker Compose (Recommended)
```bash
# Clone the repository
git clone https://github.com/yourusername/construction-ai-planner.git
cd construction-ai-planner

# Set up environment
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY

# Run entire stack
docker-compose up --build
```

Then access:
- **Frontend Dashboard**: http://localhost:8501
- **Backend Swagger**: http://localhost:8000/docs
- **API Endpoint**: http://localhost:8000

### Option 2: Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Set environment
export OPENAI_API_KEY="sk-..."
export LLM_PROVIDER="openai"

# Run backend
uvicorn backend/src/main:app --reload --port 8000

# In another terminal, run frontend
streamlit run frontend/app.py
```

## 📋 API Endpoints

### 1. Ingest Document
**POST** `/ingest/document`

Upload a construction specification PDF.

```bash
curl -F "file=@spec.pdf" http://localhost:8000/ingest/document
```

**Response:**
```json
{
  "status": "success",
  "document_id": "doc_abc123",
  "filename": "spec.pdf",
  "chunks_indexed": 24
}
```

### 2. Generate Plan
**POST** `/generate/plan`

Generate a complete execution plan with schedule, costs, and risks.

```bash
curl -X POST http://localhost:8000/generate/plan \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": "WH-2025-01",
    "location": "Seattle, WA",
    "notes": "Prioritize concrete curing"
  }'
```

**Response:**
```json
{
  "status": "success",
  "plan": {
    "project_id": "WH-2025-01",
    "tasks": [
      {
        "id": "T-001",
        "description": "Site Clearing",
        "phase": "Site Preparation",
        "duration_days": 5,
        "labor_cost": 2500,
        "material_cost": 1200,
        "total_cost": 3700,
        "dependencies": []
      }
    ],
    "risks": [
      {
        "risk_type": "Weather",
        "probability": "High",
        "mitigation_strategy": "Schedule site prep in dry season"
      }
    ],
    "total_estimated_cost": 125000,
    "total_duration_days": 120,
    "critical_path": ["T-001", "T-002", "T-005"]
  }
}
```

### 3. Health Check
**GET** `/health`

```bash
curl http://localhost:8000/health
```

## 🔌 Connecting to OpenAI GPT

### Step 1: Public URL
Expose your backend using ngrok:
```bash
ngrok http 8000
# Copy the HTTPS URL
```

### Step 2: Create Custom GPT
1. Go to [ChatGPT - Create GPT](https://chatgpt.com/create)
2. Name: "Construction Planner"
3. Description: "Expert construction project planner with AI-powered scheduling"
4. Instructions: See `GPT_INSTRUCTIONS.md` in this repo

### Step 3: Add Action
1. Click "Create new action"
2. Choose "Import from URL"
3. Paste: `https://YOUR_NGROK_URL/openapi.json`
4. Authenticate: Select "None"

Now your GPT can:
- Upload PDFs: `Upload this construction spec and analyze it`
- Generate plans: `Create an execution plan for the Seattle warehouse`
- Analyze risks: `What are the major risks and how long will this project take?`

## 📊 Features

### Intelligent Scheduling
- **CPM Analysis**: Computes critical path, slack, and total duration
- **Dependency Inference**: Automatically detects task sequences
- **Duration Estimation**: Calculates based on quantities and productivity rates

### Cost Management
- **Material Estimation**: Extracts quantities from specs
- **Unit Rate Library**: Configurable labor and material rates
- **Cost Breakdown**: Detailed labor vs. material costs per task

### Risk Analysis
- **Location-Based Risks**: Identifies weather, permitting, supply chain issues
- **Probability Assessment**: High/Medium/Low risk quantification
- **Mitigation Strategies**: AI-generated mitigation plans

### Document Intelligence
- **PDF Parsing**: Extracts text and tables from construction specs
- **OCR Support**: Reads handwritten notes and scanned documents
- **GraphRAG**: Connects tasks, materials, and locations for context

### Memory & Context
- **Layered Memory**: Recent buffer + summarized history + vector retrieval
- **Semantic Search**: Finds relevant docs based on natural language queries
- **Session Persistence**: Remembers project context across multiple requests

## 🛠️ Configuration

### Environment Variables
Create `.env`:
```text
OPENAI_API_KEY=sk-your-api-key
LLM_PROVIDER=openai
OPENAI_MODEL=gpt-4o
LOG_LEVEL=INFO
API_PORT=8000
FRONTEND_PORT=8501
```

### Customization

**Add More Time Zones** (if extending to global projects):
Edit `backend/src/config.py`

**Adjust Cost Rates**:
Edit `backend/src/workflows/estimation.py` → `PRODUCTIVITY_RATES`

**Modify Risk Factors**:
Edit `backend/src/agent/risk_agent.py` → Risk prompt template

## 📦 Deployment

### To AWS/Google Cloud/Azure:
```bash
# Build image
docker build -t construction-ai:latest .

# Tag for registry
docker tag construction-ai:latest myregistry/construction-ai:latest

# Push
docker push myregistry/construction-ai:latest

# Deploy via your cloud provider's container service
```

### Using Railway / Render:
1. Connect GitHub repo
2. Set `OPENAI_API_KEY` in environment variables
3. Deploy

## 🧪 Testing

```bash
# Run unit tests
pytest backend/tests/

# Generate synthetic PDF for testing
python scripts/generate_synthetic_pdf.py

# Test API endpoints
python scripts/test_api.py
```

## 📚 Documentation

- [SETUP.md](SETUP.md) - Detailed setup instructions
- [openapi.json](openapi.json) - OpenAPI specification for GPT integration
- [GPT_INSTRUCTIONS.md](GPT_INSTRUCTIONS.md) - Instructions for custom GPT

## 🔐 Security

- Prompt injection detection (Rebuff-style checks)
- JSON schema validation (Guardrails)
- Rate limiting ready
- API key rotation support

## 📈 Roadmap

- [ ] Multi-project dashboard
- [ ] Team collaboration features
- [ ] Real-time progress tracking
- [ ] Integration with project management tools (Monday.com, Asana)
- [ ] Advanced ML-based risk prediction
- [ ] Mobile app (React Native)

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repo
2. Create a feature branch
3. Submit a pull request

## 📄 License

MIT License - feel free to use commercially

## 💬 Support

For issues or questions:
- Open a GitHub issue
- Check [SETUP.md](SETUP.md) for troubleshooting
- Email: support@example.com

---

**Built with ❤️ using FastAPI, Streamlit, and OpenAI**