from dataclasses import dataclass

from app.db.models.environment import Environment
from app.db.models.organization import Organization
from app.db.models.project import Project
from app.db.models.service import Service
from app.db.models.user import User


@dataclass
class AlertContext:
    """
    Context passed into the AlertWorkflow containing authenticated state, tenant hierarchy, and current policies.
    """
    organization: Organization
    project: Project
    environment: Environment
    service: Service
    actor: User
    
    # Active policies resolved during request lifecycle
    active_policies: list[str] = None
    active_silences: list[str] = None
    
    def __post_init__(self):
        if self.active_policies is None:
            self.active_policies = []
        if self.active_silences is None:
            self.active_silences = []
