import uuid
import time
from loguru import logger
from ..model.context_vars import trace_id, mode, start_time


def __since(start: float) -> float:
    """
    Calculate the elapsed time since the given start time.

    Args:
        start: A timestamp from time.perf_counter()

    Returns:
        Elapsed time in milliseconds
    """
    return int((time.perf_counter() - start) * 1000)


def full_info(__stage: str, __message: str = "", *args) -> None:
    """
    Generate a full information dictionary for tracing.

    Args:
        __stage: The stage name
        __message: Message template with {} placeholders
        *args: Arguments for message formatting

    Returns:
        A dictionary containing trace information.
    """
    # init trace_id if not set
    if not trace_id.get():
        trace_id.set(str(uuid.uuid4()))

    # init start_time if not set
    if not start_time.get():
        start_time.set(time.perf_counter())

    # format message if args provided
    formatted_message = __message.format(*args) if args else __message

    # log full info
    logger.info("trace_id[{}], mode[{}], stage[{}], total_cost[{}ms]{}",
                trace_id.get(), mode.get(), __stage, __since(start_time.get()), f", {formatted_message}" if formatted_message else "")
