from uuid6 import uuid7

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request


class RequestIDMiddleware(BaseHTTPMiddleware):
    """
    Adds a unique request ID to every request.
    """

    async def dispatch(self, request: Request, call_next):

        request_id = str(uuid7())

        request.state.request_id = request_id

        response = await call_next(request)

        response.headers["X-Request-ID"] = request_id

        return response
