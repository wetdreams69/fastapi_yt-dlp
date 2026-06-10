import logging
from fastapi import FastAPI, status, Depends
from fastapi.responses import JSONResponse, RedirectResponse

from app.dependencies import get_stream_service
from app.services.stream_service import StreamService
from app.resolvers.resolver_interface import ResolutionError
from app.logger_config import setup_logging
from app.config import get_settings

settings = get_settings()
setup_logging(settings.log_level)

logger = logging.getLogger(__name__)

app = FastAPI()


@app.exception_handler(ResolutionError)
def resolution_error_handler(request, exc: ResolutionError):
    logger.error("Resolution failed: %s", str(exc), exc_info=exc)
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc)},
    )


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/resolve")
def resolve(
    url: str,
    service: StreamService = Depends(get_stream_service)
):
    stream = service.resolve(url)
    return RedirectResponse(url=stream.stream_url)
