import time
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

# Configure standard JSON-like logging for production (easier for Datadog/CloudWatch to parse)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger("aria.telemetry")

class TelemetryMiddleware(BaseHTTPMiddleware):
    """
    Milestone 12: Observability
    Logs all incoming requests, their execution time, and status code.
    In a full production environment, this is where OpenTelemetry 
    or Datadog APM tracing decorators would be initialized.
    """
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        response = await call_next(request)
        
        process_time = (time.time() - start_time) * 1000
        logger.info(
            f"METHOD={request.method} "
            f"PATH={request.url.path} "
            f"STATUS={response.status_code} "
            f"DURATION={process_time:.2f}ms "
            f"IP={request.client.host if request.client else 'unknown'}"
        )
        
        # Inject standard telemetry headers
        response.headers["X-Process-Time-Ms"] = str(round(process_time, 2))
        return response
