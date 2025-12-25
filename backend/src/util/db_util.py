from typing import Any
import asyncpg
from ..config import global_vars


async def fetch(query: Any,
                *args: Any,
                timeout: Any = None,
                record_class: Any = None,
                to_list: bool = False) -> list:
    """
    Fetch records from the database.

    Args:
        query: The SQL query to execute.
        *args: Arguments for the SQL query.
        timeout: Optional timeout for the query.
        record_class: Optional class to use for records.
        to_list: If True, convert records to list of dicts.

    Returns:
        list: A list of records (as dicts if as_dict=True, otherwise asyncpg.Record).
    """
    pool: asyncpg.Pool = global_vars.get_value("DB_POOL")
    records = await pool.fetch(query, *args, timeout=timeout, record_class=record_class)
    return [dict(record) for record in records] if to_list else records