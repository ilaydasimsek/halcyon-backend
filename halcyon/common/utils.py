import os

from django.core.exceptions import ImproperlyConfigured


def read_from_env(key, return_type=str, default_value=None, required=False):
    env_variable = os.environ.get(key)
    if env_variable is None:
        if required is True:
            raise ImproperlyConfigured(f"{key} is not supplied as an env variable")
        return default_value

    if return_type is str:
        return env_variable
    elif return_type is int:
        return int(env_variable)
    elif return_type is bool:
        return env_variable == "True"
    elif return_type is list:
        return [item.strip() for item in env_variable.split(",")]

    raise ValueError(f"Unknown return_type given {return_type}")
