from fastapi import APIRouter
from starlette.responses import StreamingResponse, JSONResponse

from ..service import proxy_service

router = APIRouter()

@router.get("/health", operation_id="get_proxy_health")
async def get_proxy_health() -> dict:
    """代理健康检查端点"""
    return {"mode": "proxy", "status": "healthy"}


@router.post("/chat/completions", operation_id="post_chat_completions", response_model=None)
async def chat_completions(request: dict) -> JSONResponse | StreamingResponse:
    """处理聊天请求的代理端点"""
    async def streaming_response_generator():
        import asyncio
        yield "data: This is a streaming response chunk 1.\n\n"
        await asyncio.sleep(2)
        yield "data: This is a streaming response chunk 2.\n\n"
        await asyncio.sleep(2)
        yield "data: This is a streaming response chunk 3.\n\n"

    if request["stream"]:
        return StreamingResponse(
            content=proxy_service.stream_chat_completions(request),
            media_type="text/event-stream"
        )

    return JSONResponse(
        content=await proxy_service.chat_completions(request)
    )