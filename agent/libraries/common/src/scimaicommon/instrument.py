from openinference.instrumentation.smolagents import SmolagentsInstrumentor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor


def initialize_tracing(tracing_endpoint: str) -> None:
  """Initialize tracing for smolagents.

  This function sets up a tracing provider with a span processor that exports
  spans to the specified tracing endpoint. It also instruments the application
  with the configured tracer provider.

  Args:
    tracing_endpoint (str): The endpoint to which the tracing data will be exported.

  Returns:
    None

  """
  trace_provider = TracerProvider()
  trace_provider.add_span_processor(SimpleSpanProcessor(OTLPSpanExporter(tracing_endpoint)))

  SmolagentsInstrumentor().instrument(tracer_provider=trace_provider)
