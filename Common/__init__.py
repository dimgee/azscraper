from configparser import ConfigParser
from pathlib import Path

PATH_COMMON = Path(__file__).parent.absolute()

CONFIG = ConfigParser()
CONFIG.read('config.ini')

__categories = CONFIG['valid_categories']._options()
VALID_CATEGORIES = [x for x in __categories if CONFIG['valid_categories'][x] == 'True']
