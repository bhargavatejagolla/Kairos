from dataclasses import dataclass

from app.core.config import settings


@dataclass(slots=True)
class ApplicationContainer:
    """
    Central application container.

    Every long-lived shared dependency
    will live here.
    """

    settings = settings


container = ApplicationContainer()
