import httpx
from . import global_vars


async def init_httpx_client():
    """
    Init httpx client
    """
    client = httpx.AsyncClient(
        timeout=httpx.Timeout(
            connect=3.0,    # 建连
            read=60.0,      # 等模型吐 token
            write=10.0,     # 发请求体
            pool=5.0        # 等连接池
        )
    )
    global_vars.set_value("HTTPX_CLIENT", client)


async def close_httpx_client():
    """
    Close the postgreSQL database connection.
    """
    httpx_client: httpx.AsyncClient = global_vars.get_value("HTTPX_CLIENT")
    await httpx_client.aclose()