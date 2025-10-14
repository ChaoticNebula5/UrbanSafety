from sqlalchemy import create_engine, Column, Integer, String, Text, Float, DateTime, Enum, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from geoalchemy2 import Geometry
from datetime import datetime
from typing import List, Optional
import enum

from config import settings


Base = declarative_base()


class IncidentCategoryDB(str, enum.Enum):
    """Database enum matching Pydantic model"""
    THEFT = "theft"
    ASSAULT = "assault"
    VANDALISM = "vandalism"
    TRAFFIC = "traffic"
    SUSPICIOUS = "suspicious_activity"
    OTHER = "other"


class IncidentSeverityDB(str, enum.Enum):
    """Database enum for severity"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class UserDB(Base):
    """User model with emergency contacts"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    phone = Column(String(20), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    email = Column(String(100), nullable=True)
    emergency_contacts = Column(JSON, default=list)  
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class IncidentDB(Base):
    """
    SQLAlchemy ORM model for incidents table.
    
    Key features:
    - Uses GeoAlchemy2's Geometry type for PostGIS POINT storage
    - Timestamps with automatic updates
    - AI-generated fields (category, severity, summary)
    """
    
    __tablename__ = "incidents"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    
    location = Column(Geometry('POINT', srid=4326), nullable=False)
    
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    
    category = Column(Enum(IncidentCategoryDB), nullable=True)
    severity = Column(Enum(IncidentSeverityDB), nullable=True)
    ai_summary = Column(Text, nullable=True)
    
    reporter_name = Column(String(100), nullable=False)
    reporter_phone = Column(String(20), nullable=False)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class DatabaseService:
    
    def __init__(self):
        """
        Initialize database engine and session factory.
        """
        self.engine = create_engine(
            settings.DATABASE_URL,
            echo=settings.DEBUG,  
            pool_pre_ping=True,   
        )
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
    
    def init_db(self):
        """
        Create all tables and enable PostGIS extension.
        
        This should be called once on app startup.
        """
        with self.engine.connect() as conn:
            try:
                conn.execute("CREATE EXTENSION IF NOT EXISTS postgis;")
                conn.commit()
                print("PostGIS extension enabled")
            except Exception as e:
                print(f"PostGIS extension may already exist or lack permissions: {e}")
        
        # Create all tables
        Base.metadata.create_all(bind=self.engine)
        print("Database tables created")
    
    def get_session(self) -> Session:
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()
    
    def create_incident(self, db: Session, incident_data: dict) -> IncidentDB:
        """
        Create a new incident in the database.
        
        Args:
            db: SQLAlchemy session
            incident_data: Dict with incident fields (from Pydantic model)
        
        Returns:
            Created IncidentDB object
        """
        from geoalchemy2.elements import WKTElement
        
        point = WKTElement(
            f"POINT({incident_data['longitude']} {incident_data['latitude']})",
            srid=4326
        )
        
        incident = IncidentDB(
            title=incident_data['title'],
            description=incident_data['description'],
            latitude=incident_data['latitude'],
            longitude=incident_data['longitude'],
            location=point,
            reporter_name=incident_data['reporter_name'],
            reporter_phone=incident_data['reporter_phone'],
        )
        
        db.add(incident)
        db.commit()
        db.refresh(incident)
        return incident
    
    def get_incident_by_id(self, db: Session, incident_id: int) -> Optional[IncidentDB]:
        return db.query(IncidentDB).filter(IncidentDB.id == incident_id).first()
    
    def get_incidents(
        self, 
        db: Session, 
        skip: int = 0, 
        limit: int = 20,
        category: Optional[str] = None
    ) -> List[IncidentDB]:
        query = db.query(IncidentDB)
        
        if category:
            query = query.filter(IncidentDB.category == category)
        
        return query.order_by(IncidentDB.created_at.desc()).offset(skip).limit(limit).all()
    
    def count_incidents(self, db: Session, category: Optional[str] = None) -> int:
        """Count total incidents (for pagination)"""
        query = db.query(IncidentDB)
        if category:
            query = query.filter(IncidentDB.category == category)
        return query.count()
    
    def update_incident_ai_fields(
        self,
        db: Session,
        incident_id: int,
        category: str,
        severity: str,
        ai_summary: str
    ) -> Optional[IncidentDB]:
        incident = self.get_incident_by_id(db, incident_id)
        if incident:
            incident.category = category
            incident.severity = severity
            incident.ai_summary = ai_summary
            incident.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(incident)
        return incident
    
    
    async def create_user(
        self,
        name: str,
        phone: str,
        password_hash: str,
        email: Optional[str],
        emergency_contacts: List[dict]
    ) -> UserDB:
        db = self.SessionLocal()
        try:
            user = UserDB(
                name=name,
                phone=phone,
                password_hash=password_hash,
                email=email,
                emergency_contacts=emergency_contacts
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            return user
        finally:
            db.close()
    
    async def get_user_by_phone(self, phone: str) -> Optional[UserDB]:
        db = self.SessionLocal()
        try:
            return db.query(UserDB).filter(UserDB.phone == phone).first()
        finally:
            db.close()
    
    async def get_user_by_id(self, user_id: int) -> Optional[UserDB]:
        db = self.SessionLocal()
        try:
            return db.query(UserDB).filter(UserDB.id == user_id).first()
        finally:
            db.close()


db_service = DatabaseService()
