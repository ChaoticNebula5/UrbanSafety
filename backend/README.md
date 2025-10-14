# Urban Safety Intelligence Platform

Agentic urban safety platform for Patiala with AI classification, geospatial analytics, and automation.

## Quick Start

```bash
# Setup
pip install -r requirements.txt
# Update .env with your PostgreSQL password

# Run
python main.py
# Visit: http://localhost:8000/docs
```

## API Endpoints

- `POST /api/incidents` - Submit incident (auto-classified by AI)
- `GET /api/incidents` - List all incidents
- `GET /api/incidents/{id}` - Get incident details
- `GET /api/analytics/clusters` - Get unsafe zone clusters

## Stack

FastAPI + PostgreSQL/PostGIS + Ollama (Llama 3.2) + GeoPandas
