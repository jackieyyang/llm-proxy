from .base import BaseAdapter

# Import all adapters to trigger registration via decorators
from .tencent import TencentAdapter
# from .aliyun import AliyunAdapter
# from .azure import AzureAdapter
# from .deepseek import DeepseekAdapter
# from .openai import OpenAIAdapter

__all__ = [
    "BaseAdapter",
    "TencentAdapter",
    # "AliyunAdapter",
    # "AzureAdapter",
    # "DeepseekAdapter",
    # "OpenAIAdapter",
]
