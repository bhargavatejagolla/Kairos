from sqlalchemy import select, and_, or_, cast, String
from sqlalchemy.orm import selectinload
from typing import Dict, Any, Optional
from datetime import datetime
from uuid import UUID

from app.audit.models.audit_log import AuditLog
from app.audit.models.actor import AuditActor
from app.audit.models.target import AuditTarget
from app.audit.enums.action import AuditAction
from app.audit.enums.severity import AuditSeverity

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

    def build(self, filters: Dict[str, Any]):
        stmt = self.base_stmt
        conditions = []

        if "organization_id" in filters and filters["organization_id"]:
            conditions.append(AuditLog.organization_id == UUID(filters["organization_id"]))
            
        if "project_id" in filters and filters["project_id"]:
            conditions.append(AuditLog.project_id == UUID(filters["project_id"]))
            
        if "start_date" in filters and filters["start_date"]:
            conditions.append(AuditLog.created_at >= filters["start_date"])
            
        if "end_date" in filters and filters["end_date"]:
            conditions.append(AuditLog.created_at <= filters["end_date"])
            
        if "severity" in filters and filters["severity"]:
            # Could be a single severity or list
            if isinstance(filters["severity"], list):
                conditions.append(AuditLog.severity.in_([AuditSeverity(s) for s in filters["severity"]]))
            else:
                conditions.append(AuditLog.severity == AuditSeverity(filters["severity"]))
                
        if "action" in filters and filters["action"]:
            if isinstance(filters["action"], list):
                conditions.append(AuditLog.action.in_([AuditAction(a) for a in filters["action"]]))
            else:
                conditions.append(AuditLog.action == AuditAction(filters["action"]))
                
        if "event_type" in filters and filters["event_type"]:
            conditions.append(AuditLog.event_type.ilike(f"%{filters['event_type']}%"))

        # Actor filters require joining AuditActor
        if "actor_id" in filters and filters["actor_id"]:
            stmt = stmt.join(AuditActor, AuditLog.id == AuditActor.audit_log_id)
            conditions.append(AuditActor.actor_id == filters["actor_id"])
            
        # Target filters require joining AuditTarget
        if "resource_id" in filters and filters["resource_id"]:
            stmt = stmt.join(AuditTarget, AuditLog.id == AuditTarget.audit_log_id)
            conditions.append(AuditTarget.resource_id == filters["resource_id"])

        if conditions:
            stmt = stmt.where(and_(*conditions))
            
        return stmt
