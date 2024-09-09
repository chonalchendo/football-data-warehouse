import yaml
from scrapy.utils.project import get_project_settings


def read_config(): 
    """
    Read the config file and return the settings
    """
    with open("config.yml", 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
