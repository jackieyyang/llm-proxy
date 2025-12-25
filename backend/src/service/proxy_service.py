import time

from ..adapter.base import BaseAdapter
from ..util import logger_util


async def chat_completions(request: dict) -> dict:
    adapter = BaseAdapter.create(provider="tencent", api_key="xxxx")  # Ensure TencentAdapter is registered
    return await adapter.chat_completion(messages=request.get("messages", []), **request)


async def stream_chat_completions(request):
    start = time.perf_counter()
    logger_util.full_info("invoked_start", "Starting streaming response")
    yield "data: This is a streaming response chunk 1.\n\n"
    import asyncio
    await asyncio.sleep(2)
    yield "data: This is a streaming response chunk 2.\n\n"
    await asyncio.sleep(2)
    yield "data: This is a streaming response chunk 3.\n\n"
    end = int((time.perf_counter() - start) * 1000)
    logger_util.full_info("invoked_end", "invoked_cost[{}ms]", end)