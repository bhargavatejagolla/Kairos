
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps.auth import get_current_user
from app.api.deps.database import get_db
from app.audit.analytics.metrics import AuditAnalyticsEngine
from app.db.models.user import User

router = APIRouter()

@router.get("/dashboard")
async def get_audit_dashboard_metrics(
    days: int = 7,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Returns summary metrics for the Audit Dashboard.
    """
    analytics = AuditAnalyticsEngine(db)
    org_id = current_user.organization_id
    
    summary = await analytics.get_activity_summary(org_id, days)
    top_users = await analytics.get_most_active_users(org_id, days)
    
    return {
        "summary": summary,
        "most_active_users": top_users
    }
