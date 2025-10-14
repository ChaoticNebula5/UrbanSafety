from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from config import settings
from services import db_service
from routes import incidents_router, analytics_router
from routes.users import router as users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting Urban Safety Intelligence...")
    
    db_service.init_db()
    
    print(f"{settings.APP_NAME} is ready!")
    print(f"Database: {settings.DATABASE_URL.split('@')[-1]}")  # Hide password
    print(f"AI Provider: {settings.AI_PROVIDER.upper()} ({settings.OLLAMA_MODEL if settings.AI_PROVIDER == 'ollama' else 'GPT-4'})")
    #print(f"n8n Automation: {'Enabled' if settings.N8N_ENABLED else 'Disabled (Mock Mode)'}")
    
    yield
    
    print("Shutting down gracefully...")


app = FastAPI(
    title=settings.APP_NAME,
    description="Agentic urban safety platform with AI classification, GIS analytics, and automation",
    version="1.0.0",
    lifespan=lifespan,
    debug=settings.DEBUG
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Health"])
async def root():
    """
    Root endpoint - health check and API info.
    """
    return {
        "status": "online",
        "app": settings.APP_NAME,
        "message": "Urban Safety Intelligence Platform API",
        "docs": "/docs",
        "version": "1.0.0"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """
    Detailed health check for monitoring.
    """
    return {
        "status": "healthy",
        "database": "connected",
        "postgis": settings.POSTGIS_ENABLED,
        "ai_agent": bool(settings.OPENAI_API_KEY)
    }


app.include_router(users_router)  # User authentication
app.include_router(incidents_router, prefix="/api", tags=["Incidents"])
app.include_router(analytics_router, prefix="/api", tags=["Analytics"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
