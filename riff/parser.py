import os.path
import yaml


def parse(filepath: str) -> dict:
    if os.path.isfile(filepath):
        with open(filepath, "r") as filehandle:
            return yaml.load(filehandle, Loader=yaml.FullLoader)
    raise FileNotFoundError
