import logging

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from app.core.config import settings


def configure_tracing() -> None:
    """Configures the global OpenTelemetry tracer provider."""
    if not settings.enable_tracing:
        return
    
    # 1. Define Resource attributes (metadata for traces)
    resource = Resource(attributes={
        SERVICE_NAME: settings.app_name
    })

    # 2. Create Tracer Provider
    provider = TracerProvider(resource=resource)

    # 3. Configure OTLP Exporter (sending traces to Jaeger/Tempo)
    # Default endpoint usually points to localhost:4317 (gRPC) if not specified by env vars
    try:
        otlp_exporter = OTLPSpanExporter(insecure=True)
        processor = BatchSpanProcessor(otlp_exporter)
        provider.add_span_processor(processor)
    except Exception as e:
        logging.warning(f"Failed to initialize OTLP exporter: {e}")

    # 4. Register the global tracer provider
    trace.set_tracer_provider(provider)
