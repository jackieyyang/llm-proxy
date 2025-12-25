from .base import BaseAdapter
from ..util import logger_util


@BaseAdapter.register("aliyun")
class AliyunAdapter(BaseAdapter):
    def __init__(self, **config):
        super().__init__(**config)

    async def chat_completion(self, messages, **kwargs) -> dict:
        # Implement Tencent-specific chat completion logic here
        logger_util.full_info("TencentAdapter.chat_completion", "Called with messages: {}", messages)
        return {"message": "This is a Tencent chat completion response."}