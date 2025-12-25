from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from .api.management_api import router as management_router
from .config.env_config import init_env
from .config.lifespan_config import lifespan
from .config.logger_config import init_logger
from .exception.exception_handler import (
    http_exception_handler,
    validation_exception_handler,
    fallback_exception_handler,
)
from .middleware.trace_middleware import trace_middleware

init_env()
init_logger()

app = FastAPI(lifespan=lifespan)

# Register routers
app.include_router(management_router, prefix="/management")

# Register middleware
app.middleware("http")(trace_middleware)

# Register exception handlers
app.exception_handler(HTTPException)(http_exception_handler)
app.exception_handler(StarletteHTTPException)(http_exception_handler)
app.exception_handler(RequestValidationError)(validation_exception_handler)
app.exception_handler(Exception)(fallback_exception_handler)

