from app.api.v1.auth import router as auth_router
from app.api.v1.organizations import router as organizations_router
from app.api.v1.permissions import router as permissions_router
from app.api.v1.ping import router as ping_router
from app.api.v1.roles import router as roles_router
from app.api.v1.users import router as users_router

routers = [
    ping_router,
    auth_router,
    users_router,
    roles_router,
    permissions_router,
    organizations_router,
]
