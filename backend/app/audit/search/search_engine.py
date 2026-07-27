from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any, Tuple, List

from app.audit.search.query_builder import AuditQueryBuilder
from app.audit.models.audit_log import AuditLog

class AuditSearchEngine:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.builder = AuditQueryBuilder()

    async def search(self, filters: Dict[str, Any], page: int = 1, page_size: int = 50) -> Tuple[List[AuditLog], int]:
        """
        Executes a paginated search against the audit logs.
        """
        stmt = self.builder.build(filters)
        
        # In a real enterprise system, you would do a separate count query or use elasticsearch
        # For simplicity, we just execute the query with offset/limit
        
        # Order by newest first
        stmt = stmt.order_by(AuditLog.created_at.desc())
        
        # Apply pagination
        offset = (page - 1) * page_size
        stmt = stmt.offset(offset).limit(page_size)
        
        result = await self.session.execute(stmt)
        items = list(result.scalars().all())
        
        # Return total_count as -1 or implement a true count query
        # Returning len(items) is just for the current page
        return items, -1 
