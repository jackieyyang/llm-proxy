def _init():  # pragma: no cover
    """
    Initialize the global variable dictionary
    """
    try:
        if is_initialized():
            return
        raise NameError
    except NameError:
        global _global_dict
        _global_dict = {}


def is_initialized():
    """
    Check if the global variable dictionary is initialized

    Returns:
        bool: True if initialized, False otherwise
    """
    try:
        _ = _global_dict
        return True
    except NameError:
        return False


def set_value(key, value):
    """
    Set a value in the global variable dictionary

    Args:
        key: Key in the global variable dictionary
        value: Value to associate with the key
    """
    try:
        _global_dict[key] = value
    except NameError:
        _init()
        set_value(key, value)


def get_value(key, default_value=None):
    """
    Get a value from the global variable dictionary

    Args:
        key: Key in the global variable dictionary
        default_value: Default value if the key does not exist

    Returns:
        Value associated with the key, or default_value if the key does not exist
    """
    try:
        return _global_dict[key]
    except KeyError:
        return default_value
    except NameError:
        _init()
        return get_value(key, default_value)


def items() -> dict:
    """
    Get all key-value pairs in the global variable dictionary

    Returns:
        dict: All key-value pairs in the global variable dictionary
    """
    return _global_dict


def get_sys_value(key):
    """
    Get a system configuration value

    Args:
        key: Key in the system configuration

    Returns:
        Value associated with the key in the system configuration
    """
    return get_value("rb_system_json", {}).get(key)
