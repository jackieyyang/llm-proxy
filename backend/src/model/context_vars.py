from contextvars import ContextVar

# Context variable to store the state for the current coroutine
trace_id: ContextVar[str] = ContextVar("trace_id", default="")
mode: ContextVar[str] = ContextVar("mode", default="")
start_time: ContextVar[float] = ContextVar("start_time", default=0.0)