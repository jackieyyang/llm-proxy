from fastapi import FastAPI, HTTPException
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exceptions import RequestValidationError
from .api.management_api import router as management_router
from .api.proxy_api import router as proxy_router
from .config.env_config import init_env
from .config import global_vars
from .config.lifespan_config import lifespan
from .config.logger_config import init_logger
from .middleware.trace_middleware import trace_middleware
from .exception.exception_handler import (
    http_exception_handler,
    validation_exception_handler,
    fallback_exception_handler,
)

init_env()
init_logger(global_vars.get_value("LOG_LEVEL"))


app = FastAPI(lifespan=lifespan)

# Register routers
app.include_router(management_router, prefix="/management", tags=["Management"])
app.include_router(proxy_router, prefix="/proxy", tags=["Proxy"])

# Register middleware
app.middleware("http")(trace_middleware)

# Register exception handlers
app.exception_handler(HTTPException)(http_exception_handler)
app.exception_handler(StarletteHTTPException)(http_exception_handler)
app.exception_handler(RequestValidationError)(validation_exception_handler)
app.exception_handler(Exception)(fallback_exception_handler)