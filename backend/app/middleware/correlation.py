import contextvars
import uuid

import structlog
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

# Global contextvar to hold the correlation ID for the current request
correlation_id_var: contextvars.ContextVar[str] = contextvars.ContextVar('correlation_id', default=None)

class CorrelationIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        # Check if the client passed a correlation ID
        correlation_id = request.headers.get("X-Correlation-ID")
        if not correlation_id:
            correlation_id = str(uuid.uuid4())
            
        # Set it in the contextvar for this request
        correlation_id_var.set(correlation_id)
        
        # Bind it to structlog so every log in this request includes the correlation_id
        structlog.contextvars.bind_contextvars(correlation_id=correlation_id)
        
        response = await call_next(request)
        
        # Include it in the response
        response.headers["X-Correlation-ID"] = correlation_id
        
        # Clear structlog contextvars for the next request
        structlog.contextvars.clear_contextvars()
        
        return response
