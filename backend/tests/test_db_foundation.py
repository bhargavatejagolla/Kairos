from app.core.config import settings
from app.db.session import AsyncSessionLocal, engine


def test_database_url_configured():
    assert "postgresql+asyncpg://" in settings.database_url
    assert settings.database_name in ("kairos", "kairos_db")
    assert engine is not None
    assert AsyncSessionLocal is not None
