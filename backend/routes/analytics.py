"""
Analytics API Routes - GIS Clustering and Spatial Intelligence
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Optional

from services import db_service, geo_service


router = APIRouter()


@router.get("/analytics/clusters")
async def get_incident_clusters(
    eps_km: float = 0.5,
    category: Optional[str] = None,
    db: Session = Depends(db_service.get_session)
):

    incidents = db_service.get_incidents(db, skip=0, limit=1000, category=category)
    
    incident_data = [
        {
            "id": inc.id,
            "latitude": inc.latitude,
            "longitude": inc.longitude,
            "severity": inc.severity.value if inc.severity else "medium",
            "category": inc.category.value if inc.category else "other"
        }
        for inc in incidents
    ]
    
    # Get 
    clusters = geo_service.cluster_incidents(incident_data, eps_km=eps_km)
    
    return {
        "total_incidents": len(incidents),
        "total_clusters": len(clusters),
        "clusters": clusters
    }


@router.get("/analytics/heatmap")
async def get_heatmap_data(
    category: Optional[str] = None,
    db: Session = Depends(db_service.get_session)
):
    """
    Get heatmap data for visualization.
    
    Query params:
    - category: Filter by incident category
    """
    incidents = db_service.get_incidents(db, skip=0, limit=1000, category=category)
    
    incident_data = [
        {
            "latitude": inc.latitude,
            "longitude": inc.longitude,
            "severity": inc.severity.value if inc.severity else "medium",
            "category": inc.category.value if inc.category else "other"
        }
        for inc in incidents
    ]
    
    heatmap = geo_service.generate_heatmap_data(incident_data)
    
    return heatmap


@router.get("/analytics/danger-zones")
async def get_danger_zones(
    threshold: int = 3,
    db: Session = Depends(db_service.get_session)
):
    """
    Identify high-risk danger zones.
    
    Query params:
    - threshold: Minimum incidents to mark as danger zone (default: 3)
    """
    incidents = db_service.get_incidents(db, skip=0, limit=1000)
    
    incident_data = [
        {
            "id": inc.id,
            "latitude": inc.latitude,
            "longitude": inc.longitude,
            "severity": inc.severity.value if inc.severity else "medium",
            "category": inc.category.value if inc.category else "other"
        }
        for inc in incidents
    ]
    
    danger_zones = geo_service.identify_danger_zones(incident_data, threshold=threshold)
    
    return {
        "total_zones": len(danger_zones),
        "zones": danger_zones
    }


@router.get("/analytics/spatial-context")
async def get_spatial_context(lat: float, lng: float):
    """
    Get spatial context for given coordinates.
    Returns nearest police station, hospital, and landmarks.
    """
    context = geo_service.get_spatial_context(lat, lng)
    
    return context
