from app.db.models.refresh_token import RefreshToken
from app.db.models.user import User

Session = RefreshToken

__all__ = ["RefreshToken", "Session", "User"]
