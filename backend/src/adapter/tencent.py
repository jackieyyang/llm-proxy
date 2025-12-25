from .base import BaseAdapter
from ..util import logger_util


@BaseAdapter.register("tencent")
class TencentAdapter(BaseAdapter):
    def __init__(self, **config):
        super().__init__(**config)

    async def chat_completion(self, messages, **kwargs) -> dict:
        logger_util.full_info("invoke_start", "Called with messages: {}", messages)
        logger_util.full_info("invoke_end", "Completed processing messages.")
        return {"message": "This is a Tencent chat completion response."}