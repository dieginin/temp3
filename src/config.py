import toml


def _get_app_version() -> str:
    pyproject = toml.load("pyproject.toml")
    return pyproject["project"]["version"]


VERSION = _get_app_version()
