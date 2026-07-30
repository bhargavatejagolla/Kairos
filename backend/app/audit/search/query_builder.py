from typing import Any
from uuid import UUID

from sqlalchemy import and_, select
from sqlalchemy.orm import selectinload

from app.audit.enums.action import AuditAction
from app.audit.enums.severity import AuditSeverity
from app.audit.models.actor import AuditActor
from app.audit.models.audit_log import AuditLog
from app.audit.models.target import AuditTarget


class AuditQueryBuilder:
    """
    Dynamically constructs SQLAlchemy queries based on complex search filters.
    """
    def __init__(self):
        self.base_stmt = select(AuditLog).options(
            selectinload(AuditLog.actor),
            selectinload(AuditLog.targets),
            selectinload(AuditLog.changes),
            selectinload(AuditLog.metadata_info)
        )

    def build(self, filters: dict[str, Any]):
        stmt = self.base_stmt
        conditions = []

        if filters.get("organization_id"):
            conditions.append(AuditLog.organization_id == UUID(filters["organization_id"]))
            
        if filters.get("project_id"):
            conditions.append(AuditLog.project_id == UUID(filters["project_id"]))
            
        if filters.get("start_date"):
            conditions.append(AuditLog.created_at >= filters["start_date"])
            
        if filters.get("end_date"):
            conditions.append(AuditLog.created_at <= filters["end_date"])
            
        if filters.get("severity"):
            # Could be a single severity or list
            if isinstance(filters["severity"], list):
                conditions.append(AuditLog.severity.in_([AuditSeverity(s) for s in filters["severity"]]))
            else:
                conditions.append(AuditLog.severity == AuditSeverity(filters["severity"]))
                
        if filters.get("action"):
            if isinstance(filters["action"], list):
                conditions.append(AuditLog.action.in_([AuditAction(a) for a in filters["action"]]))
            else:
                conditions.append(AuditLog.action == AuditAction(filters["action"]))
                
        if filters.get("event_type"):
            conditions.append(AuditLog.event_type.ilike(f"%{filters['event_type']}%"))

        # Actor filters require joining AuditActor
        if filters.get("actor_id"):
            stmt = stmt.join(AuditActor, AuditLog.id == AuditActor.audit_log_id)
            conditions.append(AuditActor.actor_id == filters["actor_id"])
            
        # Target filters require joining AuditTarget
        if filters.get("resource_id"):
            stmt = stmt.join(AuditTarget, AuditLog.id == AuditTarget.audit_log_id)
            conditions.append(AuditTarget.resource_id == filters["resource_id"])

        if conditions:
            stmt = stmt.where(and_(*conditions))
            
        return stmt
