# KAIROS Authentication Architecture & API Reference

## 🎯 Overview

KAIROS employs a modern, production-grade authentication architecture built around **stateless short-lived JWT access tokens** paired with **database-backed refresh token sessions**. This design achieves maximum API scalability while preserving absolute session control, revocation capabilities, and security event detection.

---

## 🔐 Core Architecture

### 1. Token Lifecycle & Rotation
- **Access Tokens**: Short-lived (default 15 minutes), stateless JWTs containing the user's `sub` (ID) and type (`access`). Verified independently by API routers without database queries.
- **Refresh Tokens**: Long-lived (default 7 days), secure JWTs containing a unique token ID (`jti`). Persisted in the database via the `RefreshToken` (`Session`) model.
- **Refresh Token Rotation (RTR)**: Every call to `/api/v1/auth/refresh` revokes the old refresh token and issues a brand new access/refresh pair.
- **Compromised Token Detection**: If an already-revoked refresh token is presented again, KAIROS treats this as a security anomaly (token reuse) and immediately revokes **all** active user sessions across all devices.

### 2. Multi-Device Session Tracking
When a user logs in, KAIROS captures:
- `user_id`: UUID of the authenticated user
- `token_id` (`jti`): Unique JWT identifier
- `user_agent`: Device / browser signature from request headers
- `ip_address`: Client network host address
- `expires_at`: Absolute expiration timestamp
- `revoked`: Boolean session status

---

## 🔄 Complete Authentication Flows

### Login Flow
```text
Client                         FastAPI Router                       AuthService                        PostgreSQL
  │                                  │                                   │                                 │
  │─── POST /api/v1/auth/login ─────▶│                                   │                                 │
  │    (email, password)             │─── login(request, login_in) ─────▶│                                 │
  │                                  │                                   │─── get_by_email(email) ────────▶│
  │                                  │                                   │◀── return User ─────────────────│
  │                                  │                                   │─── verify_password(hash)        │
  │                                  │                                   │─── create_token_pair()          │
  │                                  │                                   │─── create_token(session_record)▶│
  │◀── TokenResponse (tokens) ───────│◀── return TokenResponse ──────────│                                 │
```

### Protected Endpoint Request
```text
Client                         FastAPI Router                      Dependencies                        Service
  │                                  │                                   │                                │
  │─── GET /api/v1/auth/me ─────────▶│                                   │                                │
  │    Header: Bearer <access_token> │─── require ActiveUserDep ────────▶│                                │
  │                                  │                                   │─── decode_token(access_token)  │
  │                                  │                                   │─── get_by_id(sub) ────────────▶│
  │                                  │                                   │◀── return User ────────────────│
  │◀── CurrentUserResponse ──────────│◀── return User ───────────────────│                                │
```

### Refresh Token Rotation Flow
```text
Client                         FastAPI Router                       AuthService                        PostgreSQL
  │                                  │                                   │                                 │
  │─── POST /api/v1/auth/refresh ───▶│                                   │                                 │
  │    (refresh_token)               │─── refresh_tokens(token) ────────▶│                                 │
  │                                  │                                   │─── get_by_jti(jti) ────────────▶│
  │                                  │                                   │◀── return RefreshToken ─────────│
  │                                  │                                   │─── check not revoked / expired  │
  │                                  │                                   │─── revoke_by_jti(old_jti) ─────▶│
  │                                  │                                   │─── create_token(new_session) ──▶│
  │◀── TokenResponse (new pair) ─────│◀── return TokenResponse ──────────│                                 │
```

### Logout & Device Revocation Flow
```text
Client                         FastAPI Router                       AuthService                        PostgreSQL
  │                                  │                                   │                                 │
  │─── POST /api/v1/auth/logout ────▶│                                   │                                 │
  │    (refresh_token)               │─── logout(refresh_token) ────────▶│                                 │
  │                                  │                                   │─── revoke_by_jti(jti) ─────────▶│
  │◀── 200 OK ───────────────────────│◀── return success ────────────────│                                 │
```

---

## 📌 OpenAPI Reference

### `POST /api/v1/auth/login`
Authenticate user credentials and establish a new tracked session.
- **Request Body**: `LoginRequest` (`email`, `password`)
- **Headers**: Optional `User-Agent` captured for session logging.
- **Response**: `200 OK` -> `TokenResponse` (`access_token`, `refresh_token`, `token_type="bearer"`).
- **Errors**: `401 Unauthorized` (invalid credentials or inactive account).

### `POST /api/v1/auth/refresh`
Rotate a valid refresh token for a brand new access and refresh token pair.
- **Request Body**: `RefreshTokenRequest` (`refresh_token`)
- **Response**: `200 OK` -> `TokenResponse`
- **Errors**: `401 Unauthorized` (expired token, revoked token, or reuse anomaly).

### `POST /api/v1/auth/logout`
Revoke the provided refresh token session for the calling device.
- **Request Body**: `LogoutRequest` (`refresh_token`)
- **Response**: `200 OK` -> `{"message": "Logged out successfully"}`

### `POST /api/v1/auth/logout-all`
Revoke all active refresh token sessions for the authenticated user across all browsers and devices.
- **Headers**: `Authorization: Bearer <access_token>`
- **Response**: `200 OK` -> `{"message": "Logged out from <N> devices successfully"}`

### `GET /api/v1/auth/me`
Retrieve the profile of the currently authenticated active user.
- **Headers**: `Authorization: Bearer <access_token>`
- **Response**: `200 OK` -> `CurrentUserResponse`

### `POST /api/v1/auth/change-password`
Verify current password, update password hash, and automatically terminate all existing sessions.
- **Headers**: `Authorization: Bearer <access_token>`
- **Request Body**: `ChangePasswordRequest` (`current_password`, `new_password`)
- **Response**: `200 OK` -> `{"message": "Password changed successfully"}`

---

## 🏗️ Dependency Injection Aliases

To keep FastAPI controllers clean, KAIROS provides typed dependency aliases in `app.api.deps.auth` and `app.dependencies.auth`:

```python
from typing import Annotated
from fastapi import Depends
from app.api.deps.auth import get_current_user, get_current_active_user
from app.db.models.user import User

# Standard type-annotated dependency for any authenticated user
CurrentUserDep = Annotated[User, Depends(get_current_user)]

# Type-annotated dependency ensuring the user is active and not disabled
ActiveUserDep = Annotated[User, Depends(get_current_active_user)]
```

---

## 🚀 Architectural Transition to Phase 6 (RBAC)

In **Phase 6**, authorization will decouple user identities from static role designations. Instead of storing a monolithic `role_id` on the `User` model, KAIROS implements **fine-grained permissions** structured for multi-tenant SaaS organizations via the future `OrganizationMember` association model:

```text
User ◀─── OrganizationMember ───▶ Organization
               │
               ▼
             Role ───▶ Permissions (user:create, project:delete, etc.)
```
