class TaskRetryLimitExceeded(Exception):
    """Raised when a task exceeds its maximum retry limit."""

class DeadLetterQueueError(Exception):
    """Raised when a task fails and must be moved to the DLQ."""
