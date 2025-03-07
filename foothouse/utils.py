from pathlib import Path

import yaml
from scrapy.utils.project import get_project_settings


def read_config():
    """
    Read the config file and return the settings
    """
    with open("config.yml", "r") as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)


def read_requirements(file_path: Path = Path("requirements.txt").resolve()):
    """Read and parse requirements.txt file"""
    reqs = [req.strip() for req in file_path.read_text().splitlines()]
    return [req for req in reqs if req and not req.startswith("#")]
