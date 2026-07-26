from typing import Annotated, Optional
from datetime import datetime
from uuid import UUID
from fastapi import Query, Depends

class IncidentSearchParams:
    def __init__(
        self,
        status: Optional[str] = Query(None, description="Filter by status (e.g., OPEN, RESOLVED)"),
        severity: Optional[str] = Query(None, description="Filter by severity (e.g., SEV1)"),
        priority: Optional[str] = Query(None, description="Filter by priority (e.g., P1)"),
        assignee: Optional[UUID] = Query(None, description="Filter by assignee user ID"),
        service: Optional[UUID] = Query(None, description="Filter by service ID"),
        created_after: Optional[datetime] = Query(None, description="Filter incidents created after this date"),
        created_before: Optional[datetime] = Query(None, description="Filter incidents created before this date"),
        sort: Optional[str] = Query("-created_at", description="Sort field (prefix with - for descending)"),
    ):
        self.status = status
        self.severity = severity
        self.priority = priority
        self.assignee = assignee
        self.service = service
        self.created_after = created_after
        self.created_before = created_before
        self.sort = sort

IncidentSearchDep = Annotated[IncidentSearchParams, Depends()]
