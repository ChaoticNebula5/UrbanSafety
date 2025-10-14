from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from models import IncidentCreate, IncidentResponse, IncidentListResponse
from services import db_service, ai_classifier
from services.notification_service import notification_service


router = APIRouter()


@router.post("/incidents", response_model=IncidentResponse, status_code=201)
async def create_incident(
    incident: IncidentCreate,
    user_id: Optional[int] = None,  
    db: Session = Depends(db_service.get_session)
):
    incident_db = db_service.create_incident(db, incident.model_dump())
    
    ai_result = ai_classifier.classify(
        title=incident.title,
        description=incident.description
    )
    
    incident_db = db_service.update_incident_ai_fields(
        db=db,
        incident_id=incident_db.id,
        category=ai_result["category"],
        severity=ai_result["severity"],
        ai_summary=ai_result["ai_summary"]
    )
    
    notification_result = None
    if user_id:
        user = await db_service.get_user_by_id(user_id)
        if user and user.emergency_contacts:
            incident_data = {
                "title": incident.title,
                "description": incident.description,
                "latitude": incident.latitude,
                "longitude": incident.longitude,
                "category": ai_result["category"],
                "severity": ai_result["severity"],
                "ai_summary": ai_result["ai_summary"]
            }
            
            notification_result = notification_service.send_emergency_alert(
                incident_data=incident_data,
                emergency_contacts=user.emergency_contacts,
                user_name=user.name
            )
            
            print(f"\n[SUCCESS] Sent {notification_result['notifications_sent']} emergency alerts!")
    
    return incident_db


@router.get("/incidents", response_model=IncidentListResponse)
async def list_incidents(
    page: int = 1,
    page_size: int = 20,
    category: Optional[str] = None,
    db: Session = Depends(db_service.get_session)
):
    skip = (page - 1) * page_size
    incidents = db_service.get_incidents(db, skip=skip, limit=page_size, category=category)
    total = db_service.count_incidents(db, category=category)
    
    return {
        "total": total,
        "incidents": incidents,
        "page": page,
        "page_size": page_size
    }


@router.get("/incidents/{incident_id}", response_model=IncidentResponse)
async def get_incident(
    incident_id: int,
    db: Session = Depends(db_service.get_session)
):
    incident = db_service.get_incident_by_id(db, incident_id)
    
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    
    return incident
