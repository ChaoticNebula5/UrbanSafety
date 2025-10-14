from .incidents import router as incidents_router
from .analytics import router as analytics_router

__all__ = ["incidents_router", "analytics_router"]
