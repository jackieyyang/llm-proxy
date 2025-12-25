from fastapi import Request
from ..util import logger_util
from ..model.context_vars import trace_id, mode


async def trace_middleware(request: Request, call_next):
    """Middleware for request tracing and logging."""
    # 开始事件
    mode.set(request.url.path.split("/")[1]
             if len(request.url.path.split("/")) > 1 else "unknown")

    logger_util.full_info("START", "url[{}], method[{}]",
                     request.url.path, request.method)

    # 处理请求
    response = await call_next(request)

    # 完成事件
    # - 如果是管理端点，使用默认日志；
    # - 如果是代理端点且是流式响应，则在流结束时记录完成日志
    if request.url.path.startswith("/management"):
        logger_util.full_info("DONE")
    
    response.headers["Trace-ID"] = trace_id.get()
    return response
