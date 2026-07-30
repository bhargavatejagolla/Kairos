from .alert_rules import router as alert_rules_router
from .alerts import router as alerts_router
from .attachments import router as attachments_router
from .auth import router as auth_router
from .background import router as background_router
from .comments import router as comments_router
from .incidents import router as incidents_router
from .maintenance import router as maintenance_router
from .notifications import router as notifications_router
from .organizations import router as organizations_router
from .permissions import router as permissions_router
from .ping import router as ping_router
from .policies import router as policies_router
from .projects import router as projects_router
from .roles import router as roles_router
from .services import router as services_router
from .signals import router as signals_router
from .silences import router as silences_router
from .statistics import router as statistics_router
from .timelines import router as timelines_router
from .users import router as users_router

routers = [
    ping_router,
    auth_router,
    users_router,
    roles_router,
    permissions_router,
    organizations_router,
    projects_router,
    services_router,
    incidents_router,
    timelines_router,
    statistics_router,
    comments_router,
    attachments_router,
    signals_router,
    alerts_router,
    alert_rules_router,
    policies_router,
    silences_router,
    maintenance_router,
    background_router,
    notifications_router,
]
