from sqlalchemy.ext.asyncio import AsyncSession
import structlog
import hashlib
import json
from uuid import UUID
from typing import Optional

from app.audit.repositories.audit_repository import AuditRepository
from app.audit.models import AuditLog, AuditActor, AuditTarget, AuditChange, AuditMetadata
from app.audit.schemas.audit import AuditEventCreate
from app.audit.enums.action import AuditAction

logger = structlog.get_logger(__name__)

class AuditService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = AuditRepository(session)
        # Note: In a real system, we might query the latest log's hash to chain them.
        self._last_known_hash = None

    def _compute_hash(self, log: AuditLog, previous_hash: str) -> str:
        # A simple deterministic representation
        payload = f"{log.id}|{log.correlation_id}|{log.event_type}|{log.action.value}|{log.created_at.isoformat()}|{previous_hash}"
        return hashlib.sha256(payload.encode('utf-8')).hexdigest()

    async def create_audit_record(self, event: AuditEventCreate) -> AuditLog:
        """
        Creates an immutable audit record from a standardized domain event.
        Includes Redaction logic and Hash Chaining.
        """
        # Redaction Layer (Sanitizer logic inline for simplicity)
        safe_metadata = dict(event.metadata)
        if "password" in safe_metadata:
            safe_metadata["password"] = "***REDACTED***"
        if "token" in safe_metadata:
            safe_metadata["token"] = "***REDACTED***"

        # 1. Build Aggregate Root
        log = AuditLog(
            organization_id=event.organization_id,
            project_id=event.project_id,
            environment_id=event.environment_id,
            service_id=event.service_id,
            correlation_id=event.correlation_id,
            request_id=event.request_id,
            event_type=event.event_type,
            action=event.action,
            status=event.status,
            severity=event.severity,
            source=event.source,
            ip_address=event.ip_address,
            user_agent=event.user_agent
        )

        # 2. Build Actor
        log.actor = AuditActor(
            actor_type=event.actor_type,
            actor_id=event.actor_id,
            actor_name=event.actor_name,
            actor_email=event.actor_email
        )

        # 3. Build Targets
        log.targets = [
            AuditTarget(
                resource_type=t.resource_type,
                resource_id=t.resource_id,
                resource_name=t.resource_name
            ) for t in event.targets
        ]

        # 4. Build Changes
        log.changes = [
            AuditChange(
                field_name=c.field_name,
                old_value=c.old_value,
                new_value=c.new_value
            ) for c in event.changes
        ]

        # 5. Build Metadata
        log.metadata_info = AuditMetadata(
            metadata_json=safe_metadata
        )

        # 6. Hash Chaining
        prev_hash = self._last_known_hash or "genesis_hash"
        log.previous_hash = prev_hash
        
        # We must flush to get the ID and created_at if we rely on DB defaults, 
        # but here they are generated in Python (`uuid4` and `datetime.now`) 
        # so we can hash immediately.
        log.record_hash = self._compute_hash(log, prev_hash)
        self._last_known_hash = log.record_hash

        # 7. Persist
        created_log = await self.repository.create(log)
        await self.session.commit()
        
        logger.info("audit_record_created", event_type=log.event_type, action=log.action.value, log_id=str(log.id))
        return created_log
