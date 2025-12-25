import asyncpg
from . import global_vars


async def init_db_connection():
    """
    Init the postgreSQL database connection.
    """
    pool = await asyncpg.create_pool(
        user=global_vars.get_value("DB_USER"),               # Username
        password=global_vars.get_value("DB_PASSWORD"),       # Password
        database=global_vars.get_value("DB_DATABASE"),       # Database name
        host=global_vars.get_value("DB_HOST"),               # Host address
        port=int(global_vars.get_value("DB_PORT")),          # Port number
        min_size=int(global_vars.get_value("DB_MIN_SIZE")),  # Minimum number of connections in the pool
        max_size=int(global_vars.get_value("DB_MAX_SIZE")),  # Maximum number of connections in the pool
        timeout=int(global_vars.get_value("DB_TIMEOUT"))     # Connection timeout in seconds
    )
    global_vars.set_value("DB_POOL", pool)


async def close_db_connection():
    """
    Close the postgreSQL database connection.
    """
    db_pool: asyncpg.Pool = global_vars.get_value("DB_POOL")
    await db_pool.close()