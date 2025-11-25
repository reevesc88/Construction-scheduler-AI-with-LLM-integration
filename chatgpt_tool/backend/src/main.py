from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import routers
from src.server.routers import health, ingest, generate

# Initialize FastAPI app
app = FastAPI(
    title="Construction AI Planner",
    description="AI-powered construction project planning system",
    version="1.0.0",
    docs_url="/docs",
    openapi_url="/openapi.json"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, tags=["System"])
app.include_router(ingest.router, prefix="/ingest", tags=["Ingestion"])
app.include_router(generate.router, prefix="/generate", tags=["Generation"])

@app.get("/")
async def root():
    """Root endpoint with API info"""
    return {
        "name": "Construction AI Planner",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("API_PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)