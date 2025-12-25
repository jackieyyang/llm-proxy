from ..util import db_util


async def fetch_users() -> list:
    """
    Fetch all users from the database.

    Returns:
        list[dict]: A list of user records as dictionaries.
    """
    return await db_util.fetch("select * from llm_proxy.tb_user", to_list=True)