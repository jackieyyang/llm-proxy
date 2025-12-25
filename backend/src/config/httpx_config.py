import httpx
from . import global_vars


async def init_httpx_client():
    """
    Init httpx client
    """
    client = httpx.AsyncClient(
        timeout=httpx.Timeout(
            connect=3.0,    # Connect timeout
            read=60.0,      # Waiting for response timeout
            write=10.0,     # Writing request timeout
            pool=5.0        # Waiting for a connection from the pool timeout
        )
    )
    global_vars.set_value("HTTPX_CLIENT", client)


async def close_httpx_client():
    """
    Close the postgreSQL database connection.
    """
    httpx_client: httpx.AsyncClient = global_vars.get_value("HTTPX_CLIENT")
    await httpx_client.aclose()