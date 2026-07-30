from kombu import Exchange, Queue

from .constants import (
    QUEUE_AI,
    QUEUE_DEFAULT,
    QUEUE_DEPLOYMENTS,
    QUEUE_KNOWLEDGE,
    QUEUE_MAINTENANCE,
    QUEUE_NOTIFICATIONS,
    QUEUE_REPORTS,
)

task_exchange = Exchange('kairos_tasks', type='direct')

CELERY_QUEUES = (
    Queue(QUEUE_DEFAULT, task_exchange, routing_key=QUEUE_DEFAULT),
    Queue(QUEUE_AI, task_exchange, routing_key=QUEUE_AI),
    Queue(QUEUE_NOTIFICATIONS, task_exchange, routing_key=QUEUE_NOTIFICATIONS),
    Queue(QUEUE_KNOWLEDGE, task_exchange, routing_key=QUEUE_KNOWLEDGE),
    Queue(QUEUE_REPORTS, task_exchange, routing_key=QUEUE_REPORTS),
    Queue(QUEUE_DEPLOYMENTS, task_exchange, routing_key=QUEUE_DEPLOYMENTS),
    Queue(QUEUE_MAINTENANCE, task_exchange, routing_key=QUEUE_MAINTENANCE),
)
