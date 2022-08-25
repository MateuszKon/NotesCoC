import pathlib


def get_project_directory():
    return pathlib.Path(__file__).parent.parent.resolve()
