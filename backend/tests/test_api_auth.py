from collections.abc import AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import StaticPool

from app.api.deps.database import get_db
from app.db.base import Base
from app.dependencies import auth as dep_auth
from app.main import app

engine = create_async_engine(
    "sqlite+aiosqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
    echo=False,
)
TestingSessionLocal = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
    async with TestingSessionLocal() as session:
        yield session


@pytest.fixture(autouse=True)
async def setup_db() -> AsyncGenerator[None, None]:
    app.dependency_overrides[get_db] = override_get_db
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    app.dependency_overrides.clear()
    await engine.dispose()


@pytest.mark.anyio
async def test_auth_api_flow() -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # 1. Register User via /api/v1/users
        user_payload = {
            "email": "auth_user@example.com",
            "username": "authuser",
            "full_name": "Auth User",
            "password": "supersecretpassword",
        }
        res_reg = await client.post("/api/v1/users", json=user_payload)
        assert res_reg.status_code == 201
        user_id = res_reg.json()["id"]

        # 2. Login successfully -> 200 with tokens
        login_payload = {
            "email": "auth_user@example.com",
            "password": "supersecretpassword",
        }
        res_login = await client.post("/api/v1/auth/login", json=login_payload)
        assert res_login.status_code == 200
        token_data = res_login.json()
        assert "access_token" in token_data
        assert "refresh_token" in token_data
        assert token_data["token_type"] == "bearer"
        access_token = token_data["access_token"]
        refresh_token = token_data["refresh_token"]

        # 3. Login with invalid password -> 401
        res_bad_pw = await client.post(
            "/api/v1/auth/login",
            json={"email": "auth_user@example.com", "password": "wrongpassword"},
        )
        assert res_bad_pw.status_code == 401
        assert "HTTP_401" in res_bad_pw.json()["error"]["code"]

        # 4. Login with non-existent email -> 401
        res_no_user = await client.post(
            "/api/v1/auth/login",
            json={
                "email": "nonexistent@example.com",
                "password": "supersecretpassword",
            },
        )
        assert res_no_user.status_code == 401

        # 5. Access protected /api/v1/auth/me without token -> 401
        res_me_no_token = await client.get("/api/v1/auth/me")
        assert res_me_no_token.status_code == 401

        # 6. Access /api/v1/auth/me with valid token -> 200
        headers = {"Authorization": f"Bearer {access_token}"}
        res_me = await client.get("/api/v1/auth/me", headers=headers)
        assert res_me.status_code == 200
        assert res_me.json()["user"]["email"] == "auth_user@example.com"
        assert res_me.json()["user"]["id"] == user_id

        # 7. Refresh tokens successfully -> 200
        res_refresh = await client.post(
            "/api/v1/auth/refresh", json={"refresh_token": refresh_token}
        )
        assert res_refresh.status_code == 200
        new_token_data = res_refresh.json()
        assert "access_token" in new_token_data
        assert "refresh_token" in new_token_data

        # 8. Refresh with invalid token -> 401
        res_bad_refresh = await client.post(
            "/api/v1/auth/refresh", json={"refresh_token": "not.a.valid.token"}
        )
        assert res_bad_refresh.status_code == 401

        # 9. Test inactive user -> 401 on login & me
        await client.patch(f"/api/v1/users/{user_id}", json={"is_active": False})
        res_login_inactive = await client.post("/api/v1/auth/login", json=login_payload)
        assert res_login_inactive.status_code == 401
        assert "inactive" in res_login_inactive.json()["error"]["message"].lower()

        res_me_inactive = await client.get("/api/v1/auth/me", headers=headers)
        assert res_me_inactive.status_code == 401

        # Verify dependency export exists
        assert dep_auth.get_current_user is not None
        assert dep_auth.get_current_active_user is not None
        assert dep_auth.CurrentUserDep is not None
        assert dep_auth.ActiveUserDep is not None

        # 10. Access /api/v1/auth/me with token missing 'sub' -> 401
        from app.core.jwt import jwt, settings

        token_no_sub = jwt.encode(
            {"type": "access"},
            settings.jwt_secret_key,
            algorithm=settings.jwt_algorithm,
        )
        res_no_sub = await client.get(
            "/api/v1/auth/me", headers={"Authorization": f"Bearer {token_no_sub}"}
        )
        assert res_no_sub.status_code == 401

        # 11. Access /api/v1/auth/me with non-UUID 'sub' -> 401
        from app.core.jwt import create_access_token

        token_bad_uuid = create_access_token(subject="not-a-uuid")
        res_bad_uuid = await client.get(
            "/api/v1/auth/me", headers={"Authorization": f"Bearer {token_bad_uuid}"}
        )
        assert res_bad_uuid.status_code == 401

        # 12. Access /api/v1/auth/me with token for deleted user -> 401
        from uuid import uuid4

        token_deleted = create_access_token(subject=uuid4())
        res_deleted = await client.get(
            "/api/v1/auth/me", headers={"Authorization": f"Bearer {token_deleted}"}
        )
        assert res_deleted.status_code == 401

        # Assert new dependencies are exported
        assert dep_auth.VerifiedUserDep is not None
        assert dep_auth.get_current_verified_user is not None
        assert dep_auth.require_auth is not None

        # 13. Test Logout endpoint
        await client.patch(f"/api/v1/users/{user_id}", json={"is_active": True})
        res_login_fresh = await client.post("/api/v1/auth/login", json=login_payload)
        assert res_login_fresh.status_code == 200
        fresh_refresh = res_login_fresh.json()["refresh_token"]

        res_logout = await client.post(
            "/api/v1/auth/logout", json={"refresh_token": fresh_refresh}
        )
        assert res_logout.status_code == 200
        assert res_logout.json()["message"] == "Logged out successfully"

        # Attempting refresh after logout should fail with 401
        res_ref_after_logout = await client.post(
            "/api/v1/auth/refresh", json={"refresh_token": fresh_refresh}
        )
        assert res_ref_after_logout.status_code == 401

        # 14. Test Change Password endpoint
        res_login_for_cp = await client.post("/api/v1/auth/login", json=login_payload)
        assert res_login_for_cp.status_code == 200
        cp_access = res_login_for_cp.json()["access_token"]
        cp_refresh = res_login_for_cp.json()["refresh_token"]

        cp_payload = {
            "current_password": "supersecretpassword",
            "new_password": "newsupersecretpassword",
        }
        res_cp = await client.post(
            "/api/v1/auth/change-password",
            json=cp_payload,
            headers={"Authorization": f"Bearer {cp_access}"},
        )
        assert res_cp.status_code == 200
        assert res_cp.json()["message"] == "Password changed successfully"

        # After password change, existing refresh tokens should be revoked!
        res_ref_after_cp = await client.post(
            "/api/v1/auth/refresh", json={"refresh_token": cp_refresh}
        )
        assert res_ref_after_cp.status_code == 401

        # Login with old password fails, new password succeeds
        res_old_pw = await client.post("/api/v1/auth/login", json=login_payload)
        assert res_old_pw.status_code == 401

        res_new_pw = await client.post(
            "/api/v1/auth/login",
            json={
                "email": "auth_user@example.com",
                "password": "newsupersecretpassword",
            },
        )
        assert res_new_pw.status_code == 200

        # 15. Test Logout All Devices endpoint
        new_access = res_new_pw.json()["access_token"]
        new_refresh = res_new_pw.json()["refresh_token"]

        res_logout_all = await client.post(
            "/api/v1/auth/logout-all",
            headers={"Authorization": f"Bearer {new_access}"},
        )
        assert res_logout_all.status_code == 200
        assert "devices successfully" in res_logout_all.json()["message"]

        # The refresh token from that login should now be revoked
        res_ref_after_logout_all = await client.post(
            "/api/v1/auth/refresh", json={"refresh_token": new_refresh}
        )
        assert res_ref_after_logout_all.status_code == 401
