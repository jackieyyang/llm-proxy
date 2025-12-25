import os
import shutil
from dotenv import dotenv_values
from . import global_vars


def init_env() -> None:
    """
    Init environment variables from .env file.

    If .env does not exist, copy from .env.example.
    """
    # Get the directory where this config file is located (backend/src/config/)
    config_dir = os.path.dirname(os.path.abspath(__file__))
    # Navigate to src directory (backend/src/)
    src_dir = os.path.dirname(config_dir)
    
    path = os.path.join(src_dir, ".env")
    example_path = os.path.join(src_dir, ".env.example")

    if not os.path.exists(path):
        if os.path.exists(example_path):
            shutil.copy(example_path, path)
        else:
            raise FileNotFoundError(f"Neither .env nor .env.example found in {src_dir}")

    for key, value in (dotenv_values(path) | dict(os.environ)).items():
        global_vars.set_value(key, value)
