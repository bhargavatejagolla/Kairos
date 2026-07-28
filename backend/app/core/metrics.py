from prometheus_client import Counter, Histogram

# --- HTTP Metrics ---
http_requests_total = Counter(
    "kairos_http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"]
)

http_request_duration_seconds = Histogram(
    "kairos_http_request_duration_seconds",
    "HTTP request duration in seconds",
    ["method", "endpoint"]
)

# --- Business Metrics ---
incidents_created_total = Counter(
    "kairos_incidents_created_total",
    "Total number of incidents created",
    ["organization_id", "severity"]
)

alerts_triggered_total = Counter(
    "kairos_alerts_triggered_total",
    "Total number of alerts triggered",
    ["organization_id", "source"]
)

ai_resolutions_total = Counter(
    "kairos_ai_resolutions_total",
    "Total number of AI automated actions or suggestions",
    ["organization_id", "action_type"]
)

notifications_sent_total = Counter(
    "kairos_notifications_sent_total",
    "Total number of notifications dispatched",
    ["organization_id", "channel"]
)
