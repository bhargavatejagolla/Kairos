from fastapi import Query
from pydantic import BaseModel

class PaginationParams(BaseModel):
    page: int = Query(1, ge=1, description="Page number")
    page_size: int = Query(50, ge=1, le=100, description="Items per page")
