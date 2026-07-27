from .constants import (
    QUEUE_DEFAULT, QUEUE_AI, QUEUE_NOTIFICATIONS, 
    QUEUE_KNOWLEDGE, QUEUE_REPORTS, QUEUE_DEPLOYMENTS, 
    QUEUE_MAINTENANCE
)

class TaskRouter:
    def route_task(self, name, args, kwargs, options, task=None, **kw):
        if name.startswith('ai.'):
            return {'queue': QUEUE_AI}
        elif name.startswith('notifications.'):
            return {'queue': QUEUE_NOTIFICATIONS}
        elif name.startswith('knowledge.'):
            return {'queue': QUEUE_KNOWLEDGE}
        elif name.startswith('reports.'):
            return {'queue': QUEUE_REPORTS}
        elif name.startswith('deployments.'):
            return {'queue': QUEUE_DEPLOYMENTS}
        elif name.startswith('maintenance.'):
            return {'queue': QUEUE_MAINTENANCE}
        
        return {'queue': QUEUE_DEFAULT}

CELERY_ROUTES = (TaskRouter(), )
