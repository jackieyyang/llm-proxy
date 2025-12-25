# LLM Proxy

## 架构

工厂模式 + Provider 模式设计，支持多种大语言模型服务提供商的无缝切换和扩展。

## 支持的提供商

## 快速开始

## 日志
- 使用 {} 进行延迟加载，避免不必要的计算开销。
- 自定义 utlil/logger.py 模块，提供更丰富的日志功能。
- 
```python
from util import logger

logger.full_info("START", "请求参数: {}", params)
# Output
# trace_id[4003176a-xxx], mode[proxy], stage[START], 请求参数: {参数内容}
```

## 数据库交互

- 使用原生 SQL 语句进行数据库操作，避免 ORM 带来的性能损耗。
- 对比：

## 运行与部署

## 性能对比