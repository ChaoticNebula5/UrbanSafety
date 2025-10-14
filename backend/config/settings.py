from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    DATABASE_URL: str = "postgresql://postgres:password@localhost:5432/urban_safety"
    POSTGIS_ENABLED: bool = True
    
    AI_PROVIDER: str = "ollama"  
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3.1:latest" 
    
    
    #N8N_WEBHOOK_URL: str = "http://localhost:5678/webhook/incident-alert"
    #N8N_ENABLED: bool = False  # Set to True when n8n is running
    
    APP_NAME: str = "Urban Safety Intelligence"
    DEBUG: bool = True
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra='ignore'
    )


settings = Settings()
