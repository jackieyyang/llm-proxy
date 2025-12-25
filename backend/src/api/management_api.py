from typing import Dict, Any, Coroutine

from fastapi import APIRouter
from ..mapper import management_mapper

router = APIRouter()


@router.get("/health", operation_id="get_management_health")
async def get_management_health() -> dict:
    """
    Management API Health Check Endpoint

    Returns:
        mode (str): The mode of the API, which is "management" or "proxy".
        status (str): The health status of the API, which is "healthy" if the API is functioning properly.
    """
    return {"mode": "management", "status": "healthy"}


@router.get("/users", operation_id="get_users")
async def get_users() -> dict:
    """
    Get a list of users.

    Returns:
        list: A list of user dictionaries.
    """
    # 这里可以添加实际的用户获取逻辑
    users = await management_mapper.fetch_users()
    return {"users": users}