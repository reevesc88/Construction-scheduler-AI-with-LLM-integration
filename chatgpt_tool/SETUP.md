# 🔧 Detailed Setup Guide

## Prerequisites

- Python 3.11+
- Docker & Docker Compose (optional but recommended)
- OpenAI API Key (get one at [platform.openai.com](https://platform.openai.com))
- Git

## Step-by-Step Installation

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/construction-ai-planner.git
cd construction-ai-planner
```

### 2. Environment Setup

**Copy example environment file:**
```bash
cp .env.example .env
```

**Edit `.env` with your keys:**
```text
OPENAI_API_KEY=sk-proj-xxxxx
LLM_PROVIDER=openai
OPENAI_MODEL=gpt-4o
LOG_LEVEL=INFO
```

### 3. Using Docker (Recommended)

**Build and run:**
```bash
docker-compose up --build
```

This starts:
- Backend API on `http://localhost:8000`
- Frontend on `http://localhost:8501`
- ChromaDB vector store on `http://localhost:8001`

### 4. Local Setup (Without Docker)

**Install system dependencies (macOS):**
```bash
brew install tesseract poppler
```

**Install system dependencies (Ubuntu/Debian):**
```bash
sudo apt-get install tesseract-ocr poppler-utils
```

**Install system dependencies (Windows):**
- Download Tesseract: https://github.com/UB-Mannheim/tesseract/wiki
- Download Poppler: https://github.com/oschwartz10612/poppler-windows/releases/

**Install Python packages:**
```bash
pip install -r requirements.txt
```

**Create necessary directories:**
```bash
mkdir -p backend/chroma_data artifacts
```

**Run backend:**
```bash
cd backend
uvicorn src.main:app --reload --port 8000
```

**Run frontend (in another terminal):**
```bash
cd frontend
streamlit run app.py
```

### 5. Verify Installation

**Check backend health:**
```bash
curl http://localhost:8000/health
# Should return: {"status": "ok"}
```

**Check Swagger UI:**
Open http://localhost:8000/docs in browser

## 🔌 Connecting to Your GPT

### Step 1: Expose Backend
If running locally, use ngrok to create a public URL:

```bash
# Install ngrok
brew install ngrok  # macOS
# or download from https://ngrok.com

# Start tunnel
ngrok http 8000
# Copy the HTTPS URL (e.g., https://abc123.ngrok-free.app)
```

### Step 2: Create Custom GPT
1. Go to https://chatgpt.com/create
2. Fill in these details:
   - **Name**: Construction Planner AI
   - **Description**: Expert AI for construction project planning and analysis
   - **Greeting**: "Upload your construction specs and I'll create a detailed execution plan with scheduling, costs, and risk analysis."

3. Click "Create new action"
4. Paste this schema (replacing YOUR_URL):

```json
{
  "openapi": "3.1.0",
  "info": {
    "title": "Construction AI Planner",
    "version": "1.0.0"
  },
  "servers": [
    {
      "url": "https://YOUR_NGROK_URL"
    }
  ],
  "paths": {
    "/ingest/document": {
      "post": {
        "operationId": "ingest_document",
        "summary": "Upload and analyze construction specification PDF",
        "requestBody": {
          "content": {
            "multipart/form-data": {
              "schema": {
                "type": "object",
                "properties": {
                  "file": {
                    "type": "string",
                    "format": "binary"
                  }
                }
              }
            }
          }
        },
        "responses": {
          "200": {
            "description": "Document ingested successfully"
          }
        }
      }
    },
    "/generate/plan": {
      "post": {
        "operationId": "generate_plan",
        "summary": "Generate complete execution plan with schedule, costs, and risks",
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "properties": {
                  "project_id": {
                    "type": "string",
                    "description": "Unique project identifier"
                  },
                  "location": {
                    "type": "string",
                    "description": "Project location (e.g., 'Seattle, WA')"
                  },
                  "notes": {
                    "type": "string",
                    "description": "Additional constraints or notes"
                  }
                },
                "required": ["project_id"]
              }
            }
          }
        },
        "responses": {
          "200": {
            "description": "Plan generated successfully"
          }
        }
      }
    }
  }
}
```

### Step 3: Test in GPT
In the preview pane, try:
- "Upload a construction specification PDF"
- "Generate an execution plan for a warehouse project in Seattle"
- "What are the major risks and timeline?"

## 🧪 Testing the System

### Generate Sample PDF
```bash
python scripts/generate_synthetic_pdf.py
# Creates synthetic_project_spec.pdf
```

### Test Full Workflow
```bash
# 1. Upload document
curl -F "file=@synthetic_project_spec.pdf" http://localhost:8000/ingest/document

# 2. Generate plan (use returned document_id)
curl -X POST http://localhost:8000/generate/plan \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": "TEST-001",
    "location": "Seattle, WA",
    "notes": "Test run"
  }'
```

## 🐛 Troubleshooting

### "ModuleNotFoundError" when running
**Solution:** Ensure you're in the correct directory and have installed dependencies:
```bash
pip install -r requirements.txt
```

### "OPENAI_API_KEY not found"
**Solution:** Check your `.env` file is created and has the key:
```bash
cat .env | grep OPENAI_API_KEY
```

### ChromaDB connection refused
**Solution:** Start ChromaDB first:
```bash
docker run -p 8001:8000 chromadb/chroma:latest
```

### "Port 8000 already in use"
**Solution:** Change the port:
```bash
uvicorn src.main:app --port 8001
```

### PDF extraction returns empty
**Solution:** Ensure tesseract is installed:
```bash
# macOS
brew install tesseract

# Ubuntu
sudo apt-get install tesseract-ocr

# Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki
```

## 📊 Performance Tuning

### Reduce Latency
- Use `gpt-4o-mini` instead of `gpt-4o` in `.env`
- Increase vector DB cache: Edit `backend/src/config.py`

### Handle Large PDFs
- Chunk size is configurable in `backend/src/tools/pdf_extractor.py`
- Default: 1000 tokens, increase for larger documents

### Scale to Multiple Users
- Deploy with Gunicorn:
```bash
gunicorn -w 4 -b 0.0.0.0:8000 "backend.src.main:app"
```

## 🚀 Production Deployment

### AWS Lambda
```bash
pip install zappa
zappa init
zappa deploy production
```

### Docker to ECR
```bash
aws ecr create-repository --repository-name construction-ai
docker build -t construction-ai .
docker tag construction-ai:latest YOUR_ECR_URL/construction-ai:latest
docker push YOUR_ECR_URL/construction-ai:latest
```

### Environment Variables for Production
```bash
OPENAI_API_KEY=sk-proj-xxxxx
LLM_PROVIDER=openai
LOG_LEVEL=ERROR
CORS_ORIGINS=["https://yourdomain.com"]
```

---

Need help? Open an issue on GitHub or email support@example.com