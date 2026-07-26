from enum import StrEnum


class Permission(StrEnum):
    # Users
    USERS_READ = "users:read"
    USERS_CREATE = "users:create"
    USERS_UPDATE = "users:update"
    USERS_DELETE = "users:delete"

    # Organizations
    ORGANIZATIONS_READ = "organizations:read"
    ORGANIZATIONS_VIEW = "organizations:view"
    ORGANIZATIONS_CREATE = "organizations:create"
    ORGANIZATIONS_UPDATE = "organizations:update"
    ORGANIZATIONS_DELETE = "organizations:delete"

    # Member permissions
    MEMBERS_VIEW = "members:view"
    MEMBERS_ADD = "members:add"
    MEMBERS_REMOVE = "members:remove"
    MEMBERS_ROLE_UPDATE = "members:role:update"

    # Project permissions
    PROJECTS_CREATE = "projects:create"
    PROJECTS_VIEW = "projects:view"
    PROJECTS_UPDATE = "projects:update"
    PROJECTS_ARCHIVE = "projects:archive"
    PROJECTS_RESTORE = "projects:restore"
    PROJECTS_DELETE = "projects:delete"
    PROJECTS_SETTINGS_UPDATE = "projects:settings:update"

    # Incidents
    INCIDENTS_VIEW = "incidents:view"
    INCIDENTS_CREATE = "incidents:create"
    INCIDENTS_UPDATE = "incidents:update"
    INCIDENTS_ASSIGN = "incidents:assign"
    INCIDENTS_RESOLVE = "incidents:resolve"
    INCIDENTS_CLOSE = "incidents:close"
    INCIDENTS_DELETE = "incidents:delete"

    # Alerts
    ALERTS_READ = "alerts:read"
    ALERTS_CREATE = "alerts:create"
    ALERTS_UPDATE = "alerts:update"
    ALERTS_DELETE = "alerts:delete"
    ALERTS_ACKNOWLEDGE = "alerts:acknowledge"

    # AI
    AI_ANALYZE = "ai:analyze"

    # Audit
    AUDIT_READ = "audit:read"
